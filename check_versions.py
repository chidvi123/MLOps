from mlflow.tracking import MlflowClient

client = MlflowClient()

versions = client.search_model_versions(
    "name='Iris_RF_Classifier'"
)

for version in versions:
    print("Version:", version.version)
    print("Status:", version.status)
    print("Run ID:", version.run_id)
    print("----------------------")