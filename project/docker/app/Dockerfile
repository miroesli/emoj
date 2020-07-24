# See: https://concisecoder.io/2019/01/12/how-to-dockerize-django-and-postgres/

# pull official base python3 image
FROM python:3.8

# create work directory
COPY requirements.txt /code/
WORKDIR /code/

# install dependencies
RUN pip install -r requirements.txt

COPY . /code/

CMD [ "./docker/app/startup.sh" ]
