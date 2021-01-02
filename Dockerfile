FROM python:3.7

RUN mkdir /src
COPY app /src/app
COPY .env /src
COPY requirements.txt /src

WORKDIR /src
RUN pip install -r requirements.txt

EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]