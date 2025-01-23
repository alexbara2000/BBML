import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

# Load the data
X = pd.read_csv("trainData.csv")
y = pd.read_csv("groundTruth.csv")

# Merge the datasets on the ID column
merged_data = pd.merge(X, y, on=X.columns[0])

# Drop the ID column after merging
X = merged_data.iloc[:, 1:-1]
y = merged_data.iloc[:, -1]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create the pipeline
pipeline = Pipeline([
    ("scaler", StandardScaler()),  # Standardize the features
    ("classifier", RandomForestClassifier(random_state=42))  # Random Forest model
])

# Train the model
pipeline.fit(X_train, y_train)

# Make predictions
y_pred = pipeline.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")
print("Classification Report:\n", classification_report(y_test, y_pred))
