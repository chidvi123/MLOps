import mlflow

model_uri = "models:/Iris_RF_Classifier/4"

local_path = mlflow.artifacts.download_artifacts(
    artifact_uri=model_uri,
    dst_path="artifacts/packaged_model"
)

print("Model downloaded to:", local_path)