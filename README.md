# 🚀 Real-Time Customer Churn Prediction System

A cloud-native **Real-Time Streaming Machine Learning System** that predicts customer churn using **Apache Kafka**, **FastAPI**, **Streamlit**, **Docker**, and **Scikit-learn**.

Unlike traditional ML applications that perform direct synchronous predictions, this project implements an **event-driven producer-consumer architecture** with a managed **Aiven Cloud Kafka Cluster** for asynchronous real-time inference.

---

## 🌐 Live Demo
🚀 **[Launch Live Application](https://customer-churn-prediction-fullstack-mlops.onrender.com)**

[![Live Demo](https://img.shields.io/badge/Live-Demo-success?style=for-the-badge)](https://customer-churn-prediction-fullstack-mlops.onrender.com)

---

## 📌 Project Overview

This project predicts whether a telecom customer is likely to churn based on their subscription and usage information.

The system streams incoming customer records through a cloud-hosted Kafka cluster, where they are processed asynchronously by a dedicated consumer service that performs machine learning inference in real time.

---

## 🏗️ System Architecture

```text
┌─────────────────┐
│  Streamlit UI   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ FastAPI Backend │
│ (Kafka Producer)│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Aiven Cloud     │
│ Kafka Cluster   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Kafka Consumer  │
│ ML Inference    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Live Prediction │
│ Results         │
└─────────────────┘
```

---

## ⚡ Workflow

### 1️⃣ Data Ingestion

* User enters customer details through the Streamlit UI.
* FastAPI receives the customer data through REST APIs.

### 2️⃣ Event Streaming

* FastAPI acts as a Kafka Producer.
* Customer records are serialized and published to the Kafka topic.

### 3️⃣ Real-Time Processing

* Kafka Consumer continuously listens for incoming events.
* The trained Machine Learning pipeline performs churn prediction.

### 4️⃣ Live Result Updates

* Prediction results are updated in real time.
* Streamlit automatically refreshes and displays the latest inference result.

---

## 🛠️ Tech Stack

### Machine Learning

* Scikit-learn
* Pandas
* NumPy
* Joblib

### Backend

* FastAPI
* Uvicorn

### Frontend

* Streamlit

### Streaming Infrastructure

* Apache Kafka
* Kafka Producer
* Kafka Consumer
* Aiven Cloud Kafka

### DevOps & Deployment

* Docker
* Render
* GitHub

---

## ✨ Key Features

✅ Real-Time Streaming Inference

✅ Event-Driven Architecture

✅ Cloud Kafka Integration

✅ Producer-Consumer Pattern

✅ Dockerized Deployment

✅ Live Prediction Updates

✅ Scalable ML Pipeline

✅ REST API Integration

---

## 📂 Project Structure

```text
Customer_Churn_Streaming_Project/
│
├── backend/
│   ├── main.py
│   └── Dockerfile
│
├── frontend/
│   ├── streamlit_app.py
│   └── Dockerfile
│
├── consumer/
│   └── consumer.py
│
├── models/
│   └── churn_pipeline.pkl
│
├── src/
│   └── train.py
│
├── requirements.txt
├── start.sh
└── README.md
```

---

## 🤖 Machine Learning Pipeline

The churn prediction model is trained using customer demographic and service usage features such as:

* Gender
* Senior Citizen
* Contract Type
* Internet Service
* Monthly Charges
* Total Charges
* Tenure
* Payment Method
* Online Services

The trained preprocessing and prediction pipeline is serialized using Joblib and used for real-time inference.

---

## 🚀 Running Locally

### Clone Repository

```bash
git clone https://github.com/MrAkash/End-to-End-MLOps-Pipeline-for-Real-Time-Streaming-Inference.git
cd End-to-End-MLOps-Pipeline-for-Real-Time-Streaming-Inference
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Application

```bash
bash start.sh
```

### Open Browser

```text
http://localhost:8501
```

---

## 📈 Future Enhancements

* 🔹 Redis for result caching
* 🔹 PostgreSQL for prediction history
* 🔹 MLflow for experiment tracking
* 🔹 Kubernetes deployment
* 🔹 CI/CD Automation
* 🔹 Real-time monitoring dashboard

---

## 💡 Learning Outcomes

Through this project, I gained hands-on experience with:

* Event-Driven System Design
* Real-Time Streaming Architectures
* Apache Kafka Fundamentals
* Producer-Consumer Communication
* Cloud-Based Messaging Systems
* End-to-End MLOps Workflows
* Dockerized Deployments
* Full-Stack Machine Learning Applications

---

## 👨‍💻 Author

### Akash Kadam

🔗 GitHub: https://github.com/MrAkash

⭐ If you found this project helpful, consider giving it a star!
