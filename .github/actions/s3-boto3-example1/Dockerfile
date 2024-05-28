FROM python:3

COPY requirements.txt /requirements.txt

RUN pip install -r requirements.txt

COPY s3-boto3-e1.py /s3-boto3-e1.py

CMD ["python", "/s3-boto3-e1.py"]