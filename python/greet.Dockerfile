FROM python:3
WORKDIR /python-app/greetings
COPY ./greetings /python-app/greetings
COPY ./templates/greetings /python-app/templates/greetings
COPY ./templates/base.html /python-app/templates/base.html
COPY ./static/greetings /python-app/static/greetings
RUN pip install -r requirements.txt
COPY . .
# EXPOSE 5000
CMD gunicorn --bind 0.0.0.0:5002 -w 3 app:app
# ENTRYPOINT [ "gunicorn" ]
# CMD ["wire_app.py"]
# ENTRYPOINT [ "python" ]