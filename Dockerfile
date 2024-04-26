FROM python:3.10
RUN mkdir /app
WORKDIR /app


COPY ./requirements.txt /app/requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app

CMD [ "python", "./main.py" ]