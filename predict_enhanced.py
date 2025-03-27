import os
import glob
import joblib
import pandas as pd
import numpy as np

# Load all models from the models folder (assuming .pkl files)
model_files = glob.glob("models/*.pkl")
models = []
for mf in model_files:
    try:
        model = joblib.load(mf)
        models.append(model)
        print(f"Loaded model: {mf}")
    except Exception as e:
        print(f"Could not load {mf}: {e}")

if not models:
    raise Exception("No models were loaded from the models folder.")

# Find all files in the results folder that start with 'processed_data'
processed_files = glob.glob(os.path.join("results", "processed_data*.csv"))
if not processed_files:
    print("No processed data files found in the results folder.")
    
for file in processed_files:
    # Extract the identifier X from filename 'processed_dataX.csv'
    base_name = os.path.basename(file)
    identifier = base_name.replace("processed_data", "").replace(".csv", "")
    
    # Load data from the current processed file
    data = pd.read_csv(file)
    # Assuming the first two columns are ID columns
    id_columns = data.iloc[:, :2]
    X_new = data.iloc[:, 2:]
    
    # Initialize union predictions.
    # We assume that the predictions are binary (0 or 1).
    union_pred = None
    for model in models:
        pred = model.predict(X_new)
        if union_pred is None:
            union_pred = pred.copy()  # initialize with the first model's predictions
        else:
            # Logical OR on the predictions: if any model gives a positive (1), result is 1.
            union_pred = np.logical_or(union_pred, pred).astype(int)
    
    # Create the output dataframe with id columns and the union prediction.
    output_df = id_columns.copy()
    output_df["Prediction"] = union_pred
    
    # Save the results to a new file in the results folder.
    output_filename = os.path.join("results", f"predictions{identifier}.csv")
    output_df.to_csv(output_filename, index=False)
    
    print(f"Predictions for {file} saved to {output_filename}")
