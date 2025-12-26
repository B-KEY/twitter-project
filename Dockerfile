FROM python:3.12-slim

# Install system dependencies for ADB and uiautomator2
RUN apt-get update && apt-get install -y \
    android-tools-adb \
    android-tools-fastboot \
    libxml2-dev \
    libxslt-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create necessary directories
RUN mkdir -p ui_dumps templates static

# Set environment variable for Python to run in unbuffered mode
ENV PYTHONUNBUFFERED=1

# Expose port for web interface
EXPOSE 5000

# Default command - run web app (can be overridden)
CMD ["python", "src/web_app.py"]
