# Use an official Python runtime as a base image
FROM python:3.11-slim

# Set the working directory in the container - COMPLETE LINE BELOW
WORKDIR /app

# Copy the current directory contents into the container - COMPLETE LINE BELOW
COPY app.py /app

# Install any needed requirements - COMPLETE LINE BELOW
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
#  - COMPLETE LINE BELOW
EXPOSE 5000

# Define environment variable
ENV netname=ech-redis

# Run the application
CMD ["python", "app.py"]
