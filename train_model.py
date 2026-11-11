import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# -----------------------------------------
# 1. LOAD DATASET
# -----------------------------------------

DATA_PATH = "dataset/placement.csv"
MODEL_DIR = "models"

TARGET = "PlacementStatus"

print("\nLoading placement dataset...")

if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(
        "Dataset not found! Place placement.csv inside the dataset folder."
    )

df = pd.read_csv(DATA_PATH)

# Remove unnecessary spaces from column names
df.columns = df.columns.astype(str).str.strip()

# Check target column
if TARGET not in df.columns:
    raise ValueError(
        f"Target column '{TARGET}' not found. "
        f"Available columns: {df.columns.tolist()}"
    )

# Remove rows without a target value
df = df.dropna(subset=[TARGET])

# Clean target labels
df[TARGET] = df[TARGET].astype(str).str.strip()

# Remove duplicate rows
df = df.drop_duplicates()

print("Dataset loaded successfully!")
print("Dataset shape:", df.shape)


# -----------------------------------------
# 2. SEPARATE INPUT AND OUTPUT
# -----------------------------------------

X = df.drop(columns=[TARGET])
y = df[TARGET]

# Remove completely empty columns
empty_columns = X.columns[X.isnull().all()].tolist()

if empty_columns:
    X = X.drop(columns=empty_columns)

if X.shape[1] == 0:
    raise ValueError("No usable input columns found.")

# Detect numeric and categorical columns
numeric_columns = X.select_dtypes(
    include=["number"]
).columns.tolist()

categorical_columns = X.select_dtypes(
    exclude=["number"]
).columns.tolist()

print("\nInput features:")
print(X.columns.tolist())

print("\nTarget classes:")
print(y.value_counts())


# -----------------------------------------
# 3. PREPROCESS DATA
# -----------------------------------------

numeric_transformer = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="median"))
    ]
)

categorical_transformer = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ]
)

preprocessor = ColumnTransformer(
    transformers=[
        ("numeric", numeric_transformer, numeric_columns),
        ("categorical", categorical_transformer, categorical_columns)
    ]
)


# -----------------------------------------
# 4. CREATE RANDOM FOREST MODEL
# -----------------------------------------

random_forest = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced"
)

# Combine preprocessing and model
model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("classifier", random_forest)
    ]
)


# -----------------------------------------
# 5. SPLIT DATASET
# -----------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining records:", len(X_train))
print("Testing records:", len(X_test))


# -----------------------------------------
# 6. TRAIN MODEL
# -----------------------------------------

print("\nTraining Random Forest model...")

model.fit(X_train, y_train)

print("Model training completed!")


# -----------------------------------------
# 7. EVALUATE MODEL
# -----------------------------------------

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("\n========== MODEL EVALUATION ==========")

print(f"\nAccuracy: {accuracy * 100:.2f}%")

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        y_pred,
        zero_division=0
    )
)

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))


# -----------------------------------------
# 8. FEATURE IMPORTANCE
# -----------------------------------------

print("\n========== FEATURE IMPORTANCE ==========")

try:
    feature_names = (
        model.named_steps["preprocessor"].get_feature_names_out()
    )

    importances = (
        model.named_steps["classifier"].feature_importances_
    )

    importance_df = pd.DataFrame({
        "Feature": feature_names,
        "Importance": importances
    })

    importance_df = importance_df.sort_values(
        by="Importance",
        ascending=False
    )

    print(importance_df.head(10).to_string(index=False))

except Exception as error:
    print("Could not calculate feature importance:", error)


# -----------------------------------------
# 9. SAVE TRAINED MODEL
# -----------------------------------------

os.makedirs(MODEL_DIR, exist_ok=True)

model_path = os.path.join(
    MODEL_DIR,
    "placement_model.pkl"
)

joblib.dump(model, model_path)

# Save feature names for the future Streamlit app
metadata = {
    "feature_columns": X.columns.tolist(),
    "target_column": TARGET,
    "classes": model.classes_.tolist(),
    "accuracy": float(accuracy)
}

metadata_path = os.path.join(
    MODEL_DIR,
    "model_metadata.pkl"
)

joblib.dump(metadata, metadata_path)

print("\n========== COMPLETED ==========")
print("Model saved at:", model_path)
print("Metadata saved at:", metadata_path)
print(f"Test accuracy: {accuracy * 100:.2f}%")
print("\nDay 1 model training completed successfully!")