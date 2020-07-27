# Emoj

[![CircleCI](https://circleci.com/gh/miroesli/emoj.svg?style=shield)](https://circleci.com/gh/miroesli/emoj)

Seng 499 project by Emily, Misha, Oleg, and Juan.

## Requirements

- [Python 3.8](https://www.python.org/downloads/)
- [Postgres 12](https://www.postgresql.org/download/)
- [psycopg](https://www.psycopg.org/docs/install.html)
- [Virtualenv (optional)](https://virtualenv.pypa.io/en/stable/installation.html)

## Running locally

### Step 1: Clone or fork the repository and change current directory

```bash
git clone https://github.com/miroesli/emoj.git
cd emoj
```

### Step 2: Install python3 and header files

```bash
sudo apt install python3 python3-dev
```

<!-- libpq-dev? -->

### Step 3: Install postgres 12

```bash
sudo apt install postgresql postgresql-contrib
```

### Step 4: Get python packages

```bash
python -m pip install -r requirements.txt
```

#### Consider using virtualenv (Optional)

Install virtualenv

```bash
pip3 install virtualenv
```

Create an env directory for python3

```bash
virtualenv -p python3 env
```

Enable the virtualenv

**On Linux**

```bash
source env/bin/activate
```

**On Windows**

```bash
env\Scripts\activate.bat
```

Use `deactivate` to stop exit the environment

### Step 5: Create the database

```bash
sudo -u postgres psql -f project/sql/init.sql
psql -U toggleme -d project -f project/sql/create.sql
psql -U toggleme -d project -f project/sql/test_data.sql
```

### Step 6: Run the server

```bash
python manage.py makemigrations && python manage.py migrate
python3 project/manage.py runserver 8000
```

### Step 7: View Application

Access the server in browser at `http://localhost:8000`

## Create User

Run createsuperuser with manage.py

```bash
python manage.py createsuperuser
```

## Runnning in Docker

### Requirements

- [docker](https://docs.docker.com/engine/install/)
- [docker-compose](https://docs.docker.com/compose/install/)

### Execution

Build and run server. `-d` puts it into the background.

<!-- sudo docker build --tag emoj:1.0 . -->

```bash
docker-compose up [-d] --build
```

Migrating data in another terminal

```bash
sudo docker-compose exec web python project/generate_cards.py
sudo docker-compose exec web python manage.py migrate --no-input
```

## Testing

Change directory to the project module

```bash
cd emoj/project
```

Run the test using `manage.py`

```bash
python manage.py test
```

Alternatively to specify which test files

```bash
python manage.py test --pattern="tests_*.py"
```

### Circleci

To test circleci script see the circleci local [installation docs](https://circleci.com/docs/2.0/local-cli/#installation)
