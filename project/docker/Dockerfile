# pull official base python3 image
FROM python:3.8

# set environment variables
# prevent writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# prevent buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# create work directory
RUN mkdir /code
WORKDIR /code

# install dependencies
RUN pip install --upgrade pip
# COPY requirements.txt /code/
ADD requirements.txt /code/
RUN pip install -r requirements.txt

# CMD sudo -u postgres psql -f sql/init.sql
# CMD psql -U toggleme -d project -f sql/create.sql
# CMD psql -U toggleme -d project -f sql/test_data.sql
# CMD python ./project/generate_cards.py

COPY . /code/

# CMD [ "python3", "manage.py", "migrate", "--no-input" ]
# CMD [ "psql", "manage.py", "migrate", "--no-input" ]
