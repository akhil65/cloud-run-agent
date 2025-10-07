# Use an official lightweight Python image as the base
FROM python:3.9-slim

# Set the working directory inside the container to /app
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python libraries from the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# Copy our app.py file into the container
COPY . .

# Tell Docker that the container will listen on port 5000
EXPOSE 5000

# This command runs when the container starts
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]# Use an official lightweight Python image as the base
FROM python:3.9-slim

# Set the working directory inside the container to /app
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python libraries from the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# Copy our app.py file into the container
COPY . .

# Tell Docker that the container will listen on port 5000
EXPOSE 8080

# This command runs when the container starts
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"] 
