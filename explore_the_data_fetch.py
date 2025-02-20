import pandas as pd
import matplotlib.pyplot as plt

# Load the datasets 

transactions_path = "/Users/King/Documents/TRANSACTION_TAKEHOME.csv"
users_path = "/Users/King/Documents/USER_TAKEHOME.csv"
products_path = "/Users/King/Documents/PRODUCTS_TAKEHOME.csv"

df_transactions = pd.read_csv(transactions_path)
df_users = pd.read_csv(users_path)
df_products = pd.read_csv(products_path)

# Step 1: Standardize column names (strip spaces and convert to lowercase)
def standardize_column_names(df):
    df.rename(columns=lambda x: x.strip().lower(), inplace=True)

standardize_column_names(df_transactions)
standardize_column_names(df_users)
standardize_column_names(df_products)

# Step 2: Basic Overview and Initial Checks
print("\n--- Basic Information ---")
print("\nTransactions Table:")
print(df_transactions.info())
print("\nUsers Table:")
print(df_users.info())
print("\nProducts Table:")
print(df_products.info())

# Step 3: Descriptive Statistics
print("\n--- Descriptive Statistics ---")
print("\nTransactions Table:")
print(df_transactions.describe(include='all'))
print("\nUsers Table:")
print(df_users.describe(include='all'))
print("\nProducts Table:")
print(df_products.describe(include='all'))

# Step 4: Missing Values Analysis
def calculate_missing_percentage(df, table_name):
    missing_percentage = (df.isnull().sum() / len(df)) * 100
    return pd.DataFrame({
        "Table": table_name,
        "Column": df.columns,
        "Missing Percentage": missing_percentage.values
    })

transactions_missing_percentage = calculate_missing_percentage(df_transactions, "Transactions")
users_missing_percentage = calculate_missing_percentage(df_users, "Users")
products_missing_percentage = calculate_missing_percentage(df_products, "Products")

missing_percentage_summary = pd.concat([
    transactions_missing_percentage,
    users_missing_percentage,
    products_missing_percentage
], ignore_index=True)

tools.display_dataframe_to_user(name="Missing Percentage by Field", dataframe=missing_percentage_summary)

# Step 5: Duplicate Check
def check_duplicates(df, table_name):
    duplicate_count = df.duplicated().sum()
    print(f"\nDuplicate Rows in {table_name}: {duplicate_count}")
    return duplicate_count

duplicate_transactions = check_duplicates(df_transactions, "Transactions")
duplicate_users = check_duplicates(df_users, "Users")
duplicate_products = check_duplicates(df_products, "Products")

# Step 6: Unmapped IDs and Barcodes
# User ID Mismatches
unmapped_user_ids = df_transactions[~df_transactions["user_id"].isin(df_users["id"])]["user_id"].nunique()
sample_unmapped_user_ids = df_transactions[~df_transactions["user_id"].isin(df_users["id"])]["user_id"].unique()[:5]
print("\nUnmapped User IDs in Transactions:", unmapped_user_ids)
print("Sample of Unmapped User IDs:", sample_unmapped_user_ids)

# Barcode Mismatches
unmapped_barcodes = df_transactions[~df_transactions["barcode"].isin(df_products["barcode"])]["barcode"].nunique()
sample_unmapped_barcodes = df_transactions[~df_transactions["barcode"].isin(df_products["barcode"])]["barcode"].unique()[:5]
print("\nUnmapped Barcodes in Transactions:", unmapped_barcodes)
print("Sample of Unmapped Barcodes:", sample_unmapped_barcodes)

# Step 7: Field Analysis - Unique Values and Distribution
def analyze_field_distribution(df, table_name):
    print(f"\n--- Field Distribution Analysis for {table_name} ---")
    for col in df.columns:
        unique_values = df[col].nunique()
        sample_values = df[col].unique()[:5]
        print(f"Column: {col} | Unique Values: {unique_values} | Sample Values: {sample_values}")

analyze_field_distribution(df_transactions, "Transactions")
analyze_field_distribution(df_users, "Users")
analyze_field_distribution(df_products, "Products")

# Step 8: FINAL_QUANTITY and FINAL_SALE Data Quality Checks
# Convert FINAL_QUANTITY and FINAL_SALE to numeric
df_transactions["final_quantity"] = pd.to_numeric(df_transactions["final_quantity"], errors="coerce")
df_transactions["final_sale"] = pd.to_numeric(df_transactions["final_sale"], errors="coerce")

# Check for NaN after conversion (indicating non-numeric values)
non_numeric_final_quantity = df_transactions["final_quantity"].isna().sum()
non_numeric_final_sale = df_transactions["final_sale"].isna().sum()
print("\nNon-Numeric FINAL_QUANTITY Values:", non_numeric_final_quantity)
print("Non-Numeric FINAL_SALE Values:", non_numeric_final_sale)

# Step 9: Date Validations for PURCHASE_DATE and SCAN_DATE
# Convert date columns to datetime and remove timezone information for comparison
df_transactions["purchase_date"] = pd.to_datetime(df_transactions["purchase_date"], errors="coerce").dt.tz_localize(None)
df_transactions["scan_date"] = pd.to_datetime(df_transactions["scan_date"], errors="coerce").dt.tz_localize(None)

# Check for invalid date order
invalid_date_order = df_transactions[df_transactions["purchase_date"] > df_transactions["scan_date"]]
tools.display_dataframe_to_user(name="Invalid Purchase and Scan Date Order", dataframe=invalid_date_order)

# Step 10: Key Findings Summary
key_findings = """
### Key Findings from Data Exploration:

#### 1. Data Quality Issues
- **Missing Values:** Significant missing values in multiple fields across all tables.
- **Duplicates:** Detected in Transactions and Products tables.
- **FINAL_QUANTITY and FINAL_SALE:** Non-numeric values identified and need cleaning.
- **Date Columns:** Some PURCHASE_DATE values are after SCAN_DATE, indicating data entry errors.
- **Unmapped IDs and Barcodes:**
  - User IDs in Transactions not found in Users table.
  - Barcodes in Transactions not found in Products table.

#### 2. Field Analysis and Challenges
- **Inconsistent Data Types:** Some columns have inconsistent data types.
- **Ambiguous Fields:** Certain fields have unclear or ambiguous meanings.
- **Unique Value Distributions:** Some fields have high cardinality or unexpected value distributions.

#### 3. Mapping Validation
- **User ID Mapping:** Mismatches found between Users and Transactions tables.
- **Barcode Mapping:** Inconsistencies between Transactions and Products tables.

#### 4. Recommendations
- **Data Cleaning:** Address non-numeric values, date inconsistencies, and unmapped IDs.
- **Data Standardization:** Standardize data types and formats for consistency.
- **Investigate Anomalies:** Review ambiguous fields and high cardinality values for potential issues.

print(key_findings)