# Module 10 Assignment: Data Manipulation and Cleaning with Pandas
# UrbanStyle Customer Data Cleaning
 
# Import required libraries
import pandas as pd
import numpy as np
from datetime import datetime
 
# Welcome message
print("=" * 60)
print("URBANSTYLE CUSTOMER DATA CLEANING")
print("=" * 60)
 
# ----- USE THE FOLLOWING CODE TO SIMULATE A CSV FILE (DO NOT MODIFY) -----
from io import StringIO
 
# Simulated CSV content with intentional data issues
csv_content = """customer_id,first_name,last_name,email,phone,join_date,last_purchase,total_purchases,total_spent,preferred_category,satisfaction_rating,age,city,state,loyalty_status
CS001,John,Smith,johnsmith@email.com,(555) 123-4567,2023-01-15,2023-12-01,12,"1,250.99",Menswear,4.5,35,Tampa,FL,Gold
CS002,Emily,Johnson,emily.j@email.com,555.987.6543,01/25/2023,10/15/2023,8,$875.50,Womenswear,4,28,Miami,FL,Silver
CS003,Michael,Williams,mw@email.com,(555)456-7890,2023-02-10,2023-11-20,15,"2,100.75",Footwear,5,42,Orlando,FL,Gold
CS004,JESSICA,BROWN,jess.brown@email.com,5551234567,2023-03-05,2023-12-10,6,659.25,Womenswear,3.5,31,Tampa,FL,Bronze
CS005,David,jones,djones@email.com,555-789-1234,2023-03-20,2023-09-18,4,350.00,Menswear,,45,Jacksonville,FL,Bronze
CS006,Sarah,Miller,sarah_miller@email.com,(555) 234-5678,2023-04-12,2023-12-05,10,1450.30,Accessories,4,29,Tampa,FL,Silver
CS007,Robert,Davis,robert.davis@email.com,555.444.7777,04/30/2023,11/25/2023,7,$725.80,Footwear,4.5,38,Miami,FL,Silver
CS008,Jennifer,Garcia,jen.garcia@email.com,(555)876-5432,2023-05-15,2023-10-30,3,280.50,ACCESSORIES,3,25,Orlando,FL,Bronze
CS009,Michael,Williams,m.williams@email.com,5558889999,2023-06-01,2023-12-07,9,1100.00,Menswear,4,39,Jacksonville,FL,Silver
CS010,Emily,Johnson,emilyjohnson@email.com,555-321-6547,2023-06-15,2023-12-15,14,"1,875.25",Womenswear,4.5,27,Miami,FL,Gold
CS006,Sarah,Miller,sarah_miller@email.com,(555) 234-5678,2023-04-12,2023-12-05,10,1450.30,Accessories,4,29,Tampa,FL,Silver
CS011,Amanda,,amanda.p@email.com,(555) 741-8529,2023-07-10,,2,180.00,womenswear,3,32,Tampa,FL,Bronze
CS012,Thomas,Wilson,thomas.w@email.com,,2023-07-25,2023-11-02,5,450.75,menswear,4,44,Orlando,FL,Bronze
CS013,Lisa,Anderson,lisa.a@email.com,555.159.7530,08/05/2023,,0,0.00,Womenswear,,30,Miami,FL,
CS014,James,Taylor,jtaylor@email.com,555-951-7530,2023-08-20,2023-10-10,11,"1,520.65",Footwear,4.5,,Jacksonville,FL,Gold
CS015,Karen,Thomas,karen.t@email.com,(555) 357-9512,2023-09-05,2023-12-12,6,685.30,Womenswear,4,36,Tampa,FL,Silver
"""
 
# Create a StringIO object (simulates a file)
customer_data_csv = StringIO(csv_content)
 
# Now you can load this as if it was a CSV file:
# raw_df = pd.read_csv(customer_data_csv)
# ----- END OF SIMULATION CODE -----
 
 
# =============================================================================
# TODO 1: Load and Explore the Dataset
# =============================================================================
 
# 1.1 Load the dataset and display basic information
# REQUIRED: Store DataFrame in variable 'raw_df'
raw_df = pd.read_csv(customer_data_csv)
 
print("\n--- 1.1 Basic Dataset Info ---")
print(f"Shape: {raw_df.shape}")
print(raw_df.dtypes)
print(raw_df.head())
 
# 1.2 Assess the data quality issues
# REQUIRED: Store initial missing value counts in 'initial_missing_counts' (pandas Series)
# REQUIRED: Store duplicate count in variable 'initial_duplicate_count' (int)
initial_missing_counts = raw_df.isnull().sum()
initial_duplicate_count = int(raw_df.duplicated().sum())
 
