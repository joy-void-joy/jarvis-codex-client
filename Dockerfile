FROM python:3.9-alpine
MAINTAINER ^,^ joyvoidjoy@gmail.com
WORKDIR /
RUN apk add git

COPY requirements.txt /
RUN pip install -r /requirements.txt
COPY client /client
COPY .env.default /
ENTRYPOINT ["python", "-m", "client"]
