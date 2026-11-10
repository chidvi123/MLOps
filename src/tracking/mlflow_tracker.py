import mlflow
import mlflow.sklearn

class MLflowTracker:

    def __init__(self,experiment_name):
        mlflow.set_experiment(experiment_name)

    def start_run(self,run_name,model,params,metrics):
        with mlflow.start_run(run_name=run_name):

            mlflow.log_params(params)
            mlflow.log_metrics(metrics)

            mlflow.sklearn.log_model(
                model,
                name="model",
                skops_trusted_types=["sklearn.tree._tree.Tree"]
            )