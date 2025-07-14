import pandas as pd
import os

# Load dataset
df = pd.read_csv("data/crop_production.csv")

# Rename for consistency
df = df.rename(columns={"State Name": "Region"})

# Extract only 'Region', 'Year', and all production columns
prod_cols = [col for col in df.columns if "PRODUCTION" in col.upper()]
keep_cols = ["Region", "Year"] + prod_cols
df = df[keep_cols]

# Melt wide to long format
long_df = pd.melt(df, id_vars=["Region", "Year"], value_vars=prod_cols,
                  var_name="Crop", value_name="Production (1000 tons)")

# Clean crop names
long_df["Crop"] = long_df["Crop"].str.replace("PRODUCTION \\(1000 tons\\)", "", regex=True)
long_df["Crop"] = long_df["Crop"].str.strip().str.title()

# Drop rows with missing values
long_df = long_df.dropna(subset=["Region", "Year", "Crop", "Production (1000 tons)"])

# Export cleaned long format data
os.makedirs("data", exist_ok=True)
output_path = "data/final_crop_production.csv"
long_df.to_csv(output_path, index=False)

print(f"✅ Converted to long format. Rows: {len(long_df)}")
print(f"📁 Saved to: {output_path}")
print("📊 Sample:\n", long_df.head())
