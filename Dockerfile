# Dockerfile CIAL_TEST

# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /stocks_api

# Copy the requirements file into the container
COPY requirements.txt /stocks_api/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project code into the container
COPY . /stocks_api

# Expose the Django port
EXPOSE 8000

# Run Django migrations and start the server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]