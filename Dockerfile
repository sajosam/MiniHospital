# Use the official Python base image with version 3.9
FROM python:3.10.0a6-alpine3.13

# Set the working directory inside the container
WORKDIR /miniHospital

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip3 install -r requirements.txt

# Copy the entire project directory into the container
COPY . .

# Expose the port on which your Django app will run (change it to the appropriate port)
EXPOSE 8000

# Set the environment variables for Django
ENV DJANGO_SETTINGS_MODULE=minihospital.settings

# Run the Django development server when the container starts
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
