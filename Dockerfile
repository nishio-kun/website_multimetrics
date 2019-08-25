FROM python:3.7
ENV PYTHONUNBUFFERED 1

RUN mkdir /website_multimetrics

ADD requirements.txt /website_multimetrics/
WORKDIR website_multimetrics/

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

ADD . /website_multimetrics/

ENTRYPOINT python main.py
