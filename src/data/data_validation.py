class DataValidator:

    def validate(self, X, y):

        if X.empty:
            raise ValueError("Feature dataset is empty")

        if y.empty:
            raise ValueError("Target dataset is empty")

        if X.isnull().sum().any():
            raise ValueError("Missing values found in features")

        if y.isnull().sum() > 0:
            raise ValueError("Missing values found in target")

        if len(X) != len(y):
            raise ValueError("Features and target have different lengths")

        print("Data validation successful!")
        return True