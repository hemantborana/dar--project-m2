"""
XML Data Processing - Part C Task 3
Hemant Borana
Processing different XML structures, attributes, namespaces
"""

import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime
import os

results = {}

print("\n--- XML Processing Task ---\n")

# 1. Parse books.xml 
print("Processing books.xml...")
tree = ET.parse('data/xml/books.xml')
root = tree.getroot()

books = []
for book in root.findall('book'):
    # get attributes
    book_id = book.get('id')
    category = book.get('category')
    
    # get text from child elements
    book_data = {
        'id': book_id,
        'category': category,
        'author': book.find('author').text,
        'title': book.find('title').text,
        'price': float(book.find('price').text),
        'currency': book.find('price').get('currency'), 
        'publish_date': book.find('publish_date').text,
        'description': book.find('description').text
    }
    books.append(book_data)

books_df = pd.DataFrame(books)
print(f"found {len(books_df)} books")
print(f"categories: {books_df['category'].unique()}")

# quick analysis
avg_price = books_df['price'].mean()
print(f"average price: ${avg_price:.2f}")

results['books'] = books_df
print("done\n")

# 2. Parse employees.xml 
print("Processing employees.xml...")
tree = ET.parse('data/xml/employees.xml')
root = tree.getroot()

employees = []
for dept in root.findall('department'):
    dept_name = dept.get('name')
    
    for emp in dept.findall('employee'):
        emp_id = emp.get('id')
        
        # get nested contact info
        contact = emp.find('contact')
        email = contact.find('email').text if contact is not None else 'N/A'
        phone = contact.find('phone').text if contact is not None else 'N/A'
        
        # get multiple skills 
        skills_elem = emp.find('skills')
        skills = []
        if skills_elem is not None:
            for skill in skills_elem.findall('skill'):
                skills.append(skill.text)
        skills_str = ', '.join(skills)
        
        # get name 
        name_elem = emp.find('n')
        if name_elem is None:
            name_elem = emp.find('name')
        name = name_elem.text if name_elem is not None else 'Unknown'
        
        emp_data = {
            'id': emp_id,
            'department': dept_name,
            'name': name,
            'position': emp.find('position').text,
            'salary': int(emp.find('salary').text),
            'email': email,
            'phone': phone,
            'skills': skills_str
        }
        employees.append(emp_data)

emp_df = pd.DataFrame(employees)
print(f"found {len(emp_df)} employees")

# group by department
dept_count = emp_df.groupby('department').size()
print("by department:")
print(dept_count)

# salary stats
print(f"salary range: ${emp_df['salary'].min():,} - ${emp_df['salary'].max():,}")

results['employees'] = emp_df
print("done\n")

# 3. Parse products.xml (has namespaces - bit tricky)
print("Processing products.xml...")
tree = ET.parse('data/xml/products.xml')
root = tree.getroot()

# namespaces make it harder - need to define them
namespaces = {
    'inv': 'http://example.com/inventory',
    'prod': 'http://example.com/products'
}

products = []
for product in root.findall('prod:product', namespaces):
    # attributes with namespace
    prod_id = product.get('{http://example.com/inventory}id')
    in_stock = product.get('{http://example.com/inventory}inStock')
    
    # elements with namespace - need to use full path
    prod_data = {
        'id': prod_id,
        'name': product.find('prod:name', namespaces).text,
        'category': product.find('prod:category', namespaces).text,
        'price': float(product.find('prod:price', namespaces).text),
        'stock': int(product.find('prod:stock', namespaces).text),
        'supplier': product.find('prod:supplier', namespaces).text,
        'in_stock': in_stock == 'true'
    }
    products.append(prod_data)

prod_df = pd.DataFrame(products)
print(f"found {len(prod_df)} products")

# check stock status
out_of_stock = prod_df[prod_df['in_stock'] == False]
print(f"out of stock items: {len(out_of_stock)}")
if len(out_of_stock) > 0:
    print(f"  {list(out_of_stock['name'])}")

results['products'] = prod_df
print("done\n")

# 4. Parse news_feed.xml (RSS format)
print("Processing news_feed.xml (RSS)...")
tree = ET.parse('data/xml/news_feed.xml')
root = tree.getroot()

# RSS has channel > item structure
channel = root.find('channel')
news_items = []

for item in channel.findall('item'):
    news = {
        'title': item.find('title').text,
        'link': item.find('link').text,
        'pub_date': item.find('pubDate').text,
        'description': item.find('description').text,
        'category': item.find('category').text
    }
    news_items.append(news)

news_df = pd.DataFrame(news_items)
print(f"found {len(news_df)} news items")

# categories breakdown
cats = news_df['category'].value_counts()
print("by category:")
print(cats)

results['news'] = news_df
print("done\n")

# convert all to structured format (CSV)
print("--- Saving to CSV ---")
for name, df in results.items():
    filename = f'outputs/{name}_from_xml.csv'
    df.to_csv(filename, index=False)
    print(f"saved {filename}")

# create summary
print("\n--- XML Processing Summary ---")
summary = []
for name, df in results.items():
    summary.append({
        'source': name,
        'records': len(df),
        'columns': len(df.columns)
    })

summary_df = pd.DataFrame(summary)
print(summary_df.to_string(index=False))
summary_df.to_csv('outputs/xml_processing_summary.csv', index=False)

# write report
report = f"""XML Processing Report
Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}

XML Files Processed: {len(results)}

Details:
- books.xml: {len(results['books'])} records (simple structure with attributes)
- employees.xml: {len(results['employees'])} records (nested structure)
- products.xml: {len(results['products'])} records (with namespaces)
- news_feed.xml: {len(results['news'])} records (RSS format)

Output Files Created:
"""

for name in results.keys():
    report += f"- outputs/{name}_from_xml.csv\n"

report += "\nXPath expressions used for extraction demonstrated.\n"
report += "Namespace handling implemented for products.xml\n"

with open('outputs/xml_report.txt', 'w') as f:
    f.write(report)

print("\nReport saved to xml_report.txt")
print("\nAll XML processing complete!")
print(f"Total records extracted: {sum([len(d) for d in results.values()])}")