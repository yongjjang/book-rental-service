FROM tiangolo/uwsgi-nginx-flask:python3.8

RUN apt-get update

RUN apt-get install -y python3-pip python3-dev



COPY ./app /app

RUN pip3 install -r /app/requirements.txt
