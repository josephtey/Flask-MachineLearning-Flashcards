FROM python:3

ADD requirements /flask-requirements

RUN pip install -r /flask-requirements/dev.txt

EXPOSE 5000

CMD [ "python3", "/flask/manage.py", "runserver", "--host=0.0.0.0"]
