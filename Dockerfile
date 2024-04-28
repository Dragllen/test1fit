FROM python:3.10
RUN mkdir /app
WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN apt-get update && \
    apt-get install -y python3 python3-pip

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /app

ENTRYPOINT ["tail", "-f", "/dev/null"]
