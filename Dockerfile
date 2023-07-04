# Use the official Python base image with Alpine
FROM python:3.10.10-alpine

# Set the working directory inside the container
WORKDIR /miniHospital

# Install system dependencies
RUN apk update && apk add --no-cache gcc musl-dev postgresql-dev

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
`1
# Copy the entire project directory to the container
COPY . .

# Set the environment variable for Python
ENV PYTHONPATH=/miniHospital

# Set the startup command to run the Django application
CMD ["python", "miniHospital/manage.py", "runserver", "0.0.0.0:8000"]
