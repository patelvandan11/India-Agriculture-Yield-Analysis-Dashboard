import pandas as pd
import numpy as np
import random

# Load your clean dataset
df = pd.read_excel("crop_yield.xlsx")  # make sure your file is in the same folder

# Make a copy
unclean_df = df.copy()

# 1. Introduce random missing values (NaNs)
for col in unclean_df.columns:
    unclean_df.loc[unclean_df.sample(frac=0.05).index, col] = np.nan  # 5% missing values

# 2. Add inconsistent casing and extra spaces in categorical/text columns
def messify_text(val):
    if pd.isna(val):
        return val
    val = str(val)
    choices = [
        val.lower(),
        val.upper(),
        val.capitalize(),
        " " + val + " ",
        val + "   ",
        val.replace("a", "@"),
    ]
    return random.choice(choices)

for col in ['Crop', 'Season', 'State']:
    unclean_df[col] = unclean_df[col].apply(messify_text)

# 3. Convert some numeric columns to strings and mix types
for col in ['Area', 'Production', 'Annual_Rainfall', 'Fertilizer', 'Pesticide', 'Yield']:
    unclean_df.loc[unclean_df.sample(frac=0.05).index, col] = unclean_df[col].astype(str)

# 4. Add duplicate rows randomly
duplicates = unclean_df.sample(frac=0.02, random_state=1)
unclean_df = pd.concat([unclean_df, duplicates]).sample(frac=1).reset_index(drop=True)

# Ensure same number of rows as original (truncate extras if needed)
unclean_df = unclean_df.iloc[:len(df), :]

# Save unclean dataset
unclean_df.to_excel("unclean_crop_yield.xlsx", index=False)

print("Unclean dataset saved as unclean_crop_yield.xlsx")
