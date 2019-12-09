FROM python:3.8.0-slim-buster
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 8081
CMD ["python3", "src/api_environment.py" ]
