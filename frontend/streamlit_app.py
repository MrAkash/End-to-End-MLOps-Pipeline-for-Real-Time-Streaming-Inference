####### frontend/streamlit_app.py #####
import streamlit as st
import requests
import json
import time
from streamlit_autorefresh import st_autorefresh

st.set_page_config(
    page_title="Streaming Churn Prediction",
    layout="wide"
)

st.title("Real-Time Customer Churn Prediction")

st_autorefresh(interval=10000, key="refresh")

# ---------------- Form ---------------- #

col1, col2 = st.columns(2)

with col1:

    gender = st.selectbox("Gender", ["Male", "Female"])
    SeniorCitizen = st.selectbox("Senior Citizen", [0, 1])
    Partner = st.selectbox("Partner", ["Yes", "No"])
    Dependents = st.selectbox("Dependents", ["Yes", "No"])
    tenure = st.slider("Tenure", 0, 72, 12)
    PhoneService = st.selectbox("Phone Service", ["Yes", "No"])

    MultipleLines = st.selectbox(
        "Multiple Lines",
        ["Yes", "No", "No phone service"]
    )

    InternetService = st.selectbox(
        "Internet Service",
        ["DSL", "Fiber optic", "No"]
    )

    OnlineSecurity = st.selectbox(
        "Online Security",
        ["Yes", "No", "No internet service"]
    )

with col2:

    OnlineBackup = st.selectbox(
        "Online Backup",
        ["Yes", "No", "No internet service"]
    )

    DeviceProtection = st.selectbox(
        "Device Protection",
        ["Yes", "No", "No internet service"]
    )

    TechSupport = st.selectbox(
        "Tech Support",
        ["Yes", "No", "No internet service"]
    )

    StreamingTV = st.selectbox(
        "Streaming TV",
        ["Yes", "No", "No internet service"]
    )

    StreamingMovies = st.selectbox(
        "Streaming Movies",
        ["Yes", "No", "No internet service"]
    )

    Contract = st.selectbox(
        "Contract",
        ["Month-to-month", "One year", "Two year"]
    )

    PaperlessBilling = st.selectbox(
        "Paperless Billing",
        ["Yes", "No"]
    )

    PaymentMethod = st.selectbox(
        "Payment Method",
        [
            "Electronic check",
            "Mailed check",
            "Bank transfer (automatic)",
            "Credit card (automatic)"
        ]
    )

    MonthlyCharges = st.number_input(
        "Monthly Charges",
        min_value=0.0,
        value=70.0
    )

    TotalCharges = st.number_input(
        "Total Charges",
        min_value=0.0,
        value=1000.0
    )

# ---------------- Send Data ---------------- #

if st.button("Start Streaming Prediction"):

    payload = {
        "gender": gender,
        "SeniorCitizen": SeniorCitizen,
        "Partner": Partner,
        "Dependents": Dependents,
        "tenure": tenure,
        "PhoneService": PhoneService,
        "MultipleLines": MultipleLines,
        "InternetService": InternetService,
        "OnlineSecurity": OnlineSecurity,
        "OnlineBackup": OnlineBackup,
        "DeviceProtection": DeviceProtection,
        "TechSupport": TechSupport,
        "StreamingTV": StreamingTV,
        "StreamingMovies": StreamingMovies,
        "Contract": Contract,
        "PaperlessBilling": PaperlessBilling,
        "PaymentMethod": PaymentMethod,
        "MonthlyCharges": MonthlyCharges,
        "TotalCharges": TotalCharges
    }

    try:

        response = requests.post(
            "http://backend:8000/predict",
            json=payload
        )

        result = response.json()

        st.success(result["message"])

    except Exception as e:

        st.error(f"Error: {e}")

# ---------------- Fetch Latest Prediction ---------------- #


st.subheader("Latest Streaming Prediction")

try:

    response = requests.get(
        "http://backend:8000/latest_prediction"
    )

    result = response.json()

    if "prediction" in result:

        if result["prediction"] == "Yes":

            st.error(
                f"""
                Customer will churn

                Probability: {result['probability']}%
                """
            )

        else:

            st.success(
                f"""
                Customer will stay

                Probability: {result['probability']}%
                """
            )

    else:

        st.info("Waiting for streaming prediction...")

except Exception as e:

    st.warning(f"Error fetching prediction: {e}")
