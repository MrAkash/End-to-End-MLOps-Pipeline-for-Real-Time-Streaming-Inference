#!/bin/bash

# 1. Start the Background ML Consumer
python consumer/consumer.py &

# 2. Start the FastAPI Backend on local port 8000
uvicorn backend.main:app --host 127.0.0.1 --port 8000 &

# 3. Start Streamlit to bind to Render's public web port
streamlit run frontend/app.py --server.port $PORT --server.address 0.0.0.0