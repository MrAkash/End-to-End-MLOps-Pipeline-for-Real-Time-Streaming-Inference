import os  
from kafka import KafkaConsumer
import json
import time
import pickle
import pandas as pd
import ssl

TOPIC_NAME = "customer-churn"
BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
KAFKA_USER = os.getenv("KAFKA_USERNAME")
KAFKA_PASS = os.getenv("KAFKA_PASSWORD")

# Ensure the results directory exists inside the volume mapping
os.makedirs("results", exist_ok=True) 

# Define exact feature order used during model training
FEATURE_ORDER = [
    "gender", "SeniorCitizen", "Partner", "Dependents", "tenure", 
    "PhoneService", "MultipleLines", "InternetService", "OnlineSecurity", 
    "OnlineBackup", "DeviceProtection", "TechSupport", "StreamingTV", 
    "StreamingMovies", "Contract", "PaperlessBilling", "PaymentMethod", 
    "MonthlyCharges", "TotalCharges"
]

# ---------------- Load Model ---------------- #
with open("models/churn_pipeline.pkl", "rb") as file:
    model = pickle.load(file)

# ---------------- Kafka Consumer ---------------- #
consumer = None

while True:
    try:
        print(f"Connecting to Kafka Consumer at {BOOTSTRAP_SERVERS}...")
        
        kafka_kwargs = {
            "bootstrap_servers": BOOTSTRAP_SERVERS,
            "auto_offset_reset": "earliest",
            "enable_auto_commit": True,
            "group_id": "churn-consumer-group",
            "value_deserializer": lambda x: json.loads(x.decode("utf-8"))
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

        consumer = KafkaConsumer(TOPIC_NAME, **kafka_kwargs)
        print("Kafka Consumer connected successfully!")
        break
    except Exception as e:
        print(f"Kafka Consumer connection waiting: {e}")
        time.sleep(5)

# ---------------- Consume Messages ---------------- #
print("Waiting for messages...")
for message in consumer:
    try:
        data = message.value
        print("Received:", data)

        # Structure DataFrame and enforce strict feature ordering
        input_df = pd.DataFrame([data])
        input_df = input_df[FEATURE_ORDER] 

        prediction = model.predict(input_df)[0]
        probability = model.predict_proba(input_df)[0].max()

        result = {
            "prediction": str(prediction),
            "probability": round(float(probability) * 100, 2),
            "message": "Customer will churn" if prediction == "Yes" else "Customer will stay"
        }

        print(result)

        # Save latest result
        with open("results/prediction_result.json", "w") as f:
            json.dump(result, f)

    except Exception as e:
        print(f"Error: {e}")
