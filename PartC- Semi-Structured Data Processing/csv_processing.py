"""
CSV and Excel Processing
Part C Task 2 - handling different file formats and encodings
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os

datasets = {}
problems = []

print("\n--- Task 2: CSV and Excel Processing ---\n")

# 1. Sales data
print("Reading sales_data.csv...")
sales = pd.read_csv('data/csv/sales_data.csv')
print(f"got {len(sales)} sales records")

# check for problems
print(f"columns: {list(sales.columns)}")
nulls = sales.isnull().sum()
if nulls.sum() > 0:
    print("found some null values:")
    print(nulls[nulls > 0])
    problems.append("sales has nulls")

# fix negative quantities
bad_qty = sales[sales['quantity'] < 0]
if len(bad_qty) > 0:
    print(f"fixing {len(bad_qty)} negative quantities...")
    sales['quantity'] = sales['quantity'].abs()  

# handle missing customer names
sales['customer_name'] = sales['customer_name'].fillna('Unknown')
sales['status'] = sales['status'].replace('', 'Pending') 

datasets['sales'] = sales
print("done with sales\n")

# 2. Employee data 
print("Reading employee_data.csv...")
try:
    emp = pd.read_csv('data/csv/employee_data.csv', encoding='utf-8')
except:
    print("utf-8 didn't work, trying latin-1...")
    emp = pd.read_csv('data/csv/employee_data.csv', encoding='latin-1')

print(f"got {len(emp)} employees")
print(f"departments: {emp['department'].unique()}")

# some stats
print(f"salary range: {emp['salary'].min()} to {emp['salary'].max()}")
avg_sal = emp['salary'].mean()
print(f"average: ${avg_sal:,.0f}")

datasets['employees'] = emp
print("done with employees\n")

# 3. Customer feedback
print("Reading customer_feedback.csv...")
feedback = pd.read_csv('data/csv/customer_feedback.csv')
print(f"got {len(feedback)} feedback entries")

# rating breakdown
print("\nratings:")
print(feedback['rating'].value_counts().sort_index())

# handle missing comments
feedback['comment'] = feedback['comment'].fillna('no comment')
feedback['comment'] = feedback['comment'].replace('', 'no comment')

datasets['feedback'] = feedback
print("done with feedback\n")

# 4. International data - uses semicolon instead of comma
print("Reading international_data.csv...")
intl = pd.read_csv('data/csv/international_data.csv', sep=';')  
print(f"got {len(intl)} records")
print(f"countries: {list(intl['country'].unique())}")

# quick analysis by country
country_avg = intl.groupby('country')['gdp'].mean()
print("\naverage gdp by country:")
print(country_avg)

datasets['international'] = intl
print("done with international\n")

# 5. Excel file with multiple sheets
print("Reading multi_sheet_data.xlsx...")
xl_file = pd.ExcelFile('data/csv/multi_sheet_data.xlsx')
print(f"sheets found: {xl_file.sheet_names}")

# read all sheets
for sheet_name in xl_file.sheet_names:
    sheet_df = pd.read_excel(xl_file, sheet_name=sheet_name)
    print(f"  {sheet_name}: {len(sheet_df)} rows")
    datasets[sheet_name] = sheet_df
    
    # do some quick checks
    if sheet_name == 'Inventory':
        # check which products are low on stock
        low = sheet_df[sheet_df['stock'] < sheet_df['reorder_level']]
        if len(low) > 0:
            print(f"    warning: {len(low)} products need reordering")
    
    elif sheet_name == 'Monthly_Sales':
        total = sheet_df['total_revenue'].sum()
        print(f"    total revenue: ${total:,}")

print("done with excel\n")

# data quality summary
print("\n--- Data Quality Check ---")
for name, df in datasets.items():
    nulls = df.isnull().sum().sum()
    dups = df.duplicated().sum()
    print(f"{name}: {len(df)} rows, {nulls} nulls, {dups} duplicates")


print("\n--- Combining Data ---")
# merging sales with feedback ratings by product
if 'sales' in datasets and 'feedback' in datasets:
    print("merging sales and feedback...")
    
    # get average rating per product
    ratings = feedback.groupby('product')['rating'].agg(['mean', 'count'])
    ratings.columns = ['avg_rating', 'num_reviews']
    ratings = ratings.reset_index()
    
    # merge into sales
    sales_merged = sales.merge(ratings, on='product', how='left')
    print(f"merged dataset has {len(sales_merged)} rows")
    
    # saving it
    sales_merged.to_csv('outputs/sales_with_ratings.csv', index=False)
    datasets['merged_sales'] = sales_merged
    print("saved to outputs/sales_with_ratings.csv")

# save all cleaned datasets
print("\n--- Saving Cleaned Data ---")
for name, df in datasets.items():
    if name not in ['merged_sales']:
        filename = f'outputs/{name}_clean.csv'
        df.to_csv(filename, index=False)
        print(f"saved {filename}")

# make a summary report
summary = []
for name, df in datasets.items():
    summary.append({
        'dataset': name,
        'rows': len(df),
        'cols': len(df.columns),
        'nulls': df.isnull().sum().sum()
    })

summary_df = pd.DataFrame(summary)
summary_df.to_csv('outputs/csv_processing_summary.csv', index=False)
print("\nsaved summary to csv_processing_summary.csv")

# write a report file
report_text = f"""CSV and Excel Processing Report
Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}

Files processed: {len(datasets)}
Total records: {sum([len(d) for d in datasets.values()])}

Problems found:
"""
for p in problems:
    report_text += f"- {p}\n"

report_text += f"""
Datasets created:
"""
for name in datasets.keys():
    report_text += f"- {name}\n"

with open('outputs/csv_report.txt', 'w') as f:
    f.write(report_text)

print("\nAll done! Check outputs folder for results.")
print(f"Processed {len(datasets)} datasets successfully.")