FROM ubuntu:latest

RUN apt-get update -y
RUN apt-get install python3.6

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8080

ENTRYPOINT ["python3", "app.py"]