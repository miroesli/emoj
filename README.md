# Emoj

Seng 499 project by Emily, Misha, Oleg, and Juan.

## Requirements

- Python3
- Postgres 12
- Virtualenv

## Running locally

### Step 1: Clone or fork the repository and change current directory

```bash
git clone https://github.com/miroesli/emoj.git
cd emoj
```

### Step 2: Install python3

```bash
sudo apt install python3
```

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
sudo -u postgres psql -f project/sql/create.sql
# or
psql -U toggleme -d project -f project/sql/create.sql
```

### Step 6: Run the server

```bash
python3 project/manage.py runserver 8000
```

### Step 7: View Application

Access the server in browser at `http://localhost:8000`
