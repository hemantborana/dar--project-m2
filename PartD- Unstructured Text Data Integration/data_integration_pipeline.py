"""
Part D - Task 2: Unstructured Data Integration Pipeline (25 minutes)
Integrating text data from multiple web sources
Hemant Borana - Dec 2024
"""

import pandas as pd
import os
from datetime import datetime
import json
from collections import Counter

print("\n" + "="*70)
print("PART D - TASK 2: UNSTRUCTURED DATA INTEGRATION")
print("="*70 + "\n")


if not os.path.exists('outputs/text/scraped_text_data.csv'):
    print("Error: Run text_processing.py first!")
    exit()

# load the scraped text data
print("--- Loading Scraped Text Data ---\n")
text_df = pd.read_csv('outputs/text/scraped_text_data.csv')
print(f"Loaded {len(text_df)} text documents")
print(f"Sources: {text_df['source'].unique()}")

# Step 1: Combine data from different sources into unified structure
print("\n--- Step 1: Creating Unified Text Data Model ---\n")

# separate by source type
wiki_data = text_df[text_df['source'] == 'Wikipedia']
news_data = text_df[text_df['source'] == 'BBC News RSS']
github_data = text_df[text_df['source'] == 'GitHub API']

print(f"Wikipedia articles: {len(wiki_data)}")
print(f"News articles: {len(news_data)}")
print(f"GitHub repos: {len(github_data)}")

# create unified schema with common fields
unified_records = []

for idx, row in text_df.iterrows():
    record = {
        'document_id': f"DOC_{idx+1:04d}",
        'source_type': row['source'],
        'topic': row['topic'],
        'title': row['title'],
        'content': row['content'],
        'cleaned_content': row.get('cleaned_content', ''),
        'word_count': row['word_count'],
        'char_count': row['char_count'],
        'sentence_count': row.get('sentence_count', 0),
        'avg_word_length': round(row.get('avg_word_length', 0), 2),
        'scraped_date': row['scraped_date'],
        'source_url': row['url'],
        'text_category': row.get('text_category', 'general')
    }
    unified_records.append(record)

unified_df = pd.DataFrame(unified_records)
print(f"\n✓ Created unified dataset with {len(unified_df)} documents")

# Step 2: Data quality measures
print("\n--- Step 2: Data Quality Assessment ---\n")

quality_checks = {
    'total_documents': len(unified_df),
    'null_values': unified_df.isnull().sum().sum(),
    'duplicate_titles': unified_df['title'].duplicated().sum(),
    'empty_content': (unified_df['content'].str.len() < 10).sum(),
    'avg_words_per_doc': round(unified_df['word_count'].mean(), 2),
    'total_words': unified_df['word_count'].sum(),
    'sources_count': unified_df['source_type'].nunique()
}

print("Quality Metrics:")
for metric, value in quality_checks.items():
    print(f"  {metric}: {value}")

# calculate quality score
total_issues = quality_checks['null_values'] + quality_checks['duplicate_titles'] + quality_checks['empty_content']
quality_score = round(100 - (total_issues / len(unified_df) * 100), 2)
print(f"\n  Overall Quality Score: {quality_score}%")

# Step 3: Text content analysis and structuring
print("\n--- Step 3: Text Content Analysis ---\n")

# analyze by source type
source_analysis = unified_df.groupby('source_type').agg({
    'word_count': ['count', 'sum', 'mean'],
    'char_count': 'sum',
    'sentence_count': 'mean'
}).round(2)

print("Analysis by Source:")
print(source_analysis)

# topic distribution
print("\n\nTopic Distribution:")
topic_dist = unified_df['topic'].value_counts()
print(topic_dist)

# Step 4: Extract and structure metadata
print("\n--- Step 4: Creating Document Metadata ---\n")

metadata_records = []
for idx, row in unified_df.iterrows():
    metadata = {
        'document_id': row['document_id'],
        'source': row['source_type'],
        'collection_date': row['scraped_date'],
        'processing_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'language': 'English',  
        'format': 'Plain Text',
        'quality_flag': 'Clean' if row['word_count'] > 10 else 'Review',
        'category': row['text_category'],
        'accessibility': 'Public',
        'retention_period': '1 year'
    }
    metadata_records.append(metadata)

metadata_df = pd.DataFrame(metadata_records)
print(f"Created metadata for {len(metadata_df)} documents")

# Step 5: Content categorization and tagging
print("\n--- Step 5: Content Categorization ---\n")

# extract key terms for each document
def extract_keywords(text, top_n=5):
    """extract top keywords from text"""
    stop_words = ['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for']
    words = str(text).lower().split()
    words = [w for w in words if w not in stop_words and len(w) > 3]
    freq = Counter(words).most_common(top_n)
    return ', '.join([word for word, count in freq])

unified_df['keywords'] = unified_df['cleaned_content'].apply(lambda x: extract_keywords(x))
print("Extracted keywords for all documents")

# categorize by content length
def categorize_length(word_count):
    if word_count < 20:
        return 'Short'
    elif word_count < 100:
        return 'Medium'
    else:
        return 'Long'

unified_df['length_category'] = unified_df['word_count'].apply(categorize_length)

length_dist = unified_df['length_category'].value_counts()
print("\nContent Length Distribution:")
print(length_dist)

# Step 6: Create integrated dataset with all enrichments
print("\n--- Step 6: Creating Final Integrated Dataset ---\n")

# merge metadata with unified data
final_integrated = unified_df.merge(
    metadata_df, 
    on='document_id', 
    how='left'
)

print(f"Final integrated dataset: {len(final_integrated)} records")
print(f"Total columns: {len(final_integrated.columns)}")

