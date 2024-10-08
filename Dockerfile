# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app/

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run migrations, collect static files, and start the server
CMD ["sh", "-c", "python manage.py migrate && gunicorn djtest.wsgi:application --bind 0.0.0.0:8000"]
