import streamlit as st
import pandas as pd
import joblib
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier

# Load the trained model
model = joblib.load("ResalePrice_compressed.pkl")


st.title("HDB Resale Price Prediction")

# Description
st.write("""
This app predicts the resale price of HDB flats in Singapore.
Fill in the required details, and the model will predict the price for you!
""")


# Input features
st.sidebar.header("Input Features")
floor_area = st.sidebar.number_input("Floor Area (sqm)", min_value=40.0, max_value=150.0, step=1.0)
region = st.sidebar.selectbox("Region", ["Central", "East", "North", "North-East", "West"])
flat_type = st.sidebar.selectbox("Flat Type", ["1 ROOM", "2 ROOM", "3 ROOM", "4 ROOM", "5 ROOM", "EXECUTIVE"])
lease_remaining = st.sidebar.slider("Lease Remaining (Years)", min_value=70, max_value=99, step=1)


# Map user input into dataframe
input_data = {
    "floor_area_sqm": [floor_area],
    "region_Central": [1 if region == "Central" else 0],
    "region_East": [1 if region == "East" else 0],
    "region_North": [1 if region == "North" else 0],
    "region_North-East": [1 if region == "North-East" else 0],
    "region_West": [1 if region == "West" else 0],
    "flat_type_1 ROOM": [1 if flat_type == "1 ROOM" else 0],
    "flat_type_2 ROOM": [1 if flat_type == "2 ROOM" else 0],
    "flat_type_3 ROOM": [1 if flat_type == "3 ROOM" else 0],
    "flat_type_4 ROOM": [1 if flat_type == "4 ROOM" else 0],
    "flat_type_5 ROOM": [1 if flat_type == "5 ROOM" else 0],
    "flat_type_EXECUTIVE": [1 if flat_type == "EXECUTIVE" else 0],
    "lease_remaining": [lease_remaining]
}

# Convert to DataFrame
input_df = pd.DataFrame(input_data)

# Predict resale price
if st.button("Predict"):
    prediction = model.predict(input_df)
    st.success(f"The predicted resale price is: ${prediction[0]:,.2f}")