# Step 7: Data lineage documentation
print("\n--- Step 7: Documenting Data Lineage ---\n")

lineage = []
source_counts = unified_df['source_type'].value_counts()

for source, count in source_counts.items():
    if source == 'Wikipedia':
        extraction = "Web scraping using BeautifulSoup"
        url_pattern = "https://en.wikipedia.org/wiki/*"
    elif source == 'BBC News RSS':
        extraction = "RSS feed parsing"
        url_pattern = "http://feeds.bbci.co.uk/news/rss.xml"
    else:  # GitHub
        extraction = "REST API call"
        url_pattern = "https://api.github.com/search/repositories"
    
    lineage.append({
        'source_name': source,
        'source_type': 'Web/API',
        'extraction_method': extraction,
        'url_pattern': url_pattern,
        'document_count': count,
        'extraction_date': datetime.now().strftime('%Y-%m-%d'),
        'transformation_steps': 'Text cleaning, tokenization, metadata creation',
        'data_format': 'Unstructured Text → Structured CSV',
        'storage_location': 'outputs/text/'
    })

lineage_df = pd.DataFrame(lineage)
print(lineage_df.to_string(index=False))

# Save all outputs
print("\n--- Step 8: Saving Integrated Outputs ---\n")

os.makedirs('outputs/integrated', exist_ok=True)

# main integrated dataset
final_integrated.to_csv('outputs/integrated/integrated_text_data.csv', index=False)
final_integrated.to_excel('outputs/integrated/integrated_text_data.xlsx', index=False)
print("✓ Saved integrated_text_data.csv and .xlsx")

# metadata
metadata_df.to_csv('outputs/integrated/document_metadata.csv', index=False)
print("✓ Saved document_metadata.csv")

# quality report
quality_df = pd.DataFrame([quality_checks])
quality_df.to_csv('outputs/integrated/quality_report.csv', index=False)
print("✓ Saved quality_report.csv")

# source analysis
source_analysis.to_csv('outputs/integrated/source_analysis.csv')
print("✓ Saved source_analysis.csv")

# lineage
lineage_df.to_csv('outputs/integrated/data_lineage.csv', index=False)
print("✓ Saved data_lineage.csv")

# Generate comprehensive report
print("\n--- Generating Integration Report ---\n")

report = f"""
{'='*70}
UNSTRUCTURED DATA INTEGRATION REPORT
Part D - Task 2
{'='*70}

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

1. DATA SOURCES
{'-'*70}
Total Documents Integrated: {len(unified_df)}

Source Breakdown:
"""

for source, count in source_counts.items():
    report += f"  - {source}: {count} documents\n"

report += f"""
2. DATA INTEGRATION PROCESS
{'-'*70}
Step 1: Extracted text from web sources
  - Wikipedia articles (encyclopedia content)
  - BBC News RSS feed (current news)
  - GitHub API (repository descriptions)

Step 2: Text preprocessing
  - Removed citations and special characters
  - Normalized whitespace
  - Converted to lowercase
  - Tokenization

Step 3: Metadata creation
  - Document IDs assigned
  - Source tracking
  - Timestamp recording
  - Quality flags

Step 4: Content structuring
  - Unified schema creation
  - Keyword extraction
  - Length categorization
  - Topic classification

3. DATA QUALITY METRICS
{'-'*70}
Total Documents: {quality_checks['total_documents']}
Total Words: {quality_checks['total_words']:,}
Average Words/Document: {quality_checks['avg_words_per_doc']}
Null Values: {quality_checks['null_values']}
Duplicate Titles: {quality_checks['duplicate_titles']}
Empty Content: {quality_checks['empty_content']}
Quality Score: {quality_score}%

4. CONTENT ANALYSIS
{'-'*70}
"""

report += "Length Distribution:\n"
for length, count in length_dist.items():
    report += f"  {length}: {count} documents\n"

report += f"""
5. DATA LINEAGE
{'-'*70}
Complete data lineage has been documented showing:
- Original source URLs
- Extraction methods
- Transformation steps
- Storage locations

See: outputs/integrated/data_lineage.csv

6. OUTPUT FILES
{'-'*70}
- integrated_text_data.csv (main dataset)
- integrated_text_data.xlsx (Excel format)
- document_metadata.csv (metadata)
- quality_report.csv (quality metrics)
- source_analysis.csv (source breakdown)
- data_lineage.csv (lineage tracking)

7. UNIFIED DATA SCHEMA
{'-'*70}
"""

report += "Columns in integrated dataset:\n"
for col in final_integrated.columns:
    report += f"  - {col}\n"

report += f"""
8. CHALLENGES ADDRESSED
{'-'*70}
- Different web scraping methods for different sources
- Handling HTML/XML parsing
- Text preprocessing and cleaning
- Creating consistent structure from unstructured data
- Metadata generation for tracking
- Quality assessment implementation

9. RECOMMENDATIONS
{'-'*70}
- Implement sentiment analysis for text content
- Add named entity recognition (NER)
- Create text similarity measures
- Build search/indexing capability
- Add automated summarization
- Implement topic modeling (LDA)
- Schedule periodic data refresh

{'='*70}
END OF INTEGRATION REPORT
{'='*70}
"""

with open('outputs/integrated/INTEGRATION_REPORT.txt', 'w', encoding='utf-8') as f:
    f.write(report)

print(report)

print("\n" + "="*70)
print("PART D COMPLETED SUCCESSFULLY")
print("="*70)
print(f"\nIntegrated {len(unified_df)} text documents from {quality_checks['sources_count']} sources")
print(f"Total words processed: {quality_checks['total_words']:,}")
print(f"Quality score: {quality_score}%")
print("\nAll outputs saved in: outputs/integrated/")