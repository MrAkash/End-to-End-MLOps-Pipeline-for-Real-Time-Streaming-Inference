import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import ssl
from kafka import KafkaProducer
import json
import time

app = FastAPI()
os.makedirs("results", exist_ok=True)
# ---------------- CORS ---------------- #

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- Kafka ---------------- #

TOPIC_NAME = "customer-churn"
BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
KAFKA_USER = os.getenv("KAFKA_USERNAME")
KAFKA_PASS = os.getenv("KAFKA_PASSWORD")

producer = None

while True:
    try:
        print(f"Connecting to Kafka at {BOOTSTRAP_SERVERS}...")
        
        kafka_kwargs = {
            "bootstrap_servers": BOOTSTRAP_SERVERS,
            "value_serializer": lambda v: json.dumps(v).encode("utf-8")
        }
        
        # If cloud credentials exist, activate secure SASL connection
        if KAFKA_USER and KAFKA_PASS:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            
            kafka_kwargs.update({
                "security_protocol": "SASL_SSL",
                "sasl_mechanism": "SCRAM-SHA-256",
                "sasl_plain_username": KAFKA_USER,
                "sasl_plain_password": KAFKA_PASS,
                "ssl_context": context
            })

        producer = KafkaProducer(**kafka_kwargs)
        print("Kafka Producer connected successfully!")
        break
    except Exception as e:
        print(f"Kafka Producer connection waiting: {e}")
        time.sleep(5)

# ---------------- Schema ---------------- #

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

# ---------------- Routes ---------------- #

@app.get("/")
def home():
    return {"message": "Streaming Backend Running"}

@app.post("/predict")
def predict(data: CustomerData):

    try:

        payload = data.dict()

        producer.send(TOPIC_NAME, value=payload)
        producer.flush()

        return {
            "status": "success",
            "message": "Data sent to streaming pipeline"
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }

@app.get("/latest_prediction")
def latest_prediction():

    try:

        with open("results/prediction_result.json", "r") as f:
            result = json.load(f)

        return result

    except Exception as e:

        return {
            "message": "No prediction yet",
            "error": str(e)
        }
