# -*- coding: utf-8 -*-
from bms.v1.action import Action
from bms.v1.exceptions import (
    PatchAttributeException
)
from bms.v1.borehole.geom.patch import PatchGeom
from bms import Locked
from datetime import datetime
from datetime import timedelta


class PatchBorehole(Action):

    async def execute(self, id, field, value, user_id):
        try:
            
            # Updating character varing, boolean fields
            if field in [
                'extended.original_name',
                'custom.public_name',
                'custom.project_name',
                'address',
                'geocoding',
                'custom.canton',
                'custom.city',
                'custom.address',
                'location',
                'location_x',
                'location_y',
                'elevation_z',
                'canton',
                'address',
                'drill_diameter',
                'custom.drill_diameter',
                'bore_inc',
                'bore_inc_dir',
                'length',
                'extended.top_bedrock',
                'extended.groundwater',
                'custom.mistakes',
                'custom.remarks'
                    ]:

                column = None

                if field == 'extended.original_name':
                    column = 'original_name_bho'

                if field == 'custom.public_name':
                    column = 'public_name_bho'

                if field == 'custom.project_name':
                    column = 'project_name_bho'

                if field == 'custom.address':
                    column = 'address_bho'

                if field == 'custom.address':
                    column = 'address_bho'

                elif field in ['location_x', 'location_y', 'location']:

                    if field == 'location_x':
                        column = 'location_x_bho'

                    elif field == 'location_y':
                        column = 'location_y_bho'

                    elif field == 'location':
                        if value[3] is None:
                            column = [
                                'location_x_bho',
                                'location_y_bho',
                                'canton_bho',
                                'city_bho'
                            ]
                            value = value[:-1]
                        else:
                            column = [
                                'location_x_bho',
                                'location_y_bho',
                                'canton_bho',
                                'city_bho',
                                'elevation_z_bho'
                            ]

                elif field == 'elevation_z':
                    column = 'elevation_z_bho'

                if field == 'geocoding':
                    column = [
                        'canton_bho',
                        'city_bho'
                    ]

                if field == 'custom.canton':
                    column = 'canton_bho'

                if field == 'custom.city':
                    column = 'city_bho'

                elif field == 'canton':
                    column = 'canton_num'

                elif field == 'address':
                    column = 'address_bho'

                elif field == 'custom.drill_diameter':
                    column = 'drill_diameter_bho'

                elif field == 'bore_inc':
                    column = 'bore_inc_bho'

                elif field == 'bore_inc_dir':
                    column = 'bore_inc_dir_bho'

                elif field == 'length':
                    column = 'length_bho'

                elif field == 'extended.top_bedrock':
                    column = 'top_bedrock_bho'

                elif field == 'extended.groundwater':
                    column = 'groundwater_bho'

                elif field == 'custom.mistakes':
                    column = 'mistakes_bho'

                elif field == 'custom.remarks':
                    column = 'remarks_bho'

                if isinstance(column, list):
                    sets = []
                    for col in column:
                        sets.append("%s = %s" % (col, self.getIdx()))
                    value.append(user_id)
                    value.append(id)
                    print(value)
                    await self.conn.execute("""
                        UPDATE public.borehole
                        SET
                            %s,
                            update_bho = now(),
                            updater_bho = %s
                        WHERE id_bho = %s
                    """ % (
                        ", ".join(sets),
                        self.getIdx(),
                        self.getIdx()
                    ), *value)

                else:
                    await self.conn.execute("""
                        UPDATE public.borehole
                        SET
                            %s = $1,
                            update_bho = now(),
                            updater_bho = $2
                        WHERE id_bho = $3
                    """ % column, value, user_id, id)
                
                if field in ['location_x', 'location_y', 'location']:

                    geom = PatchGeom(self.conn)
                    await geom.execute(id, field, value)

            # Datetime values
            elif field in [
                        'restriction_until',
                        'drilling_date'
                    ]:

                column = None

                if field == 'restriction_until':
                    column = 'restriction_until_bho'

                elif field == 'drilling_date':
                    column = 'drilling_date_bho'

                if value == '':
                    value = None

                await self.conn.execute("""
                    UPDATE public.borehole
                    SET
                        %s = to_date($1, 'YYYY-MM-DD'),
                        update_bho = now(),
                        updater_bho = $2
                    WHERE id_bho = $3
                """ % column, value, user_id, id)

            elif field in [
                'restriction',
                'kind',
                'srs',
                'qt_location',
                'qt_elevation',
                'hrs',
                'custom.landuse',
                'extended.method',
                'custom.cuttings',
                'extended.purpose',
                'extended.status',
                'custom.qt_bore_inc_dir',
                'custom.qt_length',
                'custom.qt_top_bedrock',
                'custom.processing_status',
                'custom.national_relevance',
                'custom.lit_pet_top_bedrock',
                'custom.lit_str_top_bedrock',
                'custom.chro_str_top_bedrock'
                    ]:

                column = None
                schema = field

                if field == 'restriction':
                    column = 'restriction_id_cli'

                elif field == 'kind':
                    column = 'kind_id_cli'

                elif field == 'srs':
                    column = 'srs_id_cli'

                elif field == 'qt_location':
                    column = 'qt_location_id_cli'

                elif field == 'qt_elevation':
                    column = 'qt_elevation_id_cli'

                elif field == 'hrs':
                    column = 'hrs_id_cli'

                elif field == 'custom.landuse':
                    column = 'landuse_id_cli'

                elif field == 'extended.method':
                    column = 'method_id_cli'

                elif field == 'custom.cuttings':
                    column = 'cuttings_id_cli'

                elif field == 'extended.purpose':
                    column = 'purpose_id_cli'

                elif field == 'extended.status':
                    column = 'status_id_cli'

                elif field == 'custom.qt_bore_inc_dir':
                    column = 'qt_bore_inc_dir_id_cli'

                elif field == 'custom.qt_length':
                    column = 'qt_length_id_cli'

                elif field == 'custom.qt_top_bedrock':
                    column = 'qt_top_bedrock_id_cli'

                elif field == 'custom.processing_status':
                    column = 'processing_status_id_cli'
                    schema = 'madm401'

                elif field == 'custom.national_relevance':
                    column = 'national_relevance_id_cli'
                    schema = 'madm402'

                elif field == 'custom.lit_pet_top_bedrock':
                    column = 'lithology_id_cli'
                    schema = 'custom.lit_pet_top_bedrock'

                elif field == 'custom.lit_str_top_bedrock':
                    column = 'lithostrat_id_cli'
                    schema = 'custom.lit_str_top_bedrock'

                elif field == 'custom.chro_str_top_bedrock':
                    column = 'chronostrat_id_cli'
                    schema = 'custom.chro_str_top_bedrock'

                # Check if domain is extracted from the correct schema
                if value is not None and schema != (await self.conn.fetchval("""
                            SELECT
                                schema_cli
                            FROM
                                codelist
                            WHERE
                                id_cli = $1
                        """, value)):
                    raise Exception(
                        "Attribute id %s not part of schema %s" %
                        (
                            value, schema
                        )
                    )

                await self.conn.execute("""
                    UPDATE public.borehole
                    SET
                        %s = $1,
                        update_bho = now(),
                        updater_bho = $2
                    WHERE id_bho = $3
                """ % column, value, user_id, id)

            elif field in [
                        'custom.attributes_to_edit'
                    ]:

                schema = field

                if field == 'custom.attributes_to_edit':
                    schema = 'madm404'

                await self.conn.execute("""
                    DELETE FROM public.borehole_codelist
                    WHERE id_bho_fk = $1
                    AND code_cli = $2
                """, id, schema)

                if len(value) > 0:
                    # Check if domain is extracted from the correct schema
                    check = await self.conn.fetchval("""
                        SELECT COALESCE(count(schema_cli), 0) = $1
                        FROM (
                            SELECT
                                schema_cli
                            FROM
                                codelist
                            WHERE
                                id_cli = ANY($2)
                            AND
                                schema_cli = $3
                        ) AS c
                    """, len(value), value, schema)
                    if check is False:
                        raise Exception(
                            "One ore more attribute ids %s are "
                            "not part of schema %s" %
                            (
                                value, schema
                            )
                        )

                    await self.conn.executemany("""
                        INSERT INTO
                            public.borehole_codelist (
                                id_bho_fk, id_cli_fk, code_cli
                            ) VALUES ($1, $2, $3)
                    """, [(id, v, schema) for v in value])

                    await self.conn.execute("""
                        UPDATE public.borehole
                        SET
                            update_bho = now(),
                            updater_bho = $1
                        WHERE id_bho = $2
                    """, user_id, id)

            else:
                raise PatchAttributeException(field)

            rec = await self.conn.fetchval("""
                SELECT
                    row_to_json(t2)
                FROM (
                    SELECT
                        percentage,
                        (
                            SELECT row_to_json(t)
                            FROM (
                                SELECT
                                    borehole.locked_by as id,
                                    locker.username as username,
                                    locker.firstname || ' ' || locker.lastname
                                        as fullname,
                                    to_char(
                                        borehole.locked_at,
                                        'YYYY-MM-DD"T"HH24:MI:SS'
                                    ) as date
                            ) AS t
                        ) as lock,
                        (
                            select row_to_json(t)
                            FROM (
                                SELECT
                                    updater.id_usr as id,
                                    updater.username as username,
                                    updater.firstname || ' ' || updater.lastname
                                        as fullname,
                                    to_char(
                                        update_bho,
                                        'YYYY-MM-DD"T"HH24:MI:SS'
                                    ) as date
                            ) t
                        ) as updater
                    FROM
                        borehole
                    INNER JOIN public.users as locker
                        ON locked_by = locker.id_usr
                    INNER JOIN public.completness
                        ON completness.id_bho = borehole.id_bho
                    INNER JOIN public.users as updater
                        ON updater_bho = updater.id_usr
                    WHERE borehole.id_bho = $1
                ) t2
            """, id)

            return self.decode(rec) if rec is not None else None

        except PatchAttributeException as bmsx:
            raise bmsx

        except Locked as lkd:
            raise lkd

        except Exception:
            raise Exception("Error while updating borehole")
