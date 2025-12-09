"""
JSON Data Processing - Part C Task 1
Author: Hemant Borana
Date: Dec 2024

This script handles JSON data from multiple REST APIs
- JSONPlaceholder (users, posts)  
- REST Countries API
"""

import requests
import pandas as pd
import json
from datetime import datetime
import os

# setup output folders
if not os.path.exists('outputs'):
    os.makedirs('outputs')
if not os.path.exists('data/json'):
    os.makedirs('data/json')

# keep track of errors
errors_list = []
all_data = {}

def get_json_from_api(url, api_name):
    """fetch json data from api"""
    print(f"\nFetching {api_name}...")
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        
        # save raw json too
        with open(f'data/json/{api_name}_raw.json', 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"Got {len(data) if isinstance(data, list) else 1} records from {api_name}")
        return data
    except Exception as e:
        error = f"Failed to get {api_name}: {str(e)}"
        errors_list.append(error)
        print(error)
        return None

def flatten_dict(d, parent='', sep='_'):
    """flatten nested dictionaries - useful for address, geo, company etc"""
    result = {}
    for k, v in d.items():
        new_key = f"{parent}{sep}{k}" if parent else k
        if isinstance(v, dict):
            result.update(flatten_dict(v, new_key, sep))
        elif isinstance(v, list):
            result[new_key] = str(v)  # convert lists to strings
        else:
            result[new_key] = v
    return result

# Task 1: Get users data (has nested address and company info)
print("\n--- Processing Users Data ---")
users_url = "https://jsonplaceholder.typicode.com/users"
users_data = get_json_from_api(users_url, "users")

if users_data:
    # flatten each user record since address/company are nested
    users_flat = []
    for user in users_data:
        flat = flatten_dict(user)
        users_flat.append(flat)
    
    users_df = pd.DataFrame(users_flat)
    users_df.fillna('N/A', inplace=True)  # handle missing values
    
    print(f"Created dataframe with {len(users_df)} rows, {len(users_df.columns)} columns")
    print(f"Columns: {list(users_df.columns[:5])}...")  # show first 5 cols
    
    # save it
    users_df.to_csv('outputs/users_processed.csv', index=False)
    users_df.to_excel('outputs/users_processed.xlsx', index=False)
    all_data['users'] = users_df
    print("Saved users data")

# Task 2: Get posts data (simpler structure)
print("\n--- Processing Posts Data ---")
posts_url = "https://jsonplaceholder.typicode.com/posts"
posts_data = get_json_from_api(posts_url, "posts")

if posts_data:
    posts_df = pd.DataFrame(posts_data)
    
    # add some extra fields
    posts_df['title_length'] = posts_df['title'].str.len()
    posts_df['body_length'] = posts_df['body'].str.len()
    posts_df['processed_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # check for nulls
    null_count = posts_df.isnull().sum().sum()
    print(f"Found {null_count} null values")
    posts_df.fillna('N/A', inplace=True)
    
    print(f"Posts by user: {posts_df.groupby('userId').size().head()}")
    
    posts_df.to_csv('outputs/posts_processed.csv', index=False)
    all_data['posts'] = posts_df
    print("Saved posts data")

# Task 3: Get countries data (very nested - name, currencies, languages etc)
print("\n--- Processing Countries Data ---")
countries_url = "https://restcountries.com/v3.1/all?fields=name,capital,region,subregion,population,area,languages,currencies,independent"
countries_data = get_json_from_api(countries_url, "countries")

if countries_data:
    # manually extract fields because its too nested
    countries = []
    for c in countries_data[:50]:  # just first 50 to keep it fast
        try:
            # safely get nested values
            name = c.get('name', {}).get('common', 'Unknown')
            capital = c.get('capital', ['N/A'])
            capital = capital[0] if capital else 'N/A'
            
            # languages come as dict - join them
            langs = c.get('languages', {})
            langs_str = ', '.join(langs.values()) if langs else 'N/A'
            
            # same for currencies
            curr = c.get('currencies', {})
            curr_str = ', '.join(curr.keys()) if curr else 'N/A'
            
            country = {
                'name': name,
                'official': c.get('name', {}).get('official', 'N/A'),
                'capital': capital,
                'region': c.get('region', 'N/A'),
                'subregion': c.get('subregion', 'N/A'),
                'population': c.get('population', 0),
                'area': c.get('area', 0),
                'languages': langs_str,
                'currencies': curr_str,
                'independent': c.get('independent', False)
            }
            countries.append(country)
        except:
            continue  # skip if any error
    
    countries_df = pd.DataFrame(countries)
    print(f"Processed {len(countries_df)} countries")
    print(f"Regions found: {countries_df['region'].unique()}")
    print(f"Total population: {countries_df['population'].sum():,}")
    
    countries_df.to_csv('outputs/countries_processed.csv', index=False)
    countries_df.to_excel('outputs/countries_processed.xlsx', index=False)
    all_data['countries'] = countries_df
    print("Saved countries data")

# create a summary of all datasets
print("\n--- Creating Summary ---")
summary_data = []
for name, df in all_data.items():
    summary_data.append({
        'dataset': name,
        'records': len(df),
        'columns': len(df.columns),
        'memory_kb': round(df.memory_usage(deep=True).sum() / 1024, 2)
    })

summary_df = pd.DataFrame(summary_data)
summary_df.to_csv('outputs/json_summary.csv', index=False)
print("\nSummary:")
print(summary_df)

# write a simple report
report = f"""JSON Processing Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Datasets Processed: {len(all_data)}
Total Errors: {len(errors_list)}

Output Files:
- users_processed.csv ({len(all_data.get('users', []))} records)
- posts_processed.csv ({len(all_data.get('posts', []))} records)  
- countries_processed.csv ({len(all_data.get('countries', []))} records)
- json_summary.csv

"""

if errors_list:
    report += "\nErrors:\n"
    for e in errors_list:
        report += f"- {e}\n"

with open('outputs/json_report.txt', 'w') as f:
    f.write(report)

print("\n" + report)
print("Report Generated.")