
import mlflow.pyfunc
import pandas as pd

model = mlflow.pyfunc.load_model(
    "artifacts/packaged_model"
)

X = pd.DataFrame(
    [[5.1, 3.5, 1.4, 0.2]],
    columns=[
        "sepal length (cm)",
        "sepal width (cm)",
        "petal length (cm)",
        "petal width (cm)"
    ]
)

X["petal_area"] = X["petal length (cm)"] * X["petal width (cm)"]
X["sepal_area"] = X["sepal length (cm)"] * X["sepal width (cm)"]

prediction = model.predict(X)

print("Prediction:", prediction)
