FROM python:alpine

LABEL Name=gio-device-ms Version=0.0.1
EXPOSE 5000

WORKDIR /app
ADD . /app

RUN pip install -e .

ENV FLASK_APP=gfndevice
ENV FLASK_ENV=development

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]