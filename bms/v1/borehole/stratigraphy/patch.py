# -*- coding: utf-8 -*-
from bms.v1.action import Action
from bms.v1.exceptions import (
    PatchAttributeException
)


class PatchStartigraphy(Action):

    async def execute(self, id, field, value, user_id):
        try:
            # Updating character varing, boolean fields
            if field in ['date']:

                column = None

                if field == 'date':
                    column = 'date_sty'

                if value == '':
                    value = None

                await self.conn.execute("""
                    UPDATE public.stratigraphy
                    SET
                        %s = to_date($1, 'YYYY-MM-DD'),
                        update_sty = now(),
                        updater_sty = $2
                    WHERE id_sty = $3
                """ % column, value, user_id, id)

            elif field in ['kind']:

                column = None
                schema = field

                if field == 'kind':
                    column = 'kind_id_cli'
                    schema = 'layer_kind'

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
                    UPDATE public.stratigraphy
                    SET
                        %s = $1,
                        update_sty = now(),
                        updater_sty = $2
                    WHERE id_sty = $3
                """ % column, value, user_id, id)

            else:
                raise PatchAttributeException(field)

            return None

        except PatchAttributeException as bmsx:
            raise bmsx

        except Exception:
            raise Exception("Error while updating stratigraphy")
