# Emoj

Seng 499 project by Emily, Misha, Oleg, and Juan.

## Requirements

- Python3
- Postgres 12
- Virtualenv

## Running locally

Step 1: Clone or fork the repository and change current directory

```bash
git clone https://github.com/miroesli/emoj.git
cd emoj
```

Step 2: Install python3

```bash
sudo apt install python3
```

Step 3: Install postgres 12

```bash
sudo apt install postgresql postgresql-contrib
```

Step 4: Get python packages

**Option 1:** Locally

```bash
python -m pip install django psycopg2-binary
```

**Option 2:** Using virtualenv

Install virtualenv

```bash
pip3 install virtualenv
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

Step 5: Create the database

```bash
sudo -u postgres psql -f init.sql
sudo -u postgres psql -f create.sql
```

Step 6: Run the server

```bash
python3 project/manage.py runserver 8000
```

Step 7: Access server in browser at `http://localhost:8000`
