from src.data.data_loader import DataLoader
from src.data.data_validation import DataValidator
from src.data.data_splitter import DataSplitter
from src.features.feature_engineering import FeatureEngineer
from src.models.trainer import ModelTrainer
from src.models.evaluator import ModelEvaluator
from src.tracking.mlflow_tracker import MLflowTracker
from src.config_loader import ConfigLoader

class MLPipeline:

    def __init__(self):
        self.config=ConfigLoader().get_config()
        self.data_loader = DataLoader()
        self.data_validator = DataValidator()
        self.data_splitter = DataSplitter()
        self.feature_engineer = FeatureEngineer()
        self.model_trainer = ModelTrainer()
        self.model_evaluator = ModelEvaluator()
        self.tracker=MLflowTracker(self.config['experiment']['name'])

    def run(self):

        X, y = self.data_loader.load_data()

        self.data_validator.validate(X, y)

        X = self.feature_engineer.transform(X)

        X_train, X_test, y_train, y_test = (self.data_splitter.split(X, y))

        model_config=self.config['model']
        model = self.model_trainer.train(X_train, y_train,n_estimators=model_config["n_estimators"],max_depth=model_config['max_depth'], random_state=model_config['random_state'])

        metrics = self.model_evaluator.evaluate(model, X_test, y_test)

        print(f"n_estimators:: {model_config["n_estimators"]} , max_depth :{model_config["max_depth"]} ")
        print("Model Evaluation Results:")
        for metric, value in metrics.items():
            print(f"{metric}: {value:.4f}")
        print("+"*50)

        params = {
            "algorithm":"RandomForestClassifier",
            "n_estimators":model_config["n_estimators"],
            "max_depth":model_config['max_depth'],
            "random_state":model_config['random_state']
        }

        self.tracker.start_run(
            run_name=f'RF_Trees_{model_config["n_estimators"]}_Depth_{model_config["max_depth"]}',
            model=model,
            params=params,
            metrics=metrics
        )

        return model, metrics