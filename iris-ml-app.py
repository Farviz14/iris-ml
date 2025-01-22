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


st.subheader('User Input parameters')
st.write(df)

iris = datasets.load_iris()
X = iris.data
Y = iris.target

clf = RandomForestClassifier()
clf.fit(X, Y)

prediction = clf.predict(df)
prediction_proba = clf.predict_proba(df)

st.subheader('Class labels and their corresponding index number')
st.write(iris.target_names)

st.subheader('Prediction')
st.write(iris.target_names[prediction])
#st.write(prediction)

st.subheader('Prediction Probability')
st.write(prediction_proba)
