# -*- coding: utf-8 -*-
from bms.v1.action import Action
from bms.v1.exceptions import (
    PatchAttributeException
)


class PatchLayer(Action):

    async def execute(self, id, field, value, user_id):
        try:
            # Updating character varing, boolean fields
            if field in [
                        'depth_from',
                        'depth_to',
                        'description',
                        'geology',
                        'last',
                        'striae',
                        'uscs_original',
                        'notes'
                    ]:

                column = None

                if field == 'depth_from':
                    column = 'depth_from_lay'

                elif field == 'depth_to':
                    column = 'depth_to_lay'

                elif field == 'description':
                    column = 'description_lay'

                elif field == 'geology':
                    column = 'geology_lay'

                elif field == 'last':
                    column = 'last_lay'

                elif field == 'striae':
                    column = 'striae_lay'

                elif field == 'uscs_original':
                    column = 'uscs_original_lay'

                elif field == 'notes':
                    column = 'notes_lay'

                await self.conn.execute("""
                    UPDATE bdms.layer
                    SET
                        %s = $1,
                        update_lay = now(),
                        updater_lay = $2
                    WHERE id_lay = $3
                """ % column, value, user_id, id)

            # Datetime values
            elif field in [
                        'restriction_until',
                        'drilling_date'
                    ]:

                column = None

                if field == 'restriction_until':
                    column = 'restriction_until_lay'

                elif field == 'drilling_date':
                    column = 'drilling_date_lay'

                await self.conn.execute("""
                    UPDATE bdms.layer
                    SET
                        %s = to_date($1, 'YYYY-MM-DD'),
                        update_lay = now(),
                        updater_lay = $2
                    WHERE id_lay = $3
                """ % column, value, user_id, id)

            elif field in [
                        'qt_description',
                        'lithology',
                        'lithostratigraphy',
                        'chronostratigraphy',
                        'tectonic_unit',
                        'plasticity',
                        'humidity',
                        'consistance',
                        'alteration',
                        'compactness',
                        'soil_state',
                        'grain_size_1',
                        'grain_size_2',
                        'cohesion',
                        'uscs_1',
                        'uscs_2',
                        'unconrocks',
                        'lithok',
                        'kirost'
                    ]:

                column = None
                schema = field

                if field == 'qt_description':
                    column = 'qt_description_id_cli'

                elif field == 'lithology':
                    column = 'lithology_id_cli'
                    schema = 'custom.lit_pet_top_bedrock'

                elif field == 'lithostratigraphy':
                    column = 'lithostratigraphy_id_cli'
                    schema = 'custom.lit_str_top_bedrock'

                elif field == 'chronostratigraphy':
                    column = 'chronostratigraphy_id_cli'
                    schema = 'custom.chro_str_top_bedrock'

                elif field == 'tectonic_unit':
                    column = 'tectonic_unit_id_cli'
                    schema = 'vtec404'

                elif field == 'plasticity':
                    column = 'plasticity_id_cli'
                    schema = 'mlpr101'

                elif field == 'humidity':
                    column = 'humidity_id_cli'
                    schema = 'mlpr105'

                elif field == 'consistance':
                    column = 'consistance_id_cli'
                    schema = 'mlpr103'

                elif field == 'alteration':
                    column = 'alteration_id_cli'
                    schema = 'mlpr106'

                elif field == 'compactness':
                    column = 'compactness_id_cli'
                    schema = 'mlpr102'

                elif field == 'soil_state':
                    column = 'soil_state_id_cli'
                    schema = 'mlpr108'

                elif field == 'grain_size_1':
                    column = 'grain_size_1_id_cli'
                    schema = 'mlpr109'

                elif field == 'grain_size_2':
                    column = 'grain_size_2_id_cli'
                    schema = 'mlpr109'

                elif field == 'cohesion':
                    column = 'cohesion_id_cli'
                    schema = 'mlpr116'

                elif field == 'uscs_1':
                    column = 'uscs_1_id_cli'
                    schema = 'mcla101'

                elif field == 'uscs_2':
                    column = 'uscs_2_id_cli'
                    schema = 'mcla101'

                elif field == 'unconrocks':
                    column = 'unconrocks_id_cli'
                    schema = 'mcla102'

                elif field == 'lithok':
                    column = 'lithok_id_cli'
                    schema = 'mcla105'

                elif field == 'kirost':
                    column = 'kirost_id_cli'
                    schema = 'mcla106'

                # Check if domain is extracted from the correct schema
                if schema != (await self.conn.fetchval("""
                            SELECT
                                schema_cli
                            FROM
                                bdms.codelist
                            WHERE id_cli = $1
                        """, value)):
                    raise Exception(
                        "Attribute id %s not part of schema %s" %
                        (
                            value, schema
                        )
                    )

                await self.conn.execute("""
                    UPDATE bdms.layer
                    SET
                        %s = $1,
                        update_lay = now(),
                        updater_lay = $2
                    WHERE id_lay = $3
                """ % column, value, user_id, id)

            elif field in [
                        'color',
                        'jointing',
                        'organic_component',
                        'grain_shape',
                        'grain_granularity',
                        'further_properties',
                        'uscs_3',
                        'uscs_determination',
                        'debris',
                        'lit_pet_deb'
                    ]:

                schema = field

                if field == 'color':
                    schema = 'mlpr112'

                elif field == 'jointing':
                    schema = 'mlpr113'

                elif field == 'organic_component':
                    schema = 'mlpr108'

                elif field == 'grain_shape':
                    schema = 'mlpr110'

                elif field == 'grain_granularity':
                    schema = 'mlpr115'

                elif field == 'further_properties':
                    schema = 'mlpr117'

                elif field == 'uscs_3':
                    schema = 'mcla101'

                elif field == 'uscs_determination':
                    schema = 'mcla104'

                elif field == 'debris':
                    schema = 'mcla107'

                elif field == 'lit_pet_deb':
                    schema = 'custom.lit_pet_top_bedrock'

                await self.conn.execute("""
                    DELETE FROM bdms.layer_codelist
                    WHERE id_lay_fk = $1
                    AND code_cli = $2
                """, id, schema)

                if len(value) > 0:
                    # Check if domain(s) is(are) extracted from the correct schema
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
                            "not part of schema attribute: %s" %
                            (
                                value, field
                            )
                        )

                    await self.conn.executemany("""
                        INSERT INTO
                            bdms.layer_codelist (
                                id_lay_fk, id_cli_fk, code_cli
                            ) VALUES ($1, $2, $3)
                    """, [(id, v, schema) for v in value])

                    await self.conn.execute("""
                        UPDATE bdms.layer
                        SET
                            update_lay = now(),
                            updater_lay = $1
                        WHERE id_lay = $2
                    """, user_id, id)

            else:
                raise PatchAttributeException(field)

        except PatchAttributeException as bmsx:
            raise bmsx

        except Exception as ex:
            raise Exception("A server error occured while updating the layer")
