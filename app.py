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

    # create input dictionary
    input_dict = {}

    # numeric features (IMPORTANT: match training names)
    input_dict["total_sqft"] = sqft
    input_dict["bath"] = bath
    input_dict["bhk"] = bhk

    # initialize categorical columns
    for col in data_columns["location_columns"]:
        input_dict[col] = 0

    for col in data_columns["area_columns"]:
        input_dict[col] = 0

    for col in data_columns["availability_columns"]:
        input_dict[col] = 0

    # set selected values
    input_dict[location] = 1
    input_dict[area] = 1
    input_dict[availability] = 1

    # convert to dataframe
    df = pd.DataFrame([input_dict])

    try:
        prediction = model.predict(df)[0]
        st.success(f"Estimated Price: ₹ {round(prediction,2)} Lakhs")
    except Exception as e:
        st.error("Prediction failed. Check feature alignment.")
        st.write(e)
