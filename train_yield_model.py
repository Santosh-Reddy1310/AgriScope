import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

# Load preprocessed long-format data
df = pd.read_csv("data/final_crop_production.csv")

print("✅ Data shape before filtering:", df.shape)
print("🔍 Head of Data:")
print(df.head())
print("🔍 Null values in each column:")
print(df.isnull().sum())

# Check required columns
required_cols = ["Region", "Year", "Crop", "Production (1000 tons)"]
if not all(col in df.columns for col in required_cols):
    raise ValueError(f"❌ Required columns missing. Found: {df.columns.tolist()}")

# Drop nulls
df = df[required_cols].dropna()

if df.empty:
    raise ValueError("❌ No data available after cleaning! Check your CSV content.")

# Encode categorical features
le_region = LabelEncoder()
le_crop = LabelEncoder()

df["Region_encoded"] = le_region.fit_transform(df["Region"])
df["Crop_encoded"] = le_crop.fit_transform(df["Crop"])

# Features and target
X = df[["Region_encoded", "Crop_encoded", "Year"]]
y = df["Production (1000 tons)"]

# 🔧 Optional: Downsample for faster training
print("⚡ Sampling data for quick training...")
df_sampled = df.sample(n=3000, random_state=42) if len(df) > 3000 else df
X = df_sampled[["Region_encoded", "Crop_encoded", "Year"]]
y = df_sampled["Production (1000 tons)"]

# Split (just to avoid overfitting if needed later)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model
print("🚀 Training model...")
model = RandomForestRegressor(n_estimators=30, random_state=42, verbose=1)
model.fit(X_train, y_train)
print("✅ Model training completed.")

# Save model and encoders
joblib.dump(model, "models/crop_yield_model.pkl")
joblib.dump(le_region, "models/region_encoder.pkl")
joblib.dump(le_crop, "models/crop_encoder.pkl")
print("📦 Model and encoders saved in /models/")
