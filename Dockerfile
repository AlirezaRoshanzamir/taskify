FROM python:3.11.4-slim-buster

ARG PYPI_INDEX_URL="https://pypi.org/simple"

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install -i ${PYPI_INDEX_URL} --upgrade pip
COPY 3rdparty/requirements.txt .
RUN pip install -i ${PYPI_INDEX_URL} -r requirements.txt

# COPY . .

ENTRYPOINT [ "python", "manage.py" ]

CMD [ "runserver", "0.0.0.0:8000" ]
