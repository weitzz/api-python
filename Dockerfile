FROM python:3.11.3-slim
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt


