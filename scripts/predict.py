# scripts/predict.py
import streamlit as st
import joblib
import pandas as pd
from datetime import datetime

# # Load model + columns
# model = joblib.load("models/price_predictor.pkl")
# expected_columns = joblib.load("models/price_predictor_columns.pkl")

# st.title("🚗 Used Car Price Predictor")

# year = st.number_input("Year", 1990, 2025, 2015)
# odometer = st.number_input("Odometer (km)", 0, 300000, 50000)
# fuel = st.selectbox("Fuel", ['gas', 'diesel', 'electric'])
# transmission = st.selectbox("Transmission", ['automatic', 'manual'])

# # Build input row
# input_data = pd.DataFrame({
#     'odometer': [odometer],
#     'age': [datetime.now().year - year],
#     f'fuel_{fuel}': [1],
#     f'transmission_{transmission}': [1],
# })

# # Align columns with training data
# input_data = input_data.reindex(columns=expected_columns, fill_value=0)

# # Predict
# pred = model.predict(input_data)[0]
# st.success(f"Estimated Price: ${int(pred):,}")


# Load model & schema
model = joblib.load("models/price_predictor.pkl")
schema = joblib.load("models/schema.pkl")

expected_columns = schema["expected_columns"]
categorical_values = schema["categorical_values"]
numerical_cols = schema["numerical_cols"]

st.title("🚗 Used Car Price Predictor")

# Dictionary to collect user input
user_input = {}

# Handle numerical features
for col in numerical_cols:
    if col == "year":  
        # Special handling: compute age
        year = st.number_input("Year", 1990, datetime.now().year, 2015)
        user_input["age"] = datetime.now().year - year
    else:
        user_input[col] = st.number_input(col, 0.0, 1e6, 0.0)

# Handle categorical features dynamically
print("numerical_cols", numerical_cols)

for col, values in categorical_values.items():
    choice = st.selectbox(col, values)
    for val in values:
        user_input[f"{col}_{val}"] = 1 if choice == val else 0

# Build DataFrame
input_data = pd.DataFrame([user_input])

# Align with training schema
input_data = input_data.reindex(columns=expected_columns, fill_value=0)

# Predict
pred = model.predict(input_data)[0]
st.success(f"Estimated Price: ${int(pred):,}")
