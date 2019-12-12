FROM python:3.6-alpine

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY app.py config.py database.py forms.py loginman.py models.py routes.py ./

EXPOSE 8080
ENTRYPOINT ["python", "app.py"]
