FROM python:3-slim
COPY . /app
RUN pip install /app
WORKDIR /app
