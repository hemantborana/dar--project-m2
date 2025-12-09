"""
Final Data Integration - Part C Complete
Combining structured, semi-structured, and unstructured data
Hemant Borana - Dec 2024
"""

import pandas as pd
import os
from datetime import datetime
import matplotlib.pyplot as plt

print("\n" + "="*60)
print("FINAL DATA INTEGRATION - PART C")
print("="*60 + "\n")

# collect all processed data
all_data = {}

print("Loading processed datasets...\n")

# From JSON processing
json_files = ['users_processed.csv', 'posts_processed.csv', 'countries_processed.csv']
for file in json_files:
    path = f'outputs/{file}'
    if os.path.exists(path):
        name = file.replace('_processed.csv', '')
        df = pd.read_csv(path)
        all_data[f'json_{name}'] = df
        print(f"✓ Loaded {name} from JSON: {len(df)} records")

# From CSV/Excel processing
csv_files = ['sales_clean.csv', 'employees_clean.csv', 'feedback_clean.csv']
for file in csv_files:
    path = f'outputs/{file}'
    if os.path.exists(path):
        name = file.replace('_clean.csv', '')
        df = pd.read_csv(path)
        all_data[f'csv_{name}'] = df
        print(f"✓ Loaded {name} from CSV: {len(df)} records")

# From XML processing
xml_files = ['books_from_xml.csv', 'employees_from_xml.csv', 'products_from_xml.csv']
for file in xml_files:
    path = f'outputs/{file}'
    if os.path.exists(path):
        name = file.replace('_from_xml.csv', '')
        df = pd.read_csv(path)
        all_data[f'xml_{name}'] = df
        print(f"✓ Loaded {name} from XML: {len(df)} records")

print(f"\nTotal datasets loaded: {len(all_data)}")

# create master summary
print("\n--- Creating Master Data Catalog ---")
catalog = []

for name, df in all_data.items():
    source_type = name.split('_')[0]  # json, csv, or xml
    
    info = {
        'dataset_name': name,
        'source_type': source_type.upper(),
        'records': len(df),
        'columns': len(df.columns),
        'memory_kb': round(df.memory_usage(deep=True).sum() / 1024, 2),
        'null_values': df.isnull().sum().sum(),
        'duplicates': df.duplicated().sum()
    }
    catalog.append(info)

catalog_df = pd.DataFrame(catalog)
print("\nData Catalog:")
print(catalog_df.to_string(index=False))

# save catalog
catalog_df.to_csv('outputs/master_data_catalog.csv', index=False)
catalog_df.to_excel('outputs/master_data_catalog.xlsx', index=False)
print("\n✓ Saved master_data_catalog.csv and .xlsx")

# overall statistics
print("\n--- Overall Statistics ---")
total_records = catalog_df['records'].sum()
total_cols = catalog_df['columns'].sum()
total_mem = catalog_df['memory_kb'].sum()

print(f"Total Records: {total_records:,}")
print(f"Total Columns: {total_cols}")
print(f"Total Memory: {total_mem:.2f} KB")
print(f"Data Sources: JSON ({len([d for d in all_data if d.startswith('json')])}), "
      f"CSV ({len([d for d in all_data if d.startswith('csv')])}), "
      f"XML ({len([d for d in all_data if d.startswith('xml')])})")

# data quality summary
print("\n--- Data Quality Summary ---")
total_nulls = catalog_df['null_values'].sum()
total_dups = catalog_df['duplicates'].sum()
print(f"Total Null Values: {total_nulls}")
print(f"Total Duplicates: {total_dups}")

quality_score = 100 - ((total_nulls + total_dups) / total_records * 100)
print(f"Overall Data Quality Score: {quality_score:.2f}%")

print("\n--- Example Integration: Employee Data ---")
emp_datasets = []

if 'csv_employees' in all_data:
    csv_emp = all_data['csv_employees'][['emp_id', 'name', 'department', 'salary']].copy()
    csv_emp['source'] = 'CSV'
    emp_datasets.append(csv_emp)
    print(f"CSV employees: {len(csv_emp)}")

if 'xml_employees' in all_data:
    xml_emp = all_data['xml_employees'][['id', 'name', 'department', 'salary']].copy()
    xml_emp.rename(columns={'id': 'emp_id'}, inplace=True)
    xml_emp['source'] = 'XML'
    emp_datasets.append(xml_emp)
    print(f"XML employees: {len(xml_emp)}")

if emp_datasets:
    # combine all employee data
    combined_emp = pd.concat(emp_datasets, ignore_index=True)
    
    # some stats
    print(f"\nCombined employee dataset: {len(combined_emp)} total employees")
    print(f"Departments: {combined_emp['department'].nunique()}")
    print(f"Salary range: ${combined_emp['salary'].min():,} - ${combined_emp['salary'].max():,}")
    
    combined_emp.to_csv('outputs/integrated_employees.csv', index=False)
    print("✓ Saved integrated_employees.csv")