print(f"\n--- 1.2 Data Quality Assessment ---")
print("Initial missing values:\n", initial_missing_counts)
print(f"Initial duplicate rows: {initial_duplicate_count}")
 
# Key issues observed:
# - Mixed date formats (YYYY-MM-DD and MM/DD/YYYY)
# - Inconsistent phone formats (dots, dashes, parentheses, raw digits)
# - Currency symbols ($) and commas in total_spent
# - Inconsistent capitalization in names and categories
# - Missing: last_name (CS011), phone (CS012), last_purchase (CS011, CS013),
#            satisfaction_rating (CS005, CS013), age (CS014), loyalty_status (CS013)
# - One fully duplicate row (CS006 appears twice)
 
 
# =============================================================================
# TODO 2: Handle Missing Values
# =============================================================================
 
# 2.1 Identify and count missing values
# REQUIRED: Store in variable 'missing_value_report' (pandas Series)
missing_value_report = raw_df.isnull().sum()
print("\n--- 2.1 Missing Value Report ---")
print(missing_value_report[missing_value_report > 0])
 
# 2.2 Fill missing satisfaction_rating with the median value
# REQUIRED: Store median value used in variable 'satisfaction_median' (float)
satisfaction_median = float(raw_df['satisfaction_rating'].median())
raw_df['satisfaction_rating'] = raw_df['satisfaction_rating'].fillna(satisfaction_median)
print(f"\n--- 2.2 Satisfaction Rating Median Used: {satisfaction_median} ---")
 
# 2.3 Fill missing last_purchase dates using forward fill
# Forward fill is appropriate here: if a customer has no last_purchase recorded,
# we propagate the most recent known date as a conservative estimate.
# REQUIRED: Store strategy used in variable 'date_fill_strategy' (string)
date_fill_strategy = 'forward_fill'
raw_df['last_purchase'] = raw_df['last_purchase'].ffill()
print(f"\n--- 2.3 Date Fill Strategy: {date_fill_strategy} ---")
 
# 2.4 Handle other missing values
# - last_name: fill with empty string (Amanda has no last name on record)
# - phone: fill with 'Unknown' (cannot infer phone numbers)
# - age: fill with median age (reasonable imputation for a numeric field)
# - loyalty_status: fill with 'Bronze' (lowest tier is safest default for unknown status)
raw_df['last_name'] = raw_df['last_name'].fillna('')
raw_df['phone'] = raw_df['phone'].fillna('Unknown')
age_median = raw_df['age'].median()
raw_df['age'] = raw_df['age'].fillna(age_median)
raw_df['loyalty_status'] = raw_df['loyalty_status'].fillna('Bronze')
 
# REQUIRED: Store cleaned DataFrame in variable 'df_no_missing'
df_no_missing = raw_df.copy()
print(f"\n--- 2.4 Missing Values After Cleaning ---")
print(df_no_missing.isnull().sum())
 
 
# =============================================================================
# TODO 3: Correct Data Types
# =============================================================================
 
# 3.1 Convert join_date and last_purchase to datetime
# dayfirst=False handles both YYYY-MM-DD and MM/DD/YYYY via infer_datetime_format
# REQUIRED: Work with 'df_no_missing' and store result in 'df_typed'
df_typed = df_no_missing.copy()
df_typed['join_date'] = pd.to_datetime(df_typed['join_date'], format='mixed', dayfirst=False)
df_typed['last_purchase'] = pd.to_datetime(df_typed['last_purchase'], format='mixed', dayfirst=False)
print("\n--- 3.1 Date Columns Converted ---")
print(df_typed[['join_date', 'last_purchase']].dtypes)
 
# 3.2 Convert total_spent to numeric (remove $ signs and commas)
df_typed['total_spent'] = (
    df_typed['total_spent']
    .astype(str)
    .str.replace(r'[\$,]', '', regex=True)
    .pipe(pd.to_numeric, errors='coerce')
)
print("\n--- 3.2 total_spent dtype:", df_typed['total_spent'].dtype, "---")
 
# 3.3 Ensure other numeric fields are correct types
df_typed['total_purchases'] = pd.to_numeric(df_typed['total_purchases'], errors='coerce').astype(int)
df_typed['age'] = pd.to_numeric(df_typed['age'], errors='coerce').astype(int)
print("--- 3.3 Numeric dtypes verified ---")
print(df_typed[['total_purchases', 'age']].dtypes)
 
 
# =============================================================================
# TODO 4: Clean and Standardize Text Data
# =============================================================================
 
