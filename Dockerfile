# Use a base Python image based on a modern Debian release for stability and size efficiency
FROM python:3.10-slim-bullseye

# Set the working directory inside the container
WORKDIR /app

# --- Install system dependencies ---
# build-essential is included as a general safeguard for any underlying C extensions
# that might be part of Python packages, though often not strictly necessary for pure API clients.
RUN apt-get update && apt-get install -y \
    build-essential \
    # Clean up apt cache to reduce image size
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and setuptools to ensure compatibility with newer packages and better build reliability
RUN pip install --upgrade pip setuptools

# Copy your requirements.txt file into the container
COPY requirements.txt .

# Install Python dependencies from requirements.txt
# --no-cache-dir reduces the image size by not storing pip's cache
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code into the container
COPY . .

# Expose the port your application will listen on. This is a declaration.
EXPOSE 8000

# Command to run your application using Uvicorn.
# We explicitly set the port to 8000, aligning with common deployment configurations
# where the platform maps external traffic to this internal port.
# Using the exec form (square brackets) is generally preferred for proper signal handling.
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]