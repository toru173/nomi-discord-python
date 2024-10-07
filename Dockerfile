# Stage 1: Builder stage to check for requirements.txt
FROM python:3.12-slim AS builder

# Install git
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file if it exists
COPY requirements.txt .

# Install dependencies if requirements.txt exists
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the working directory
COPY . .

# Define an environment variable for the Python script
ENV PYTHON_SCRIPT=main.py

# Make the script executable
RUN chmod +x $PYTHON_SCRIPT

# Set the entrypoint to use the environment variable
ENTRYPOINT ["sh", "-c", "./$PYTHON_SCRIPT"]