# Use the official Python image as a base image
FROM python:3.11-alpine as requirements-stage

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Create and activate a virtual environment
RUN python3 -m venv .venv
RUN /bin/sh -c "source .venv/bin/activate"


# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port that FastAPI will run on
# EXPOSE 8000

# Command to run your application using uvicorn
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
ENTRYPOINT [ "sh", "./scripts/launch.sh" ]
