import streamlit as st
import pandas as pd
import joblib

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
town = st.sidebar.selectbox("Town", [
    'ANG MO KIO', 'BEDOK', 'BISHAN', 'BUKIT BATOK', 'BUKIT MERAH', 'BUKIT TIMAH',
    'CENTRAL AREA', 'CHOA CHU KANG', 'CLEMENTI', 'GEYLANG', 'HOUGANG',
    'JURONG EAST', 'JURONG WEST', 'KALLANG/WHAMPOA', 'MARINE PARADE', 'PASIR RIS',
    'PUNGGOL', 'QUEENSTOWN', 'SEMBAWANG', 'SENGKANG', 'SERANGOON', 'TAMPINES',
    'TOA PAYOH', 'WOODLANDS', 'YISHUN'
])
flat_type = st.sidebar.selectbox("Flat Type", ["1 ROOM", "2 ROOM", "3 ROOM", "4 ROOM", "5 ROOM", "EXECUTIVE", "MULTI GENERATION"])
lease_remaining = st.sidebar.slider("Lease Remaining (Years)", min_value=70, max_value=99, step=1)
storey_category = st.sidebar.selectbox("Storey Category", ["Low Storey", "Mid Storey", "High Storey"])

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
    "region_" + region_map[town]: [1],
    "flat_type_" + flat_type: [1],
    "flat_model_category_" + flat_model_map.get(flat_type, "Unknown"): [1],
    "storey_category_" + storey_category: [1],
    "lease_remaining": [lease_remaining]
}

# Fill missing one-hot encoded columns with 0
all_columns = [
    # Add all expected one-hot columns here based on your training data
    "region_Central", "region_East", "region_North", "region_North-East", "region_West",
    "flat_type_1 ROOM", "flat_type_2 ROOM", "flat_type_3 ROOM", "flat_type_4 ROOM",
    "flat_type_5 ROOM", "flat_type_EXECUTIVE", "flat_type_MULTI GENERATION",
    "flat_model_category_Smaller Flats", "flat_model_category_Maisonettes",
    "flat_model_category_Larger Flats", "flat_model_category_Special Models",
    "storey_category_Low Storey", "storey_category_Mid Storey", "storey_category_High Storey"
]

input_df = pd.DataFrame(input_data)
for col in all_columns:
    if col not in input_df.columns:
        input_df[col] = 0

# Predict resale price
if st.button("Predict"):
    prediction = model.predict(input_df)
    st.success(f"The predicted resale price is: ${prediction[0]:,.2f}")
