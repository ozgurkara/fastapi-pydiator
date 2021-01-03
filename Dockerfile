FROM python:3.8

RUN mkdir /src
COPY app /src/app
COPY .env /src
COPY requirements.txt /src
COPY main.py /src
#COPY . /src

WORKDIR /src
RUN pip install -r requirements.txt


RUN ls

EXPOSE 8080
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]