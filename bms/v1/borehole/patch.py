# -*- coding: utf-8 -*-
from bms.v1.action import Action
from bms.v1.exceptions import (
    PatchAttributeException
)


class PatchBorehole(Action):

    async def execute(self, id, field, value, user_id):
        try:
            # Updating character varing field
            if field in [
                        'extended.original_name',
                        'custom.public_name',
                        'custom.project_name',
                        'custom.canton',
                        'custom.city',
                        'custom.address',
                        'location_x',
                        'location_y',
                        'elevation_z',
                        'canton',
                        'address'
                    ]:

                column = None

                if field == 'extended.original_name':
                    column = 'original_name_bho'

                if field == 'custom.public_name':
                    column = 'public_name_bho'

                if field == 'custom.project_name':
                    column = 'project_name_bho'

                if field == 'custom.canton':
                    column = 'canton_bho'

                if field == 'custom.city':
                    column = 'city_bho'

                if field == 'custom.address':
                    column = 'address_bho'

                elif field == 'location_x':
                    column = 'location_x_bho'

                elif field == 'location_y':
                    column = 'location_y_bho'

                elif field == 'elevation_z':
                    column = 'elevation_z_bho'

                elif field == 'canton':
                    column = 'canton_num'

                elif field == 'address':
                    column = 'address_bho'

                await self.conn.execute("""
                    UPDATE public.borehole
                    SET %s = $1
                    WHERE id_bho = $2
                """ % column, value, id)

            # Datetime values
            elif field in [
                        'restriction_date'
                    ]:

                column = None

                if field == 'restriction_date':
                    column = 'restriction_date_bho'

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
                        'custom.landuse'
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

                await self.conn.execute("""
                    UPDATE public.borehole
                    SET %s = $1
                    WHERE id_bho = $2
                """ % column, value, id)

            else:
                raise PatchAttributeException(field)

        except PatchAttributeException as bmsx:
            raise bmsx

        except Exception as ex:
            raise Exception("Error while updating borehole")
