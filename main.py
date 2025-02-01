import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

# Load the data
X = pd.read_csv("trainData.csv")
y = pd.read_csv("groundTruth.csv")

# Merge the datasets on the ID column
merged_data = pd.merge(X, y, on=[X.columns[0], X.columns[1]])

# Drop the ID column after merging
X = merged_data.iloc[:, 2:-1]
y = merged_data.iloc[:, -1]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)

# Create the pipeline
pipeline = Pipeline([
    ("scaler", StandardScaler()),  # Standardize the features
    ("classifier", MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=42))
])

# Train the model
pipeline.fit(X_train, y_train)

# Make predictions
y_pred = pipeline.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")
print("Classification Report:\n", classification_report(y_test, y_pred))
