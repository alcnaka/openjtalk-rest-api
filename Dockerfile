FROM python:3.11

RUN apt-get update \
    && apt-get -y install \
    curl \
    ffmpeg \
    open-jtalk \
    open-jtalk-mecab-naist-jdic

WORKDIR /usr/local/src/openjtalk-rest-api

COPY . /usr/local/src/openjtalk-rest-api
COPY ./data/htsvoice /usr/local/share/htsvoice

RUN pip install .

HEALTHCHECK --interval=60s --timeout=3s CMD curl -f "http://localhost:8000/hello?healthcheck" || exit 1

EXPOSE 8000

CMD [ "uvicorn", "openjtalk_rest_api.main:app", "--host", "0.0.0.0"]
