from src.tracking.model_registry import ModelRegistry

registry = ModelRegistry()

registry.register_best_model(
    experiment_name="Iris_Classification",
    model_name="Iris_RF_Classifier"
)