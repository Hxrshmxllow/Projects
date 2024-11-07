# Step 1: Use an official Python runtime as a base image
FROM python:3.9-slim

# Step 2: Set the working directory in the container
WORKDIR /app

# Step 3: Copy requirements.txt into the container at /app
COPY requirements.txt .

# Step 4: Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the rest of the application code to /app
COPY . .

# Step 6: Expose the port the application runs on (e.g., Flask default port)
EXPOSE 5000

# Step 7: Define the command to run the application
CMD ["python", "app.py"]