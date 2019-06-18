# Borehole Management System Service

## Installation

### Database initilization

Create the database

```bash
sudo -u postgres createdb -E UTF8 bdms
```

Create the tables:

```bash
sudo -u postgres psql -d bdms -f db/1_schema.sql
```

Add default data:

```bash
sudo -u postgres psql -d bdms -f db/2_data.sql
sudo -u postgres psql -d bdms -f db/3_cantons.sql
sudo -u postgres psql -d bdms -f db/4_municipalities.sql
```

## Run Server

### Setup virtual environment

```bash
python3 -m venv ./venv
source venv/bin/activate
pip3 install --upgrade pip
pip install -r requirements.txt
```

### Activate virtual environment

```bash
source venv/bin/activate
```

### Run Server

```bashm
python bms/main.py --pg_database=bdms
```

Config parameters:

```
--pg-database      PostgrSQL database name (default bms)
--pg-host          PostgrSQL database host (default localhost)
--pg-password      PostgrSQL user password (default postgres)
--pg-port          PostgrSQL database port (default 5432)
--pg-user          PostgrSQL database user (default postgres)
--port             Tornado Web port (default 8888)
```
