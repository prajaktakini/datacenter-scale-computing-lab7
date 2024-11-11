FROM xserrat/facebook-demucs:latest

RUN pip3 install jsonpickle redis minio demucs requests
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=development
ENV FLASK_APP=rest-server.py
ENV FLASK_DEBUG=1
WORKDIR /data

COPY worker.py /data

ENTRYPOINT [ "python3", "worker.py" ]