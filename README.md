# Borehole Management System Service

Setup developer environment

```bash
python3 -m venv ./venv
source venv
pip3 install --upgrade pip
pip3 install psycopg2-binary \
  momoko \
  jsonschema \
  pytest \
  dateutils \
  tornado
```

Activate virtual environment

```bash
source venv/bin/activate
```

Run Server

```bashm
python3 bms/main.py -c assets/config.json
```
