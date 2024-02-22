FROM python:3.11-slim

RUN apt-get update && \
    apt-get -y install gcc && \
    rm -rf /var/lib/apt/lists/*
#RUN apt install uwsgi-plugin-python3

COPY requirements.prod.txt /requirements.txt
ENV PATH="/root/.local/bin:${PATH}"

RUN pip install -r /requirements.txt \
    --no-cache-dir \
    --trusted-host pypi.python.org \
    --trusted-host files.pythonhosted.org

COPY src /src
RUN useradd --create-home --shell /bin/bash uwsgi \
    && chown -R uwsgi /src

WORKDIR /src

ENV DB_URI=sqlite:////src/test.sqlite
ENV API_PORT=5000
ENV AUTO_DB_META=1

EXPOSE 5000
VOLUME /var/log/adp

COPY entrypoint.sh /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
