# Use a smaller base image
FROM python:3.8-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Clean up unnecessary files and packages
RUN rm -rf /var/cache/apk/*

# Define environment variable for SignalR hub URL
ENV HOST_ENV="http://159.203.50.162"
ENV HOST_TOKEN="3f0a57e541e13a3b6549"
ENV OXYGEN_T_MAX=60
ENV OXYGEN_T_MIN=20
ENV OXYGEN_DATABASE_URL="postgresql://user02eq12:E84YDXF2l5P4FkFG@157.230.69.113:5432/db02eq12"

# Run main.py when the container launches
CMD ["python", "main.py"]
