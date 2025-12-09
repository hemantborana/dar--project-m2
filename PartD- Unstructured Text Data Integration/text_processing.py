"""
Part D - Task 1: Text Data Processing (35 minutes)
Web scraping, text extraction, preprocessing
Hemant Borana - Dec 2024
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import re
import os

os.makedirs('outputs/text', exist_ok=True)
os.makedirs('data/text', exist_ok=True)

scraped_data = []
errors = []

print("\n" + "="*60)
print("PART D - UNSTRUCTURED TEXT DATA PROCESSING")
print("="*60 + "\n")

# 1. Scrape Wikipedia articles
print("--- Task 1: Scraping Wikipedia Articles ---\n")

# need headers to avoid 403 error
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

wiki_topics = [
    'Artificial_intelligence',
    'Machine_learning',
    'Data_science'
]

for topic in wiki_topics:
    try:
        url = f'https://en.wikipedia.org/wiki/{topic}'
        print(f"Scraping: {topic.replace('_', ' ')}...")
        
        # add headers parameter here
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # get title
        title = soup.find('h1', class_='firstHeading')
        title_text = title.get_text() if title else topic.replace('_', ' ')
        
        # get first few paragraphs
        content = []
        paragraphs = soup.find_all('p')
        for p in paragraphs[:5]:  # first 5 paragraphs
            text = p.get_text().strip()
            if len(text) > 50:  # skip short paragraphs
                content.append(text)
        
        article_text = ' '.join(content)
        
        # basic preprocessing
        # removing citations like [1], [2]
        article_text = re.sub(r'\[\d+\]', '', article_text)
        # removing extra whitespace
        article_text = re.sub(r'\s+', ' ', article_text).strip()
        
        scraped_data.append({
            'source': 'Wikipedia',
            'topic': topic.replace('_', ' '),
            'title': title_text,
            'content': article_text,
            'word_count': len(article_text.split()),
            'char_count': len(article_text),
            'scraped_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'url': url
        })
        
        print(f"  ✓ Got {len(article_text.split())} words")
        
    except Exception as e:
        error_msg = f"Failed to scrape {topic}: {str(e)}"
        print(f"  ✗ {error_msg}")
        errors.append(error_msg)

print(f"\nScraped {len(scraped_data)} Wikipedia articles\n")

# 2. Scrape news from RSS feed 
print("--- Task 2: Scraping News RSS Feed ---\n")

try:
    # using BBC RSS feed
    rss_url = 'http://feeds.bbci.co.uk/news/rss.xml'
    print(f"Fetching RSS feed from BBC News...")
    
    response = requests.get(rss_url, timeout=10)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, 'xml')
    
    items = soup.find_all('item')[:5]  # get first 5 news items
    
    for item in items:
        try:
            title = item.find('title').get_text() if item.find('title') else 'No title'
            desc = item.find('description').get_text() if item.find('description') else 'No description'
            link = item.find('link').get_text() if item.find('link') else ''
            pub_date = item.find('pubDate').get_text() if item.find('pubDate') else ''
            
            # clean description
            desc = re.sub(r'<[^>]+>', '', desc)  # removing html tags
            desc = re.sub(r'\s+', ' ', desc).strip()
            
            scraped_data.append({
                'source': 'BBC News RSS',
                'topic': 'News',
                'title': title,
                'content': desc,
                'word_count': len(desc.split()),
                'char_count': len(desc),
                'scraped_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'url': link
            })
            
        except Exception as e:
            print(f"  Error parsing news item: {e}")
            continue
    
    print(f"  ✓ Got {len(items)} news articles from RSS feed\n")
    
except Exception as e:
    error_msg = f"Failed to fetch RSS feed: {str(e)}"
    print(f"  ✗ {error_msg}\n")
    errors.append(error_msg)

# 3. Scrape GitHub trending repositories (alternative text source)
print("--- Task 3: Scraping GitHub Trending ---\n")

try:
    # GitHub API - get trending repositories info
    api_url = 'https://api.github.com/search/repositories?q=stars:>1000&sort=stars&order=desc&per_page=10'
    print("Fetching data from GitHub API...")
    
    response = requests.get(api_url, timeout=10)
    response.raise_for_status()
    github_data = response.json()
    
    items = github_data.get('items', [])
    
    for repo in items:
        name = repo.get('name', 'Unknown')
        desc = repo.get('description', 'No description available')
        owner = repo.get('owner', {}).get('login', 'Unknown')
        
        if desc:  # only if description exists
            scraped_data.append({
                'source': 'GitHub API',
                'topic': 'Technology',
                'title': f'{owner}/{name}',
                'content': desc,
                'word_count': len(desc.split()),
                'char_count': len(desc),
                'scraped_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'url': repo.get('html_url', '')
            })
    
    print(f"  ✓ Got {len(items)} repository descriptions\n")
    
except Exception as e:
    error_msg = f"Failed to fetch GitHub data: {str(e)}"
    print(f"  ✗ {error_msg}\n")
    errors.append(error_msg)

# Convert to DataFrame
print("--- Processing Scraped Data ---\n")
df = pd.DataFrame(scraped_data)

if len(df) > 0:
    print(f"Total items scraped: {len(df)}")
    print(f"Sources: {df['source'].unique()}")
    print(f"\nData by source:")
    print(df.groupby('source').size())
    
    # Text preprocessing and analysis
    print("\n--- Text Preprocessing ---\n")
    
    # basic text cleaning
    def clean_text(text):
        # lowercase
        text = text.lower()
        # remove special characters but keep spaces
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        # remove extra spaces
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    df['cleaned_content'] = df['content'].apply(clean_text)
    
    # word frequency analysis
    print("Calculating text statistics...")
    df['sentence_count'] = df['content'].apply(lambda x: len(re.split(r'[.!?]+', x)))
    df['avg_word_length'] = df['content'].apply(lambda x: sum(len(word) for word in x.split()) / len(x.split()) if len(x.split()) > 0 else 0)
    
    # metadata creation
    print("Creating metadata...")
    df['processed_date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    df['text_category'] = df['source'].apply(lambda x: 'encyclopedia' if 'Wiki' in x else 'news' if 'News' in x else 'quotes')
    
    # save raw scraped data
    df.to_csv('outputs/text/scraped_text_data.csv', index=False)
    df.to_excel('outputs/text/scraped_text_data.xlsx', index=False)
    print("\n✓ Saved scraped_text_data.csv and .xlsx")
    
    # create summary statistics
    print("\n--- Text Data Summary ---")
    summary = {
        'total_documents': len(df),
        'total_words': df['word_count'].sum(),
        'total_characters': df['char_count'].sum(),
        'avg_words_per_doc': df['word_count'].mean(),
        'min_words': df['word_count'].min(),
        'max_words': df['word_count'].max(),
        'sources': len(df['source'].unique())
    }
    
    for key, value in summary.items():
        print(f"{key}: {value if isinstance(value, int) else f'{value:.2f}'}")
    
    # save summary
    summary_df = pd.DataFrame([summary])
    summary_df.to_csv('outputs/text/text_summary.csv', index=False)
    
    # word cloud data (top words)
    print("\n--- Extracting Key Terms ---")
    from collections import Counter
    
    # combine all cleaned text
    all_text = ' '.join(df['cleaned_content'].tolist())
    words = all_text.split()
    
    # remove common stop words
    stop_words = ['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                  'of', 'with', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
                  'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
                  'this', 'that', 'these', 'those', 'it', 'its', 'they', 'them']
    
    filtered_words = [w for w in words if w not in stop_words and len(w) > 3]
    
    # get top 20 words
    word_freq = Counter(filtered_words).most_common(20)
    
    print("\nTop 20 words:")
    for word, count in word_freq[:10]:
        print(f"  {word}: {count}")
    
    # save word frequency
    word_freq_df = pd.DataFrame(word_freq, columns=['word', 'frequency'])
    word_freq_df.to_csv('outputs/text/word_frequency.csv', index=False)
    print("\n✓ Saved word_frequency.csv")
    
else:
    print("No data scraped successfully")


if errors:
    print("\n--- Errors Encountered ---")
    for error in errors:
        print(f"  - {error}")

# Final report
print("\n" + "="*60)
print("TEXT PROCESSING COMPLETE")
print("="*60)

report = f"""
Text Data Processing Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Data Sources:
- Wikipedia articles (encyclopedia content)
- BBC News RSS feed (current news)
- Quotable API (quotes)

Total Documents Scraped: {len(df) if len(df) > 0 else 0}
Total Words: {df['word_count'].sum() if len(df) > 0 else 0:,}
Total Characters: {df['char_count'].sum() if len(df) > 0 else 0:,}

Processing Steps:
1. Web scraping from multiple sources
2. Text extraction and cleaning
3. Preprocessing (lowercase, remove special chars)
4. Metadata creation
5. Statistical analysis
6. Word frequency analysis

Output Files:
- outputs/text/scraped_text_data.csv
- outputs/text/scraped_text_data.xlsx
- outputs/text/text_summary.csv
- outputs/text/word_frequency.csv

Errors: {len(errors)}
"""

with open('outputs/text/text_processing_report.txt', 'w') as f:
    f.write(report)

print(report)
print("\n✓ Report saved to text_processing_report.txt")
print("\nReady for Task 2: Data Integration Pipeline!")