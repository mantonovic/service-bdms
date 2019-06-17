#!/usr/bin/env python
# coding: utf-8

import psycopg2
# Connect to an existing database

conn = psycopg2.connect(
    host='localhost',
    dbname='bdms', 
    user='postgres',
    password='postgres',
    port=9432)

# Open a cursor to perform database operations
cur = conn.cursor()

sql = open('stratigraphy-p.sql','r').read()

# PARAMETERS FOR PROFILE EXTRACTION
lan='it'
idsty=6
schema='bdms'
# ==============================

cur.execute(
        sql.format( *((lan,)*11 + (schema,)*18)), (idsty,)*3
)
res = cur.fetchone()


conn.close()

import bdms_pdf as bdms

a = bdms.bdmsPdf('/home/maxi/GIT/bdms_server/myfile.pdf', res[0])
a.renderProfilePDF('it',200)
a.close()
"""
it => language
200 => scale denominator
"""

