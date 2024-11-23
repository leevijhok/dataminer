# Use a lightweight Python image
FROM python:3.9-slim

# Set environment variables to disable buffering and install Poetry without venv
ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.7.0 \
    POETRY_VIRTUALENVS_CREATE=false

# Install dependencies for Poetry and other necessary system dependencies
RUN apt-get update && \
    apt-get install -y curl git build-essential && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Set the working directory in the container
WORKDIR /app

# Copy the poetry files to the working directory
COPY pyproject.toml poetry.lock /app/

# Install project dependencies
RUN poetry install --no-root

# Copy the rest of the application code into the container
COPY . /app

# Ensure the entry point has execution permission
RUN chmod +x /app

# Use ENTRYPOINT to forward arguments to scripts.py
ENTRYPOINT ["poetry", "run", "python", "scripts.py"]
