# -*- coding: utf-8 -*-
# This script parse the geolcode CSV file and create the sql
# https://github.com/ist-supsi/data-geolcodes

import csv
import sys
import psycopg2
import json

schema = {
    "ebor102": "custom.cuttings",
    "ebor103": "extended.purpose",
    "ebor104": "extended.status",
    "ebor106": "ebor106",  # not used
    "ebor107": "extended.method",
    "ebor108": "custom.qt_top_bedrock",
    "ebor109": "custom.landuse",
    "ebor115": "custom.qt_length",
    "ebor116": "custom.qt_bore_inc_dir",
    "ibor101": "kind",
    "ibor104": "srs",
    "ibor106": "hrs",
    "ibor111": "restriction",
    "ibor113": "qt_location",
    "ibor114": "qt_elevation",
    "ibor117": "ibor117",  # not used (prima "ansatz")
    "icon407": "cantons",  # not used
    "icon408": "country",  # not used
    "mcla101": "mcla101",
    "mlpr102": "mlpr102",
    "mlpr103": "mlpr103",
    "vchr401": "custom.chro_str_top_bedrock",
    "vlit40": "custom.lit_pet_top_bedrock",
    "vlit500": "custom.lit_str_top_bedrock",

    "mcla104": "mcla104",
    "mcla107": "mcla107", # manca geolcode
    "mlpr101": "mlpr101",
    "mlpr104": "mlpr104",
    "mlpr105": "mlpr105",
    "mlpr106": "mlpr106",
    "mlpr108": "mlpr108",
    "mlpr109": "mlpr109",
    "mlpr110": "mlpr110",
    "mlpr112": "mlpr112",
    "mlpr113": "mlpr113",
    "mlpr115": "mlpr115",
    "mlpr116": "mlpr116",
    "mlpr117": "mlpr117",
    "mlpr111": "qt_description", # manca geolcode
    "borehole_form": "borehole_form",
    "layer_form": "layer_form",
    "layer_kind": "layer_kind",

    # "vtec400": "vtec400", # before vtec404
    # "vtec404": "vtec404", # manca
    # "madm401": "madm401", # non usato
    # "madm402": "madm402", # non usato
    # "madm404": "madm404", # non usato
    # "mcla102": "mcla102", # non usato
    # "mcla105": "mcla105", # non usato
    # "mcla106": "mcla106", # non usato
}

conn = psycopg2.connect(
    "dbname=bdms "
    "user=postgres "
    "password=postgres "
    "host=localhost "
    "port=5432"
)
cur = conn.cursor()

geolcodes_location = sys.argv[1]

with open('2-geolcodes.sql', 'w+') as sqlfile:
    with open(geolcodes_location) as csvfile:
        rows = csv.reader(csvfile, delimiter=',', quotechar='"')

        row_number = 1
        cnt = 0
        s = None
        next(rows)
        for row in rows:

            row_number += 1
            geolcode = row[0]

            schema_name = row[1]

            if s != schema_name:
                s = schema_name
                cnt = 0

            cnt += 1

            conf = None

            if schema_name == 'vlit500' and row[11] != '':
                try:
                    conf = f'{{"color": [{row[11]}]}}'
                except Exception as x:
                    raise x
            
            elif schema_name == 'vlit40' and row[11] != '':
                conf = f'{{"image": "{row[11]}"}}'
                
            sqlfile.write(
                cur.mogrify(
                    """INSERT INTO bdms.codelist (
    id_cli, geolcode,
    schema_cli, code_cli,
    text_cli_de, description_cli_de,
    text_cli_fr, description_cli_fr,
    text_cli_it, description_cli_it,
    text_cli_en, description_cli_en,
    order_cli, conf_cli,
    default_cli, path_cli
) VALUES (
    %s, %s,
    %s, %s,
    %s, %s,
    %s, %s,
    %s, %s,
    %s, %s,
    %s, %s,
    false, %s
);
""", 
                    (
                        int(row[0]), int(row[0]),
                        schema[schema_name], row[2],

                        # de
                        row[3] if row[3] != '' else None,
                        row[4] if row[4] != '' else '',

                        # fr
                        row[5] if row[5] != '' else None,
                        row[6] if row[6] != '' else '',

                        # it
                        row[7] if row[7] != '' else None,
                        row[8] if row[8] != '' else '',

                        # en
                        row[9] if row[9] != '' else row[3],
                        row[10] if row[10] != '' else '',

                        cnt, conf,
                        row[12]
                    )
                ).decode('utf-8')
            )

        # 3000
        sqlfile.write(
            cur.mogrify(
                """UPDATE bdms.codelist
    SET conf_cli = %s, default_cli = TRUE
WHERE
    id_cli = 3000;
""", 
                (
                    json.dumps({
                        "color": "lithostratigraphy",
                        "colorNS": "custom.lit_str_top_bedrock",
                        "pattern": "lithology",
                        "patternNS": "custom.lit_pet_top_bedrock",
                        "fields": {
                            "color": False,
                            "notes": True,
                            "debris": False,
                            "striae": False,
                            "uscs_1": False,
                            "uscs_2": False,
                            "uscs_3": False,
                            "geology": False,
                            "cohesion": False,
                            "humidity": False,
                            "jointing": False,
                            "lithology": True,
                            "alteration": False,
                            "plasticity": False,
                            "soil_state": False,
                            "compactness": False,
                            "consistance": False,
                            "description": True,
                            "grain_shape": False,
                            "lit_pet_deb": False,
                            "grain_size_1": False,
                            "grain_size_2": False,
                            "tectonic_unit": False,
                            "uscs_original": False,
                            "qt_description": False,
                            "grain_granularity": False,
                            "lithostratigraphy": True,
                            "organic_component": False,
                            "chronostratigraphy": True,
                            "further_properties": False,
                            "uscs_determination": False
                        }
                    }),
                )
            ).decode('utf-8')
        )


        sqlfile.write(
            cur.mogrify(
                """UPDATE bdms.codelist
    SET conf_cli = %s
WHERE
    id_cli = 3001;
""", 
                (
                    json.dumps({
                        "color": None,
                        "colorNS": None,
                        "pattern": "uscs_1",
                        "patternNS": "mcla101",
                        "fields": {
                            "color": False,
                            "notes": True,
                            "debris": False,
                            "striae": False,
                            "uscs_1": False,
                            "uscs_2": False,
                            "uscs_3": False,
                            "geology": False,
                            "cohesion": False,
                            "humidity": False,
                            "jointing": False,
                            "lithology": True,
                            "alteration": False,
                            "plasticity": False,
                            "soil_state": False,
                            "compactness": False,
                            "consistance": False,
                            "description": True,
                            "grain_shape": False,
                            "lit_pet_deb": False,
                            "grain_size_1": False,
                            "grain_size_2": False,
                            "tectonic_unit": False,
                            "uscs_original": False,
                            "qt_description": False,
                            "grain_granularity": False,
                            "lithostratigraphy": True,
                            "organic_component": False,
                            "chronostratigraphy": True,
                            "further_properties": False,
                            "uscs_determination": False
                        }
                    }),
                )
            ).decode('utf-8')
        )
