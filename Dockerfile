FROM python:3.12-alpine

WORKDIR /app

COPY app/ .

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

CMD python bears.py