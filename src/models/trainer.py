from sklearn.ensemble import RandomForestClassifier
from src.config_loader import ConfigLoader


class ModelTrainer:
    def train(self, X_train, y_train, n_estimators=100, max_depth=5,random_state=42):

        model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=random_state
        )

        model.fit(X_train, y_train)

        return model