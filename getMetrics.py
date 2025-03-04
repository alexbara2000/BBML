import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, 
    log_loss, hinge_loss,
)
import time
import joblib
import os

def evaluate_model(model, X_test, y_test, task_type="classification"):
    """
    Evaluates a scikit-learn model on the given test dataset.
    
    :param model: Trained scikit-learn model
    :param X_test: Test features
    :param y_test: True labels for test set
    :param task_type: "classification" or "regression"
    :return: Dictionary with evaluation metrics
    """
    metrics = {}

    # Measure inference time
    start_time = time.time()
    y_pred = model.predict(X_test)
    inference_time = (time.time() - start_time) / len(X_test) * 1000  # Convert to ms per sample

    # Classification Metrics
    if task_type == "classification":
        y_prob = model.predict_proba(X_test)[:, 1] if hasattr(model, "predict_proba") else None

        metrics["Accuracy"] = accuracy_score(y_test, y_pred)
        metrics["Precision"] = precision_score(y_test, y_pred, average="weighted", zero_division=0)
        metrics["Recall"] = recall_score(y_test, y_pred, average="weighted", zero_division=0)
        metrics["F1-score"] = f1_score(y_test, y_pred, average="weighted", zero_division=0)
        metrics["AUC-ROC"] = roc_auc_score(y_test, y_prob) if y_prob is not None else "N/A"
        metrics["Log Loss"] = log_loss(y_test, y_prob) if y_prob is not None else "N/A"

    # Common metrics
    metrics["Inference Time (ms)"] = inference_time

    # Estimate model size
    model_path = "temp_model.pkl"
    joblib.dump(model, model_path)
    metrics["Model Size (MB)"] = os.path.getsize(model_path) / (1024 * 1024)
    os.remove(model_path)

    return metrics

# Example Usage
if __name__ == "__main__":
    from sklearn.model_selection import train_test_split

    # Load data
    X = pd.read_csv("trainData.csv")
    y = pd.read_csv("groundTruth.csv")
    merged_data = pd.merge(X, y, on=[X.columns[0], X.columns[1]])

    # split data
    X = merged_data.iloc[:, 2:-1]
    y = merged_data.iloc[:, -1]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Evaluate
    for filename in os.listdir('models'):
        results = evaluate_model(joblib.load("models/"+filename), X_test, y_test, task_type="classification")

        # Print results
        print(f"Model: {filename[:-4]}")
        print("-" * 50)
        for metric, value in results.items():
            print(f"{metric}: {value}")
        print()
