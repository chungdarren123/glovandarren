# Step 1: Use an official Python runtime as a parent image
FROM python:3.9-slim

# Step 2: Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Set default DATABASE_URL if not overridden by docker-compose or .env
ENV DATABASE_URL sqlite:///./sql_app.db

# Step 3: Set the working directory in the container
WORKDIR /app_engine

# Step 4: Install system dependencies (if any)
# RUN apt-get update && apt-get install -y --no-install-recommends some-package && rm -rf /var/lib/apt/lists/*

# Step 5: Install Python dependencies
# Copy only requirements.txt first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Step 6: Copy the rest of the application code into the container
COPY . .
# The above COPY . . will copy the entire build context (respecting .dockerignore)
# This includes the 'app' directory, 'main.py', '.env' (if not in .dockerignore), etc.

# Step 7: Expose the port the app runs on
EXPOSE 8000

# Step 8: Define the command to run the application
# This will run the FastAPI app using Uvicorn.
# The main:app refers to main.py and the app FastAPI instance within it.
# The on_startup event in main.py will create DB tables if they don't exist.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
