
import pandas as pd

class DataLoader:

    def load_data(self):
        df = pd.read_csv("data/raw/iris.csv")

        X = df.drop(columns=["target"])
        y = df["target"]

        return X, y
