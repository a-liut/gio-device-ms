FROM python:alpine

LABEL Name=gio-device-ms Version=0.0.1
EXPOSE 5000

WORKDIR /app

ADD ./setup.cfg /app/setup.cfg
ADD ./setup.py /app/setup.py
ADD ./README.rst /app/README.rst
RUN pip install -e .

ADD . /app

ENV FLASK_APP=gfndevice
ENV FLASK_ENV=development

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]