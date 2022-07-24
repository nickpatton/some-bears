FROM python:slim

WORKDIR /app

COPY app.py .
COPY bears.txt .
COPY requirements.txt .

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

CMD python app.py