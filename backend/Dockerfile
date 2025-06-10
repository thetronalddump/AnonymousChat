FROM python:3.13
LABEL authors="mbchl"

WORKDIR /backend

COPY requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "./main.py"]