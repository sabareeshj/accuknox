# Use the official Python image as the base image
FROM python:3.8

# Set environment variables for running in production
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE accuknox_social.settings

# Create and set the working directory
RUN mkdir /app
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files into the container
COPY . /app/

# Expose the port the application runs on
EXPOSE 8000

# Start the application
CMD ["gunicorn", "accuknox_social.wsgi:application", "--bind", "0.0.0.0:8000"]
