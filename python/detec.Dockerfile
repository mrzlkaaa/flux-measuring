FROM python:3
WORKDIR /python-app/detectors
COPY ./detectors /python-app/detectors
COPY ./templates/detectorsApp /python-app/templates/detectorsApp
COPY ./templates/base.html /python-app/templates/base.html
COPY ./static/detectorsApp /python-app/static/detectorsApp
RUN pip install -r requirements.txt
# COPY ./detectors ./python/detectors
# EXPOSE 5000
CMD gunicorn --bind 0.0.0.0:5000 -w 3 detectors_app:app
# ENTRYPOINT [ "gunicorn" ]
# CMD ["wire_app.py"]
# ENTRYPOINT [ "python" ]