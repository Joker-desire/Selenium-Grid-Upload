FROM python:3.10-alpine

LABEL maintainer="Joker-desire <yangyindesire@gmail.com>"

COPY . /home/fastapi/

RUN pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip install -r /home/fastapi/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

WORKDIR /home/fastapi/

CMD ["/bin/sh", "/home/fastapi/start.sh"]