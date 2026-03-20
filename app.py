import streamlit as st
import pickle
import json
import numpy as np

# load model
model = pickle.load(open("banglore_home_prices_model.pickle", "rb"))

# load columns
with open("columns.json", "r") as f:
    data_columns = json.load(f)

st.title("🏠 Bangalore House Price Prediction")

# numeric inputs
sqft = st.number_input("Total Sqft")
bath = st.number_input("Bathrooms")
bhk = st.number_input("BHK")

# categorical inputs
location = st.selectbox("Location", data_columns["location_columns"])
area = st.selectbox("Area Type", data_columns["area_columns"])
availability = st.selectbox("Availability", data_columns["availability_columns"])

if st.button("Predict"):
    
    # total feature size
    total_features = 3 + len(data_columns["location_columns"]) + \
                     len(data_columns["area_columns"]) + \
                     len(data_columns["availability_columns"])
    
    x = np.zeros(total_features)

    # numeric features
    x[0] = sqft
    x[1] = bath
    x[2] = bhk

    # location encoding
    loc_index = data_columns["location_columns"].index(location)
    x[3 + loc_index] = 1

    # area encoding
    area_offset = 3 + len(data_columns["location_columns"])
    area_index = data_columns["area_columns"].index(area)
    x[area_offset + area_index] = 1

    # availability encoding
    avail_offset = area_offset + len(data_columns["area_columns"])
    avail_index = data_columns["availability_columns"].index(availability)
    x[avail_offset + avail_index] = 1

    # prediction
    prediction = model.predict([x])[0]

    st.success(f"Estimated Price: ₹ {round(prediction,2)} Lakhs")
