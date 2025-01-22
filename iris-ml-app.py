import streamlit as st
import pandas as pd
import joblib

# Load the trained model
model = joblib.load("ResalePrice_compressed.pkl")

# Feature order from the trained model
expected_feature_order = [
    'floor_area_sqm', 'lease_age_years', 'region_Central', 'region_East', 'region_North',
    'region_North-East', 'region_West', 'flat_type_1 ROOM', 'flat_type_2 ROOM',
    'flat_type_3 ROOM', 'flat_type_4 ROOM', 'flat_type_5 ROOM', 'flat_type_EXECUTIVE',
    'flat_type_MULTI GENERATION', 'flat_model_category_Larger Flats',
    'flat_model_category_Maisonettes', 'flat_model_category_Smaller Flats',
    'flat_model_category_Special Models', 'storey_category_Low Storey',
    'storey_category_Mid Storey', 'storey_category_High Storey'
]

st.title("HDB Resale Price Prediction")

# Description
st.write("""
This app predicts the resale price of HDB flats in Singapore.
Fill in the required details, and the model will predict the price for you!
""")

# Input features
st.sidebar.header("Input Features")
floor_area = st.sidebar.number_input("Floor Area (sqm)", min_value=40.0, max_value=150.0, step=1.0)
town = st.sidebar.selectbox("Town", [
    'ANG MO KIO', 'BEDOK', 'BISHAN', 'BUKIT BATOK', 'BUKIT MERAH', 'BUKIT TIMAH',
    'CENTRAL AREA', 'CHOA CHU KANG', 'CLEMENTI', 'GEYLANG', 'HOUGANG',
    'JURONG EAST', 'JURONG WEST', 'KALLANG/WHAMPOA', 'MARINE PARADE', 'PASIR RIS',
    'PUNGGOL', 'QUEENSTOWN', 'SEMBAWANG', 'SENGKANG', 'SERANGOON', 'TAMPINES',
    'TOA PAYOH', 'WOODLANDS', 'YISHUN'
])
flat_type = st.sidebar.selectbox("Flat Type", ["1 ROOM", "2 ROOM", "3 ROOM", "4 ROOM", "5 ROOM", "EXECUTIVE", "MULTI GENERATION"])
flat_model = st.sidebar.selectbox("Flat Model", [
    'IMPROVED', 'NEW GENERATION', 'STANDARD', 'MODEL A', 'SIMPLIFIED',
    'MODEL A-MAISONETTE', 'MAISONETTE', 'IMPROVED-MAISONETTE', 'APARTMENT',
    'TERRACE', 'PREMIUM APARTMENT', '2-ROOM', 'MULTI GENERATION'
])
lease_remaining_years = st.sidebar.slider("Lease Remaining (Years)", min_value=70, max_value=99, step=1)
storey_category = st.sidebar.selectbox("Storey Category", ["Low Storey", "Mid Storey", "High Storey"])

# Map remaining years to age of lease
lease_age_years = 99 - lease_remaining_years

# Mapping towns to regions
region_map = {
    'ANG MO KIO': 'Central', 'BEDOK': 'East', 'BISHAN': 'Central', 'BUKIT BATOK': 'West', 
    'BUKIT MERAH': 'Central', 'BUKIT TIMAH': 'Central', 'CENTRAL AREA': 'Central', 
    'CHOA CHU KANG': 'West', 'CLEMENTI': 'West', 'GEYLANG': 'East', 'HOUGANG': 'North-East', 
    'JURONG EAST': 'West', 'JURONG WEST': 'West', 'KALLANG/WHAMPOA': 'Central', 
    'MARINE PARADE': 'East', 'PASIR RIS': 'East', 'PUNGGOL': 'North-East', 
    'QUEENSTOWN': 'Central', 'SEMBAWANG': 'North', 'SENGKANG': 'North-East', 
    'SERANGOON': 'North-East', 'TAMPINES': 'East', 'TOA PAYOH': 'Central', 
    'WOODLANDS': 'North', 'YISHUN': 'North'
}

# Map flat models to broader categories
flat_model_map = {
    'IMPROVED': 'Smaller Flats', 'NEW GENERATION': 'Smaller Flats', 'STANDARD': 'Smaller Flats', 
    'MODEL A': 'Smaller Flats', 'SIMPLIFIED': 'Smaller Flats', 'MODEL A-MAISONETTE': 'Maisonettes', 
    'MAISONETTE': 'Maisonettes', 'IMPROVED-MAISONETTE': 'Maisonettes', 'APARTMENT': 'Larger Flats', 
    'TERRACE': 'Larger Flats', 'PREMIUM APARTMENT': 'Larger Flats', '2-ROOM': 'Special Models', 
    'MULTI GENERATION': 'Special Models'
}

# Map user input into dataframe
input_data = {
    "floor_area_sqm": [floor_area],
    "lease_age_years": [lease_age_years],
    f"region_{region_map[town]}": [1],
    f"flat_type_{flat_type}": [1],
    f"flat_model_category_{flat_model_map[flat_model]}": [1],
    f"storey_category_{storey_category}": [1]
}

# Add missing columns and set them to 0
for feature in expected_feature_order:
    if feature not in input_data:
        input_data[feature] = [0]

# Create DataFrame and order columns
input_df = pd.DataFrame(input_data)
input_df = input_df[expected_feature_order]

# Predict resale price
if st.button("Predict"):
    try:
        prediction = model.predict(input_df)
        st.success(f"The predicted resale price is: ${prediction[0]:,.2f}")
    except Exception as e:
        st.error(f"Error during prediction: {e}")
