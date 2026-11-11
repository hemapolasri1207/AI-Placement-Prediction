import pandas as pd

# Load dataset
file_path = "placement.csv"
df = pd.read_csv(file_path)

print("\n========== DATASET INFORMATION ==========")

# Display first five records
print("\nFirst 5 records:")
print(df.head())

# Display number of rows and columns
print("\nDataset shape:")
print(df.shape)

# Display column names
print("\nColumn names:")
print(df.columns.tolist())

# Display data types
print("\nData types:")
print(df.dtypes)

# Check missing values
print("\nMissing values:")
print(df.isnull().sum())

# Check placement status distribution
if "PlacementStatus" in df.columns:
    print("\nPlacement status distribution:")
    print(df["PlacementStatus"].value_counts())

print("\nDataset inspection completed!")