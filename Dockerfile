FROM python:3.11-slim

WORKDIR /app

# Copy the single requirements file from your root directory
COPY requirements.txt .

# Install all project dependencies at once
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your entire project code
COPY . .

# Make the startup execution script executable
RUN chmod +x start.sh

CMD ["./start.sh"]