ARG DOCKER_MIRROR_URL=docker.arvancloud.ir

FROM ${DOCKER_MIRROR_URL}/python:3.11.4-slim-buster

ARG PYPI_INDEX_URL=https://mirrors.aliyun.com/pypi/simple

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install -i ${PYPI_INDEX_URL} --upgrade pip
COPY 3rdparty/requirements.txt .
RUN pip install -i ${PYPI_INDEX_URL} -r requirements.txt

ENTRYPOINT [ "python", "manage.py" ]
