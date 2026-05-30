
import pandas as pd
#import joblib  
import pickle

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


# Load dataset

df = pd.read_csv("data/telco_churn.csv")

# Remove customerID

df.drop(columns=["customerID"], inplace=True)

# Handle TotalCharges

df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
df["TotalCharges"] = df["TotalCharges"].fillna(df["TotalCharges"].median())

# Features and target

X = df.drop("Churn", axis=1)
y = df["Churn"]

# Categorical and numerical columns

categorical_cols = X.select_dtypes(include=["object"]).columns
numerical_cols = X.select_dtypes(exclude=["object"]).columns

# Preprocessing

preprocessor = ColumnTransformer(
    transformers=[
        (
            "cat",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_cols
        ),
        (
            "num",
            StandardScaler(),
            numerical_cols
        )
    ]
)

# Pipeline

pipeline = Pipeline([
    (
        "preprocessor",
        preprocessor
    ),
    (
        "model",
        RandomForestClassifier(
            n_estimators=200,
            max_depth=10,
            random_state=42
        )
    )
])

# Train test split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Train

pipeline.fit(X_train, y_train)

# Predict

y_pred = pipeline.predict(X_test)

# Accuracy

accuracy = accuracy_score(y_test, y_pred)

print(f"Accuracy: {accuracy:.4f}")

print("Classification Report:")
print(classification_report(y_test, y_pred))

# Save model

# Replace joblib.dump(pipeline, "models/churn_pipeline.pkl") with:
with open("models/churn_pipeline.pkl", "wb") as file:
    pickle.dump(pipeline, file)

print("Model saved successfully!")