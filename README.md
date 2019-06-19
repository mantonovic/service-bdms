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

## Run with docker

### Installation

Docker install:

```bash
sudo apt-get remove docker docker-engine docker.io containerd runc
sudo apt-get update
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
```

Git install:

```bash
sudo apt-get install git
```

### Build image and run docker

Clone server repository:

```bash
git clone https://github.com/geoadmin/bdms-service
cd bdms-service
```

Build Docker image:

```bash
 sudo docker build -t swisstopo/bdms:1.0.0 ./config
```

Run Docker container:

```bash
sudo docker run -d --name bdmsContainer -p 80:80 swisstopo/bdms:1.0.0
```
