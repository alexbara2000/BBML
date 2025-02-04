import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

# Load data
X = pd.read_csv("trainData.csv")
y = pd.read_csv("groundTruth.csv")
merged_data = pd.merge(X, y, on=[X.columns[0], X.columns[1]])

# split data
X = merged_data.iloc[:, 2:-1]
y = merged_data.iloc[:, -1]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

models = {
    "RandomForest": (RandomForestClassifier(random_state=42), {
        'classifier__n_estimators': [50, 100, 150],
        'classifier__max_depth': [None, 10, 20, 30],
        'classifier__min_samples_split': [2, 5, 10],
        'classifier__min_samples_leaf': [1, 2, 4]
    }),
    "SVM": (SVC(random_state=42), {
        'classifier__C': [0.1, 1, 10],
        'classifier__kernel': ['linear', 'rbf'],
        'classifier__gamma': ['scale', 'auto']
    }),
    "KNN": (KNeighborsClassifier(), {
        'classifier__n_neighbors': [3, 5, 7],
        'classifier__weights': ['uniform', 'distance'],
        'classifier__metric': ['euclidean', 'manhattan']
    }),
    "XGBoost": (GradientBoostingClassifier(random_state=42), {
        'classifier__n_estimators': [50, 100, 150],
        'classifier__max_depth': [3, 5, 7],
        'classifier__learning_rate': [0.01, 0.1, 0.2]
    }),
    "NeuralNetwork": (MLPClassifier(max_iter=1000, random_state=42), {
        'classifier__hidden_layer_sizes': [(50,), (100,), (50, 50)],
        'classifier__activation': ['relu', 'tanh'],
        'classifier__solver': ['adam', 'sgd']
    })
}

for model_name, (classifier, param_grid) in models.items():
    print(f"Running GridSearchCV for {model_name}...")
    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("classifier", classifier)
    ])

    grid_search = GridSearchCV(pipeline, param_grid, cv=5, n_jobs=-1, scoring='accuracy')
    grid_search.fit(X_train, y_train)

    print(f"Best Parameters for {model_name}: {grid_search.best_params_}")
    print(f"Best Cross-validation Accuracy for {model_name}: {grid_search.best_score_:.2f}")

    # Evaluate model
    best_pipeline = grid_search.best_estimator_
    y_pred = best_pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Test Set Accuracy for {model_name}: {accuracy:.2f}")
    print(f"Classification Report for {model_name}:\n", classification_report(y_test, y_pred))
    print("-" * 50)
