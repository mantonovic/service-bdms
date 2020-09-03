#!/bin/sh

set -e

psql -U $POSTGRES_USER -d $POSTGRES_DB -f 1_schema.sql
psql -U $POSTGRES_USER -d $POSTGRES_DB -f 2_geolcodes.sql
psql -U $POSTGRES_USER -d $POSTGRES_DB -f 3_data.sql
psql -U $POSTGRES_USER -d $POSTGRES_DB -f 4_cantons.sql
psql -U $POSTGRES_USER -d $POSTGRES_DB -f 5_municipalities.sql

