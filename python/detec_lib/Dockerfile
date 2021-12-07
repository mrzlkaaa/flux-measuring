FROM python:3
ADD . /python-lib
WORKDIR /python-lib
RUN pip install -r requirements.txt
COPY . .
# EXPOSE 5000
CMD gunicorn --bind 0.0.0.0:5000 -w 3 detec_lib_app:app
# ENTRYPOINT [ "gunicorn" ]
# CMD ["wire_app.py"]
# ENTRYPOINT [ "python" ]