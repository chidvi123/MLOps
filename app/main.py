
from fastapi import FastAPI
from pydantic import BaseModel
import mlflow.pyfunc
import pandas as pd

app = FastAPI()

# Load the trained ML model
model = mlflow.pyfunc.load_model(
    "artifacts/packaged_model"
)


# Define expected input
class IrisInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float


# Prediction endpoint
@app.post("/predict")
def predict(data: IrisInput):

    input_data = pd.DataFrame(
        [[
            data.sepal_length,
            data.sepal_width,
            data.petal_length,
            data.petal_width
        ]],
        columns=[
            "sepal length (cm)",
            "sepal width (cm)",
            "petal length (cm)",
            "petal width (cm)"
        ]
    )

    # Apply feature engineering
    input_data["petal_area"] = (
        input_data["petal length (cm)"] *
        input_data["petal width (cm)"]
    )

    input_data["sepal_area"] = (
        input_data["sepal length (cm)"] *
        input_data["sepal width (cm)"]
    )

    # Generate prediction
    prediction = model.predict(input_data)

    return {
        "prediction": int(prediction[0])
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
