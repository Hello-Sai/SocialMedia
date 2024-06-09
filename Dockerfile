# Use the official Python base image
FROM python:3.10.7


# Set the working directory in the container
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
# Install dependencies
COPY . .
EXPOSE 8000


# Copy the project code into the container
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
