import streamlit as st
import pickle
import json
import pandas as pd

# -------------------------------
# Load model and columns
# -------------------------------
model = pickle.load(open("banglore_home_prices_model.pickle", "rb"))

with open("columns.json", "r") as f:
    data_columns = json.load(f)

# -------------------------------
# UI
# -------------------------------
st.title("🏠 Bangalore House Price Prediction")

st.write("Enter property details to estimate price")

# numeric inputs
sqft = st.number_input("Total Sqft", min_value=0.0)
bath = st.number_input("Bathrooms", min_value=0)
bhk = st.number_input("BHK", min_value=0)

# categorical inputs
location = st.selectbox("Location", data_columns["location_columns"])
area = st.selectbox("Area Type", data_columns["area_columns"])
availability = st.selectbox("Availability", data_columns["availability_columns"])

# -------------------------------
# Prediction
# -------------------------------
if st.button("Predict"):

    input_dict = {}

    # numeric
    input_dict["total_sqft"] = sqft
    input_dict["bath"] = bath
    input_dict["bhk"] = bhk

    # categorical (initialize all to 0)
    for col in data_columns["location_columns"]:
        input_dict[col] = 0

    for col in data_columns["area_columns"]:
        input_dict[col] = 0

    for col in data_columns["availability_columns"]:
        input_dict[col] = 0

    # set selected = 1
    if location in input_dict:
        input_dict[location] = 1

    if area in input_dict:
        input_dict[area] = 1

    if availability in input_dict:
        input_dict[availability] = 1

    # convert to dataframe
    df = pd.DataFrame([input_dict])

    # 🚨 IMPORTANT FIX: match training feature count
    expected_features = model.get_booster().num_features()

    if df.shape[1] > expected_features:
        df = df.iloc[:, :expected_features]
    elif df.shape[1] < expected_features:
        # add missing columns
        for i in range(expected_features - df.shape[1]):
            df[f"missing_{i}"] = 0

    # prediction
    prediction = model.predict(df)[0]

    st.success(f"Estimated Price: ₹ {round(prediction,2)} Lakhs")
