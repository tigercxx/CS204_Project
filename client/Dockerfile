FROM ubuntu:20.04

RUN apt update \
    && DEBIAN_FRONTEND=noninteractive apt install -y \
    wget \
    gpg

RUN mkdir -p /etc/apt/keyrings && \
    touch /etc/apt/keyrings/google-chrome.gpg

ENV TZ=Asia/Kolkata \
    DEBIAN_FRONTEND=noninteractive

RUN wget https://dl-ssl.google.com/linux/linux_signing_key.pub -O /tmp/google.pub && \
    gpg --no-default-keyring --keyring /etc/apt/keyrings/google-chrome.gpg --import /tmp/google.pub && \
    echo 'deb [arch=amd64 signed-by=/etc/apt/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main' | tee /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    apt --fix-broken install

RUN apt install curl -y

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apt install python3-pip -y

RUN pip3 install -r requirements.txt

COPY client.py client.py

CMD ["tail", "-f", "/dev/null"]
