FROM python:3.4
ENV PYTHONUNBUFFERED 1
RUN mkdir /config
ADD /config/requirements.pip /config/
RUN pip install -r /config/requirements.pip
RUN mkdir /src
CMD python3 manage.py collectstatic --no-input;python3 manage.py migrate; gunicorn --timeout 120 ilusiones.wsgi -b 0.0.0.0:8000;


WORKDIR /src



