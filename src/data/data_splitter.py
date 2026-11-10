from sklearn.model_selection import train_test_split
from src.config_loader import ConfigLoader

class DataSplitter:
    def __init__(self):
        self.config=ConfigLoader().get_config()

    def split(self, X, y):
        test_size=self.config['training']['test_size']
        random_state=self.config['model']['random_state']

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=test_size,
            random_state=random_state,
            stratify=y
        )

        return X_train, X_test, y_train, y_test