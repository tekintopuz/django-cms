FROM python:3.11.5-slim-bookworm AS app

RUN apt-get update \
  && apt-get install -y --no-install-recommends build-essential curl libpq-dev \
  && rm -rf /var/lib/apt/lists/* /usr/share/doc /usr/share/man \
  && apt-get clean

# Requirements are installed here to ensure they will be cached.
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt


COPY ./compose/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start


RUN mkdir /app
RUN mkdir /app/static
RUN mkdir /app/media

WORKDIR /app
# copy project code
COPY . .

#RUN chown -R django:django /app
#
RUN chmod -R 755 /app