FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install required system packages for Chromium and Xvfb
RUN apt-get update && apt-get install -y \
    wget curl ca-certificates \
    fonts-liberation libappindicator3-1 libasound2 libatk-bridge2.0-0 \
    libatk1.0-0 libcups2 libdbus-1-3 libdrm2 libxcomposite1 libxdamage1 \
    libxrandr2 libxss1 libxtst6 xauth xvfb \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Playwright + deps
RUN pip install playwright && playwright install --with-deps

# Set working directory
WORKDIR /app

# Copy your local code into the image
COPY . .

# Install your Python package from local source
RUN pip install .

# Default command (can be overridden at runtime)
ENTRYPOINT ["zoomeyesearch"]