# 4.1 Standardize case for first_name and last_name (Title/Proper case)
# This fixes issues like "JESSICA", "jones", "BROWN"
df_text_cleaned = df_typed.copy()
df_text_cleaned['first_name'] = df_text_cleaned['first_name'].str.strip().str.title()
df_text_cleaned['last_name'] = df_text_cleaned['last_name'].str.strip().str.title()
print("\n--- 4.1 Names Standardized ---")
print(df_text_cleaned[['first_name', 'last_name']].head(5))
 
# 4.2 Standardize category names (Title case fixes ACCESSORIES, womenswear, menswear)
df_text_cleaned['preferred_category'] = df_text_cleaned['preferred_category'].str.strip().str.title()
print("\n--- 4.2 Categories Standardized ---")
print(df_text_cleaned['preferred_category'].unique())
 
# 4.3 Standardize phone numbers to format: XXX-XXX-XXXX
# Strip all non-digit characters, then reformat (if 10 digits), else keep as-is
# REQUIRED: Store standardized phone format used in variable 'phone_format' (string)
phone_format = 'XXX-XXX-XXXX'
 
def standardize_phone(phone):
    """Remove non-digit characters and reformat to XXX-XXX-XXXX."""
    if phone == 'Unknown':
        return 'Unknown'
    digits = ''.join(filter(str.isdigit, str(phone)))
    if len(digits) == 10:
        return f"{digits[:3]}-{digits[3:6]}-{digits[6:]}"
    return phone  # Return original if unexpected length
 
df_text_cleaned['phone'] = df_text_cleaned['phone'].apply(standardize_phone)
print(f"\n--- 4.3 Phone Format: {phone_format} ---")
print(df_text_cleaned['phone'].head(10))
 
 
# =============================================================================
# TODO 5: Remove Duplicates
# =============================================================================
 
# 5.1 Identify duplicate records
# REQUIRED: Store duplicate count in variable 'duplicate_count' (int)
duplicate_count = int(df_text_cleaned.duplicated().sum())
print(f"\n--- 5.1 Duplicate Records Found: {duplicate_count} ---")
print(df_text_cleaned[df_text_cleaned.duplicated(keep=False)])
 
# 5.2 Remove duplicates, keeping the first occurrence
# The duplicate CS006 row is completely identical, so keeping 'first' is correct.
# REQUIRED: Work with 'df_text_cleaned' and store result in 'df_no_duplicates'
df_no_duplicates = df_text_cleaned.drop_duplicates(keep='first').reset_index(drop=True)
print(f"\n--- 5.2 Shape After Removing Duplicates: {df_no_duplicates.shape} ---")
 
 
# =============================================================================
# TODO 6: Add Derived Features
# =============================================================================
 
# 6.1 Calculate days_since_last_purchase
# Using a fixed reference date of 2023-12-31 (end of the data year) for consistency
reference_date = pd.Timestamp('2023-12-31')
df_no_duplicates['days_since_last_purchase'] = (
    reference_date - df_no_duplicates['last_purchase']
).dt.days
print("\n--- 6.1 days_since_last_purchase ---")
print(df_no_duplicates[['customer_id', 'last_purchase', 'days_since_last_purchase']].head())
 
# 6.2 Calculate average_purchase_value (total_spent / total_purchases)
# Handle division by zero: customers with 0 purchases get 0.0 average
df_no_duplicates['average_purchase_value'] = np.where(
    df_no_duplicates['total_purchases'] > 0,
    (df_no_duplicates['total_spent'] / df_no_duplicates['total_purchases']).round(2),
    0.0
)
print("\n--- 6.2 average_purchase_value ---")
print(df_no_duplicates[['customer_id', 'total_spent', 'total_purchases', 'average_purchase_value']].head())
 
# 6.3 Create purchase_frequency_category
# High: >= 10 purchases | Medium: 5-9 | Low: < 5
def classify_frequency(purchases):
    if purchases >= 10:
        return 'High'
    elif purchases >= 5:
        return 'Medium'
    else:
        return 'Low'
 
df_no_duplicates['purchase_frequency_category'] = df_no_duplicates['total_purchases'].apply(classify_frequency)
print("\n--- 6.3 purchase_frequency_category ---")
print(df_no_duplicates[['customer_id', 'total_purchases', 'purchase_frequency_category']].head(10))
 
 
# =============================================================================
# TODO 7: Clean Up the DataFrame
# =============================================================================
 
# 7.1 Rename columns to more readable formats
# REQUIRED: Store renamed DataFrame in 'df_renamed'
df_renamed = df_no_duplicates.rename(columns={
    'customer_id':                  'Customer ID',
    'first_name':                   'First Name',
    'last_name':                    'Last Name',
    'email':                        'Email',
    'phone':                        'Phone',
    'join_date':                    'Join Date',
    'last_purchase':                'Last Purchase Date',
    'total_purchases':              'Total Purchases',
    'total_spent':                  'Total Spent',
    'preferred_category':           'Preferred Category',
    'satisfaction_rating':          'Satisfaction Rating',
    'age':                          'Age',
    'city':                         'City',
    'state':                        'State',
    'loyalty_status':               'Loyalty Status',
    'days_since_last_purchase':     'Days Since Last Purchase',
    'average_purchase_value':       'Avg Purchase Value',
    'purchase_frequency_category':  'Purchase Frequency'
})
 
