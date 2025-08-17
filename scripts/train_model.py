import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib
from wrangle_data import wrangle_car_data

def train():
    df = wrangle_car_data("data/raw/vehicles.csv")
    
    X = df.drop("price", axis=1)
    y = df["price"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        

    model = LinearRegression(positive=True)
    model.fit(X_train, y_train)

    # categorical_cols = df.select_dtypes(include=["category"]).columns.tolist()
    # # Save unique values for each categorical column
    # cat_values = {col: df[col].dropna().unique().tolist() for col in categorical_cols}
    
    numerical_cols = X.select_dtypes(include=["int64", "float64"]).columns.tolist()

    try:
        schema = joblib.load("models/schema.pkl")
    except FileNotFoundError:
        schema = {}  # start with empty dict if file doesn’t exist

    # Save schema
    joblib.dump({
        **schema,
        "expected_columns": X.columns.tolist(),
        "numerical_cols": numerical_cols
    }, "models/schema.pkl")

    # expected_columns = X_train.columns.tolist()
    # # Save the expected column order
    # joblib.dump(expected_columns, "models/price_predictor_columns.pkl")
    
    joblib.dump(model, "models/price_predictor.pkl")
    print("✅ Model trained and saved.")



if __name__ == "__main__":
    train()
