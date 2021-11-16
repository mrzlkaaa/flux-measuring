FROM python:3
ADD . /python-flask
WORKDIR /python-flask
RUN pip install -r requirements.txt
COPY . .
CMD ["wire_app.py"]
ENTRYPOINT [ "python" ]