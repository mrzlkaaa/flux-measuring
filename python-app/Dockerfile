FROM python:3
ADD . /python-flask
WORKDIR /python-flask
RUN pip install -r requirements.txt
COPY . .
# EXPOSE 5000
CMD gunicorn --bind 0.0.0.0:5000 -w 3 wire_app:app
# ENTRYPOINT [ "gunicorn" ]
# CMD ["wire_app.py"]
# ENTRYPOINT [ "python" ]