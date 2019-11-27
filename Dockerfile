FROM python:3.8.0-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8080

CMD [ "python", "src/api_environment.py" ]
