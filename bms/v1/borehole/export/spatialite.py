# -*- coding: utf-8 -*-
from bms.v1.action import Action
from datetime import datetime
from bms.v1.borehole import ListBorehole
import traceback
import spatialite
import tempfile

# https://docs.python.org/2/library/sqlite3.html
# https://pypi.org/project/spatialite/

class ExportSpatiaLite(Action):
    
    async def execute(self, filter={}, user=None):

        # Creating a temporary file where the 
        # SpatialLite DB will be populated
        spatia_lite_file = tempfile.NamedTemporaryFile(
            suffix='.db',
            prefix='bdms_',
            delete=False
        )

        print(spatia_lite_file.name)
        try:
            with spatialite.connect(spatia_lite_file.name) as db:
                print(db.execute('SELECT spatialite_version()').fetchone()[0])

                cur = db.cursor()
                # Create the Borehole table

                print("creating spatialite db:")
                print(" - InitSpatialMetaData")

                cur.execute("SELECT InitSpatialMetaData()")

                print(" - Creating schema")

                cur.execute("""
                    CREATE TABLE boreholes (
                        id integer NOT NULL PRIMARY KEY,
                        original_name text,
                        project_name text,
                        public_name text,
                        kind integer,

                        restriction integer,
                        restriction_until text
                    )
                """)

                cur.execute("""
                    SELECT AddGeometryColumn(
                        'boreholes', 'the_geom',
                        2056, 'POINT', 'XY');
                """)

                print(".. done.")

                # Load all the boreholes
                boreholes = await self.conn.fetch(
                    ListBorehole.get_sql_geolcode()
                )

                print(f"Loaded: {len(boreholes)} boreholes")

                for borehole in boreholes:

                    print(f'id: {borehole["id"]}')

                    sql = """
                        INSERT INTO boreholes VALUES (
                            ?,
                            ?, ?, ?,
                            ?, ?, ?,
                            GeomFromText(?, 2056)
                        )
                    """, (
                        borehole['id'],
                        borehole['original_name'],
                        borehole['project_name'],
                        borehole['public_name'],
                        borehole['kind'],
                        (
                            borehole['restriction']
                            if borehole['restriction'] is not None
                            else 'NULL'
                        ),
                        borehole['restriction_until'],
                        "POINT({} {})".format(
                            borehole['location_x'],
                            borehole['location_y']
                        )
                    )

                    print(sql)

                    cur.execute(sql)
                
                cur.commit()

            spatia_lite_file.close()

            return spatia_lite_file

        except Exception as ex:
            print(traceback.print_exc())
            spatia_lite_file.close()

        return None
