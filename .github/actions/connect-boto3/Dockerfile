FROM python:3.11-slim

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY connect-boto3-e1.py /connect-boto3-e1.py

CMD ["python", "/connect-boto3-e1.py"]
