# -*- coding: utf-8 -*-
from bms.v1.action import Action
from bms.v1.exceptions import (
    PatchAttributeException
)


class PatchLayer(Action):

    async def execute(self, id, field, value, user_id):
        try:
            # Updating character varing field
            if field in [
                        'depth_from',
                        'depth_to'
                    ]:

                column = None

                if field == 'depth_from':
                    column = 'depth_from_lay'

                elif field == 'depth_to':
                    column = 'depth_to_lay'

                await self.conn.execute("""
                    UPDATE public.layer
                    SET %s = $1
                    WHERE id_lay = $2
                """ % column, value, id)

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

                await self.conn.execute("""
                    UPDATE public.borehole
                    SET %s = to_date($1, 'YYYY-MM-DD')
                    WHERE id_bho = $2
                """ % column, value, id)

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
                        'custom.qt_top_bedrock'
                    ]:

                column = None

                # Check if domain is extracted from the correct schema
                schema = await self.conn.fetchval("""
                    SELECT
                        schema_cli
                    FROM
                        codelist
                    WHERE id_cli = $1
                """, value)

                if schema != field:
                    raise Exception(
                        "Attribute id %s not part of schema %s" %
                        (
                            value, field
                        )
                    )

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

                await self.conn.execute("""
                    UPDATE public.borehole
                    SET %s = $1
                    WHERE id_bho = $2
                """ % column, value, id)

            elif field in [
                        'custom.lit_pet_top_bedrock',
                        'custom.lit_str_top_bedrock',
                        'custom.chro_str_top_bedrock'
                    ]:

                await self.conn.execute("""
                    DELETE FROM public.borehole_codelist
                    WHERE id_bho_fk = $1
                    AND code_cli = $2
                """, id, field)

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
                    """, len(value), value, field)
                    if check is False:
                        raise Exception(
                            "One ore more attribute ids %s are "
                            "not part of schema %s" %
                            (
                                value, field
                            )
                        )

                    await self.conn.executemany("""
                        INSERT INTO
                            public.borehole_codelist (
                                id_bho_fk, id_cli_fk, code_cli
                            ) VALUES ($1, $2, $3)
                    """, [(id, v, field) for v in value])

            else:
                raise PatchAttributeException(field)

        except PatchAttributeException as bmsx:
            raise bmsx

        except Exception as ex:
            raise Exception("Error while updating borehole")
