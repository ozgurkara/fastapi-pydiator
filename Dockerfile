FROM python:3.8

RUN mkdir src

COPY requirements.txt src
COPY app src/app
COPY .env src
COPY main.py src

WORKDIR src
RUN pip install -r requirements.txt

EXPOSE 8081
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8081"]