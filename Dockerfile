# Use Python 3.12 slim image
FROM python:3.12-slim

# Avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies needed for some Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    git \
    curl \
    libatlas3-base \
    liblapack3 \
    libblas3 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Upgrade pip
RUN python -m pip install --upgrade pip

# Fix pandas version and install dependencies
RUN sed -i 's/^pandas>=1.5.0/pandas>=2.3.3/' requirements.txt && \
    pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose Flask port
EXPOSE 5000

# Run your actual Flask app
CMD ["python", "web_prototype.py"]
