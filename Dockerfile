
# pull official base image
FROM python:3.8.10

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

# collect static files
RUN python manage.py collectstatic --noinput
RUN python manage.py makemigrations
RUN python manage.py migrate

# add and run as non-root user
RUN adduser -u 123 nurs
USER nurs
# run gunicorn
CMD gunicorn medtech.wsgi:application --bind 0.0.0.0:$PORT