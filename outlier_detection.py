# -------------------------------
# Outlier Detection Script
# -------------------------------

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------------
# Step 1: Load dataset
# -------------------------------
df = pd.read_excel(r"C:\Users\TWEENCY MARVANIYA\OneDrive\Desktop\Agri Crop\unclean_crop_yield.xlsx")

# Strip any extra spaces in column names
df.columns = df.columns.str.strip()

# Columns to check (exact names from your dataset)
columns_of_interest = ['Area (ha)', 'Production(MT)', 'Annual_Rainfall (mm)',
                       'Fertilizer (kg)', 'Pesticide (kg)', 'Yield (t/ha)']

# -------------------------------
# Step 2: Summary statistics
# -------------------------------
print("Summary statistics:\n")
print(df[columns_of_interest].describe())

# -------------------------------
# Step 3: Detect outliers using IQR
# -------------------------------
outliers_dict = {}  # Store outlier indices for each column
for col in columns_of_interest:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
    outliers_dict[col] = outliers.index
    print(f"{col}: {len(outliers)} outliers")

# -------------------------------
# Step 4: Visualize outliers with boxplots
# -------------------------------
plt.figure(figsize=(15, 7))
sns.boxplot(data=df[columns_of_interest])
plt.title("Boxplot for detecting outliers")
plt.show()

# -------------------------------
# Step 5: Optional - mark outliers in a new column
# -------------------------------
for col in columns_of_interest:
    df[col + '_outlier'] = df[col].apply(lambda x: 1 if x in df.loc[outliers_dict[col], col].values else 0)

# -------------------------------
# Step 6: Optional - remove outliers
# -------------------------------
# Uncomment below lines to remove outliers from all columns
# for col in columns_of_interest:
#     Q1 = df[col].quantile(0.25)
#     Q3 = df[col].quantile(0.75)
#     IQR = Q3 - Q1
#     lower = Q1 - 1.5*IQR
#     upper = Q3 + 1.5*IQR
#     df = df[(df[col] >= lower) & (df[col] <= upper)]

# -------------------------------
# Step 7: Save dataset with outlier info
# -------------------------------
df.to_excel(r"C:\Users\TWEENCY MARVANIYA\OneDrive\Desktop\Agri Crop\dataset_with_outliers.xlsx", index=False)
print("Dataset with outlier flags saved as 'dataset_with_outliers.xlsx'.")
