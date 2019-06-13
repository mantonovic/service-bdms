# Borehole Management System Service

## Installation

### Databasa initilization

Create the database

```bash
sudo -u postgres createdb -E UTF8 bdms
```

Create the tables:

```bash
sudo -u postgres psql -d bdms -f db.sql
```

Add default data:

```bash
sudo -u postgres psql -d bdms -f data.sql
sudo -u postgres psql -d bdms -f cantons.sql
sudo -u postgres psql -d bdms -f municipalities.sql
```

### Python env



### Run Server

```bashm
python3 bms/main.py 
```

## Developer corner

Setup developer environment

```bash
python3 -m venv ./venv
source venv/bin/activate
pip3 install --upgrade pip
pip3 install jsonschema \
  pytest \
  dateutils \
  tornado \
  asyncpg
```

Activate virtual environment

```bash
source venv/bin/activate
```

Run Server

```bashm
python3 bms/main.py -c assets/config.json
```
