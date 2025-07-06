# Use Python base image
FROM python:3.11-slim

# Set working dir
WORKDIR /app

# Install system dependencies (for Chromium)
RUN apt-get update && apt-get install -y \
    wget curl unzip gnupg ca-certificates \
    fonts-liberation libappindicator3-1 libasound2 libatk-bridge2.0-0 \
    libatk1.0-0 libcups2 libdbus-1-3 libgdk-pixbuf2.0-0 libnspr4 \
    libnss3 libxcomposite1 libxdamage1 libxrandr2 xdg-utils libgbm1 libxshmfence-dev \
    chromium chromium-driver

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright and its browsers
RUN python -m playwright install

# Copy app
COPY . .

# Run your app (e.g., streamlit)
CMD ["streamlit", "run", "main.py", "--server.port=10000", "--server.address=0.0.0.0"]
