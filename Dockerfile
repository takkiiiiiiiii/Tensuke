FROM ubuntu:25.04

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    curl \
    vim \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip3 install Flask line-bot-sdk

COPY . /app/

EXPOSE 7777

CMD ["python3", "sample.py"]