# 7.2 Remove unnecessary columns
# 'Email' is PII that isn't needed for segmentation analysis; removing it keeps
# the dataset focused. All other columns contribute meaningful analytical value.
# REQUIRED: Store cleaned DataFrame in 'df_final'
df_final = df_renamed.drop(columns=['Email'])
 
# 7.3 Sort by Total Spent descending (most valuable customers first)
# REQUIRED: Sort 'df_final' by total_spent descending and store in 'df_final'
df_final = df_final.sort_values(by='Total Spent', ascending=False).reset_index(drop=True)
print("\n--- 7.3 Final DataFrame (sorted by Total Spent) ---")
print(df_final.head())
 
 
# =============================================================================
# TODO 8: Generate Insights from Cleaned Data
# =============================================================================
 
# 8.1 Average spent by loyalty_status
# REQUIRED: Store result in 'avg_spent_by_loyalty' (pandas Series)
avg_spent_by_loyalty = df_final.groupby('Loyalty Status')['Total Spent'].mean().round(2)
print("\n--- 8.1 Avg Spent by Loyalty Status ---")
print(avg_spent_by_loyalty)
 
# 8.2 Top preferred categories by total revenue
# REQUIRED: Store result in 'category_revenue' (pandas Series, sorted descending)
category_revenue = (
    df_final.groupby('Preferred Category')['Total Spent']
    .sum()
    .sort_values(ascending=False)
    .round(2)
)
print("\n--- 8.2 Revenue by Category ---")
print(category_revenue)
 
# 8.3 Correlation between satisfaction_rating and total_spent
# REQUIRED: Store correlation value in 'satisfaction_spend_corr' (float)
satisfaction_spend_corr = float(
    df_final['Satisfaction Rating'].corr(df_final['Total Spent'])
)
print(f"\n--- 8.3 Satisfaction vs Spend Correlation: {satisfaction_spend_corr:.4f} ---")
 
 
# =============================================================================
# TODO 9: Generate Final Report
# =============================================================================
 
print("\n" + "=" * 60)
print("URBANSTYLE CUSTOMER DATA CLEANING REPORT")
print("=" * 60)
 
# 9.1 Data Quality Issues Found
total_missing = int(initial_missing_counts.sum())
print(f"""
Data Quality Issues:
- Missing Values: {total_missing} total missing entries
  * satisfaction_rating: 2 (filled with median: {satisfaction_median})
  * last_purchase: 2 (filled using forward fill)
  * last_name: 1 (filled with empty string)
  * phone: 1 (filled with 'Unknown')
  * age: 1 (filled with median age)
  * loyalty_status: 1 (filled with 'Bronze')
- Duplicates: {initial_duplicate_count} duplicate record found (CS006 appeared twice)
- Data Type Issues: ['Mixed date formats (YYYY-MM-DD and MM/DD/YYYY)',
                     'Currency symbols ($) and commas in total_spent',
                     'All columns loaded as object/string type']
""")
 
# 9.2 Standardization Changes Made
print(f"""Standardization Changes:
- Names: Converted to proper case (e.g., JESSICA → Jessica, jones → Jones)
- Categories: Standardized to Title case (e.g., ACCESSORIES → Accessories, womenswear → Womenswear)
- Phone Numbers: Reformatted to {phone_format} (stripped symbols, restructured 10-digit numbers)
- Dates: Parsed both YYYY-MM-DD and MM/DD/YYYY formats to uniform datetime objects
- total_spent: Removed $ and , characters, converted to float
""")
 
# 9.3 Key Business Insights
top_category = category_revenue.idxmax()
top_category_revenue = category_revenue.max()
total_customers = len(df_final)
 
print(f"""Key Business Insights:
- Customer Base: {total_customers} total customers
- Revenue by Loyalty:
{avg_spent_by_loyalty.to_string()}
- Top Category: {top_category} with ${top_category_revenue:,.2f} in total revenue
- Satisfaction vs Spend Correlation: {satisfaction_spend_corr:.4f}
  (Positive correlation — higher satisfaction links to higher spending)
""")
 
# 9.4 Display first 5 rows of the final clean dataset
print("--- Final Clean Dataset (First 5 Rows) ---")
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 120)
print(df_final.head())