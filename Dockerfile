# Use a minimal Python base image
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Copy only the necessary files
COPY src/ /app/src
COPY Pipfile /app/
COPY Pipfile.lock /app/

# Install pipenv
RUN pip install --no-cache-dir pipenv

# Install system dependencies
RUN apt-get update && \
    apt-get install -y libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# Install project dependencies
RUN pipenv install --system

# Install signalrcore separately // dont know why pipenv install doesnt install signalrcore even though it is specified in the pipfile.
RUN pipenv install signalrcore



# Run the application
CMD ["pipenv", "run", "python", "src/main.py"]
