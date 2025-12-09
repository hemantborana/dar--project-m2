"""
Sample Data Generator for CSV and Excel Processing
Creates realistic test datasets with various issues to handle
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os


os.makedirs('data/csv', exist_ok=True)

print("Generating sample datasets...")

# Dataset 1: Sales data with missing values and encoding issues
print("\n1. Creating sales_data.csv...")
dates = pd.date_range(start='2023-01-01', end='2024-12-31', freq='D')
products = ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Headphones', 'Webcam']
regions = ['North', 'South', 'East', 'West']
sales_data = []

for i in range(500):
    sale = {
        'order_id': f'ORD{i+1:04d}',
        'date': random.choice(dates).strftime('%Y-%m-%d'),
        'product': random.choice(products),
        'quantity': random.randint(1, 10),
        'price': round(random.uniform(10, 1000), 2),
        'region': random.choice(regions),
        'customer_name': random.choice(['John Smith', 'María García', 'André Silva', 'François Müller', None]),  # some nulls
        'status': random.choice(['Completed', 'Pending', 'Cancelled', ''])  # empty strings
    }
    # calculate revenue
    sale['revenue'] = round(sale['quantity'] * sale['price'], 2)
    sales_data.append(sale)

sales_df = pd.DataFrame(sales_data)
# add some intentional issues
sales_df.loc[10:20, 'customer_name'] = None  # missing values
sales_df.loc[30:35, 'quantity'] = -1  # data quality issue
sales_df.to_csv('data/csv/sales_data.csv', index=False, encoding='utf-8')
print(f"   Created with {len(sales_df)} records")

# Dataset 2: Employee data with different schema and encoding
print("\n2. Creating employee_data.csv...")
departments = ['HR', 'IT', 'Sales', 'Marketing', 'Finance']
emp_data = []

for i in range(200):
    emp = {
        'emp_id': f'E{i+1:03d}',
        'name': random.choice(['Alice', 'Bob', 'José', 'François', 'Müller']),
        'department': random.choice(departments),
        'salary': random.randint(30000, 150000),
        'hire_date': (datetime.now() - timedelta(days=random.randint(100, 2000))).strftime('%Y-%m-%d'),
        'email': f'emp{i+1}@company.com',
        'manager_id': f'E{random.randint(1, 50):03d}' if i > 50 else None
    }
    emp_data.append(emp)

emp_df = pd.DataFrame(emp_data)
emp_df.to_csv('data/csv/employee_data.csv', index=False, encoding='latin-1')
print(f"   Created with {len(emp_df)} records (latin-1 encoding)")

# Dataset 3: Customer feedback with special characters
print("\n3. Creating customer_feedback.csv...")
feedback_data = []
ratings = [1, 2, 3, 4, 5]
comments = [
    'Great product!',
    'Not bad, could be better',
    'Terrible experience',
    'Awesome service!',
    None,  # missing comment
    '',
    'Product arrived damaged',
    'Very satisfied with purchase'
]

for i in range(150):
    feedback = {
        'feedback_id': i+1,
        'customer_id': f'CUST{random.randint(1, 100):04d}',
        'product': random.choice(products),
        'rating': random.choice(ratings),
        'comment': random.choice(comments),
        'date': (datetime.now() - timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d'),
        'helpful_count': random.randint(0, 50)
    }
    feedback_data.append(feedback)

feedback_df = pd.DataFrame(feedback_data)
feedback_df.to_csv('data/csv/customer_feedback.csv', index=False)
print(f"   Created with {len(feedback_df)} records")

# Dataset 4: Excel file with multiple sheets
print("\n4. Creating multi_sheet_data.xlsx...")

# Sheet 1: Product inventory
inventory = {
    'product_id': [f'P{i:03d}' for i in range(1, 51)],
    'product_name': [random.choice(products) for _ in range(50)],
    'category': [random.choice(['Electronics', 'Accessories', 'Peripherals']) for _ in range(50)],
    'stock': [random.randint(0, 500) for _ in range(50)],
    'reorder_level': [random.randint(10, 50) for _ in range(50)],
    'supplier': [f'Supplier_{random.randint(1, 5)}' for _ in range(50)]
}
inventory_df = pd.DataFrame(inventory)

# Sheet 2: Monthly sales summary
months = pd.date_range(start='2024-01-01', periods=12, freq='MS')
monthly_sales = {
    'month': [m.strftime('%Y-%m') for m in months],
    'total_revenue': [random.randint(50000, 200000) for _ in range(12)],
    'total_orders': [random.randint(100, 500) for _ in range(12)],
    'avg_order_value': [round(random.uniform(100, 500), 2) for _ in range(12)],
    'returns': [random.randint(5, 50) for _ in range(12)]
}
monthly_df = pd.DataFrame(monthly_sales)

# Sheet 3: Regional performance
regional_perf = {
    'region': regions * 4,  # 4 quarters
    'quarter': ['Q1']*4 + ['Q2']*4 + ['Q3']*4 + ['Q4']*4,
    'revenue': [random.randint(20000, 100000) for _ in range(16)],
    'target': [random.randint(25000, 90000) for _ in range(16)],
    'achievement_pct': [round(random.uniform(80, 120), 1) for _ in range(16)]
}
regional_df = pd.DataFrame(regional_perf)

# write to excel with multiple sheets
with pd.ExcelWriter('data/csv/multi_sheet_data.xlsx', engine='openpyxl') as writer:
    inventory_df.to_excel(writer, sheet_name='Inventory', index=False)
    monthly_df.to_excel(writer, sheet_name='Monthly_Sales', index=False)
    regional_df.to_excel(writer, sheet_name='Regional_Performance', index=False)

print("   Created with 3 sheets: Inventory, Monthly_Sales, Regional_Performance")

# Dataset 5: CSV with different delimiter 
print("\n5. Creating international_data.csv (semicolon delimiter)...")
intl_data = {
    'country': ['USA', 'UK', 'Germany', 'France', 'Spain', 'Italy'] * 20,
    'year': [2024] * 120,
    'gdp': [random.randint(1000, 20000) for _ in range(120)],
    'population': [random.randint(10, 350) for _ in range(120)],
    'currency': ['USD', 'GBP', 'EUR', 'EUR', 'EUR', 'EUR'] * 20
}
intl_df = pd.DataFrame(intl_data)
intl_df.to_csv('data/csv/international_data.csv', index=False, sep=';')
print(f"   Created with {len(intl_df)} records (semicolon delimiter)")

print("\n" + "="*60)
print("Sample data generation complete!")
print("="*60)
print("\nFiles created:")
print("1. data/csv/sales_data.csv (500 records, UTF-8)")
print("2. data/csv/employee_data.csv (200 records, Latin-1 encoding)")
print("3. data/csv/customer_feedback.csv (150 records)")
print("4. data/csv/multi_sheet_data.xlsx (3 sheets)")
print("5. data/csv/international_data.csv (120 records, semicolon delimiter)")
print("\nReady for csv_processing.py!")