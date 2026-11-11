from sklearn.datasets import load_iris
from pathlib import Path

iris = load_iris(as_frame=True)
df = iris.frame

Path("data/raw").mkdir(parents=True, exist_ok=True)
df.to_csv("data/raw/iris.csv", index=False)

print("Dataset saved successfully!")
print("Shape:", df.shape)
