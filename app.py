import streamlit as st

st.title("🏠 House Price Prediction")

sqft = st.number_input("Enter Square Feet")
bath = st.number_input("Enter Number of Bathrooms")
bhk = st.number_input("Enter BHK")

if st.button("Predict"):
    price = sqft * 0.01 + bath * 10 + bhk * 5
    st.success(f"Estimated Price: {price}")
