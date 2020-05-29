FROM python:3.7.4

WORKDIR /app

RUN pip3 install --upgrade pip
RUN pip3 install pipenv

COPY python/Pipfile.lock ./

RUN pipenv install --ignore-pipfile

COPY python/app.py ./

ENTRYPOINT ["pipenv","run"]

CMD ["gunicorn","--bind","0.0.0.0:5000","app:app"]
