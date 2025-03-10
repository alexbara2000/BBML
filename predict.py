import joblib
import pandas as pd

# Load the trained model from a file
model_filename = "models/NeuralNetwork.pkl"
model = joblib.load(model_filename)

# Load the new data from a CSV file
data_filename = "processed_data.csv"
data = pd.read_csv(data_filename)

id_columns = data.iloc[:, :2]
X_new = data.iloc[:, 2:]

# Make predictions
predictions = model.predict(X_new)

output_df = id_columns.copy()
output_df["Prediction"] = predictions

output_filename = "predictions.csv"
output_df.to_csv(output_filename, index=False)

# Print predictions
print("Predictions:")
print(predictions)
