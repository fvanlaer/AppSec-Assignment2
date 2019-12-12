FROM python:3.6-alpine

#RUN apt-get update -y
#RUN apt-get install -y python3.6
#RUN apt-get install -y python-pip python-dev

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 5000

ENTRYPOINT ["python", "app.py"]