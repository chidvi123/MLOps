from src.data.data_loader import DataLoader
from src.data.data_validation import DataValidator

loader = DataLoader()

X, y = loader.load_data()

print("Features shape:", X.shape)
print("Target shape:", y.shape)

print("\nFirst 5 rows:")
print(X.head())

print("\nTarget labels:")
print(y.unique())

validator = DataValidator()
validator.validate(X,y)