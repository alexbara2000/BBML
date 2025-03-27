import os
import glob
import pandas as pd

# Find all files in the results folder that start with 'predictions'
predictions_files = glob.glob(os.path.join("results", "predictions*.csv"))
if not predictions_files:
    print("No predictions files found in the results folder.")
    
for pred_file in predictions_files:
    # Extract the identifier X from filename 'predictionsX.csv'
    base_name = os.path.basename(pred_file)
    identifier = base_name.replace("predictions", "").replace(".csv", "")
    
    # Load the predictions file
    df = pd.read_csv(pred_file)
    
    # Determine the last column (assumed to be the prediction column)
    last_col = df.columns[-1]
    
    # Filter rows where the last column equals 1
    filtered_df = df[df[last_col] == 1].copy()
    
    # Set the last column to an empty string
    filtered_df[last_col] = ""
    
    # Save the filtered dataframe to a new file named manual_classificationX.csv
    manual_filename = os.path.join("results", f"manual_classification{identifier}.csv")
    filtered_df.to_csv(manual_filename, index=False)
    print(f"Manual classification for {pred_file} saved to {manual_filename}")
