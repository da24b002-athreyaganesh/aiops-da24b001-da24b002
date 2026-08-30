import os
import subprocess
import numpy as np
import pandas as pd
import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score

SEED = 42
np.random.seed(SEED)

os.makedirs("data", exist_ok=True)
data_path = os.path.join("data", "digits.csv")

if not os.path.exists(data_path):
    digits = load_digits(as_frame=True)
    df = digits.frame
    df.to_csv(data_path, index=False)

df = pd.read_csv(data_path)
X = df.drop(columns=["target"])
y = df["target"]

try:
    git_commit = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode("utf-8").strip()
except Exception:
    git_commit = "unknown"

mlflow.set_experiment("Capstone_Reproducibility_Drill")

with mlflow.start_run() as run:
    params = {
        "hidden_layer_sizes": (128, 64),
        "learning_rate_init": 0.001,
        "max_iter": 50,
        "random_state": SEED
    }

    mlflow.log_params(params)
    mlflow.log_param("seed", SEED)
    mlflow.set_tag("git_commit", git_commit)

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=SEED)
    clf = MLPClassifier(**params)
    clf.fit(X_train, y_train)

    val_acc = accuracy_score(y_val, clf.predict(X_val))
    mlflow.log_metric("val_accuracy", val_acc)

    model_info = mlflow.sklearn.log_model(
        sk_model=clf,
        artifact_path="model",
        registered_model_name="MNIST_MLP_Model",
        serialization_format="cloudpickle"
    )

    client = MlflowClient()
    latest_version = client.get_latest_versions("MNIST_MLP_Model", stages=["None"])[0].version
    client.transition_model_version_stage(
        name="MNIST_MLP_Model",
        version=latest_version,
        stage="Staging"
    )

    print("=" * 50)
    print(f"Run ID             : {run.info.run_id}")
    print(f"Git Commit Logged  : {git_commit}")
    print(f"Validation Accuracy: {val_acc:.4f}")
    print(f"Model Version      : {latest_version} transitioned to 'Staging'")
    print("=" * 50)
