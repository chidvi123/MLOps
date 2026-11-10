import mlflow
from mlflow.tracking import MlflowClient


class ModelRegistry:

    def register_best_model(self, experiment_name, model_name):

        runs = mlflow.search_runs(
            experiment_names=[experiment_name],
            order_by=["metrics.f1_score DESC"],
            max_results=1
        )

        if runs.empty:
            raise ValueError("No runs found!")

        best_run = runs.iloc[0]
        run_id = best_run["run_id"]

        model_uri = f"runs:/{run_id}/model"

        client = MlflowClient()

        versions = client.search_model_versions(
            filter_string=f"name='{model_name}'"
        )

        for version in versions:
            if version.run_id == run_id:
                print("This run is already registered!")
                print("Existing version:", version.version)
                return version

        registered_model = mlflow.register_model(
            model_uri=model_uri,
            name=model_name
        )

        print("Best Run ID:", run_id)
        print("Best F1 Score:", best_run["metrics.f1_score"])
        print("Registered Model Version:", registered_model.version)

        return registered_model