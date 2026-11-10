class FeatureEngineer:

    def transform(self, X):

        X = X.copy()

        X["petal_area"] = (
            X["petal length (cm)"] * X["petal width (cm)"]
        )

        X["sepal_area"] = (
            X["sepal length (cm)"] * X["sepal width (cm)"]
        )

        return X