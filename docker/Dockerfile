# Use the official Python image
FROM python:3.12.0

# Set the working directory in the container
WORKDIR /app

# Copy the Pipfile and Pipfile.lock to the working directory
COPY Pipfile Pipfile.lock /app/

# Install pipenv and dependencies
RUN pip install pipenv && pipenv install --deploy --system

# Copy the rest of the application code
COPY . /app

# Command to run the FastAPI application with Uvicorn worker
CMD ["pipenv", "run", "fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]