#
FROM python:3.9

#
LABEL maintainer="helge.stein@kit.edu"

#
WORKDIR /code

#
COPY ./requirements.txt /code/requirements.txt
ENV PATH /home/paolovincenzofreieslebendeblasio/.local/bin:${PATH}
#
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#
COPY ./app /code/app

#
EXPOSE 13371

#
#CMD ["uvicorn", "app.broker_server:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "13371"]

CMD ["python3" , "app/broker_server.py"]
