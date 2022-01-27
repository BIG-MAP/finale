#
FROM python:3.10

#
LABEL maintainer="helge.stein@kit.edu"

#
WORKDIR /code

#
COPY ./requirements.txt /code/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#
COPY ./app /code/app

#
EXPOSE 13371

#
CMD ["uvicorn", "app.broker_server:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "13371"]