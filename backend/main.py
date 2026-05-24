from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import joblib

app = FastAPI()

# CORS

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model

model = joblib.load("./models/churn_pipeline.pkl")


class CustomerData(BaseModel):
    gender: str
    SeniorCitizen: int
    Partner: str
    Dependents: str
    tenure: int
    PhoneService: str
    MultipleLines: str
    InternetService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str
    Contract: str
    PaperlessBilling: str
    PaymentMethod: str
    MonthlyCharges: float
    TotalCharges: float


@app.get("/")
def home():
    return {
        "message": "Customer Churn Prediction API Running"
    }


@app.post("/predict")
def predict(data: CustomerData):

    try:

        input_data = pd.DataFrame([data.dict()])

        prediction = model.predict(input_data)[0]

        probability = model.predict_proba(input_data)[0].max()

        return {
            "prediction": prediction,
            "probability": round(float(probability) * 100, 2),
            "message": "Customer will churn" if prediction == "Yes" else "Customer will stay"
        }

    except Exception as e:

        return {
            "error": str(e)
        }