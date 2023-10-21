FROM python:3.10-alpine

LABEL maintainer="Joker-desire <yangyindesire@gmail.com>"

COPY . /home/fastapi/

RUN pip3 install -r /home/fastapi/requirements.txt

WORKDIR /home/fastapi/

CMD ["/bin/sh", "/home/fastapi/start.sh"]