# create visualization (simple bar chart)
print("\n--- Creating Visualization ---")
try:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # chart 1: records by source type
    source_counts = catalog_df.groupby('source_type')['records'].sum()
    ax1.bar(source_counts.index, source_counts.values, color=['#3498db', '#2ecc71', '#e74c3c'])
    ax1.set_title('Records by Source Type', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Source Type')
    ax1.set_ylabel('Number of Records')
    ax1.grid(axis='y', alpha=0.3)
    
    # chart 2: data quality
    quality_data = {
        'Good': total_records - total_nulls - total_dups,
        'Nulls': total_nulls,
        'Duplicates': total_dups
    }
    colors = ['#2ecc71', '#f39c12', '#e74c3c']
    ax2.pie(quality_data.values(), labels=quality_data.keys(), autopct='%1.1f%%', 
            colors=colors, startangle=90)
    ax2.set_title('Data Quality Distribution', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('outputs/integration_analysis.png', dpi=300, bbox_inches='tight')
    print("✓ Saved integration_analysis.png")
    plt.close()
except Exception as e:
    print(f"Visualization skipped: {e}")

# generate final comprehensive report
print("\n--- Generating Final Report ---")

report = f"""
{'='*60}
DATA INTEGRATION PROJECT - PART C COMPLETE
{'='*60}

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

PROJECT SUMMARY
{'-'*60}
This project demonstrates comprehensive data integration from
multiple sources including structured, semi-structured, and 
unstructured data formats.

DATA SOURCES PROCESSED
{'-'*60}

1. STRUCTURED DATA (JSON APIs)
   - JSONPlaceholder Users API: {len(all_data.get('json_users', [])):,} records
   - JSONPlaceholder Posts API: {len(all_data.get('json_posts', [])):,} records
   - REST Countries API: {len(all_data.get('json_countries', [])):,} records
   
2. SEMI-STRUCTURED DATA (CSV/Excel)
   - Sales Data: {len(all_data.get('csv_sales', [])):,} records
   - Employee Data: {len(all_data.get('csv_employees', [])):,} records
   - Customer Feedback: {len(all_data.get('csv_feedback', [])):,} records
   
3. UNSTRUCTURED DATA (XML)
   - Books Catalog: {len(all_data.get('xml_books', [])):,} records
   - Employee Records: {len(all_data.get('xml_employees', [])):,} records
   - Product Inventory: {len(all_data.get('xml_products', [])):,} records

OVERALL STATISTICS
{'-'*60}
Total Datasets: {len(all_data)}
Total Records: {total_records:,}
Total Columns: {total_cols}
Memory Usage: {total_mem:.2f} KB
Data Quality Score: {quality_score:.2f}%

DATA QUALITY METRICS
{'-'*60}
Null Values Found: {total_nulls:,}
Duplicate Records: {total_dups:,}
Clean Records: {total_records - total_nulls - total_dups:,}

TECHNICAL ACHIEVEMENTS
{'-'*60}
✓ Successfully extracted data from REST APIs (JSON)
✓ Handled multiple CSV encodings (UTF-8, Latin-1)
✓ Processed Excel files with multiple sheets
✓ Parsed XML with namespaces and attributes
✓ Implemented comprehensive error handling
✓ Created unified data model across sources
✓ Generated data quality reports
✓ Performed data integration and merging
✓ Created visualizations for analysis

OUTPUT FILES GENERATED
{'-'*60}
"""

# list all output files
output_files = [f for f in os.listdir('outputs') if os.path.isfile(f'outputs/{f}')]
for i, file in enumerate(sorted(output_files), 1):
    report += f"{i:2d}. {file}\n"

report += f"""
{'-'*60}
Total Output Files: {len(output_files)}

CHALLENGES ADDRESSED
{'-'*60}
- Handled missing and null values across datasets
- Resolved encoding issues (UTF-8, Latin-1)
- Parsed nested JSON structures
- Extracted data from XML with namespaces
- Processed different CSV delimiters
- Integrated data from heterogeneous sources
- Implemented data validation and quality checks

RECOMMENDATIONS
{'-'*60}
1. Implement automated data validation pipelines
2. Set up regular data quality monitoring
3. Create standardized data ingestion templates
4. Establish data governance policies
5. Implement incremental data loading for large datasets

{'='*60}
END OF REPORT
{'='*60}
"""

# save report
with open('outputs/FINAL_INTEGRATION_REPORT.txt', 'w', encoding='utf-8') as f:
    f.write(report)

print(report)
print("\n✓ Saved FINAL_INTEGRATION_REPORT.txt")

print("\n" + "="*60)
print(" PART C COMPLETED SUCCESSFULLY!")
print("="*60)
print(f"\nTotal files created: {len(output_files)}")
print("Check outputs/ folder for all results.")
print("\nProject demonstrates:")
print("  ✓ JSON data extraction and transformation")
print("  ✓ CSV/Excel processing with encoding handling")
print("  ✓ XML parsing with namespaces")
print("  ✓ Data integration and quality analysis")
print("  ✓ Comprehensive documentation")
print("\nReady for submission!")