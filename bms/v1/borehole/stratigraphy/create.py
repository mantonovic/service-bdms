# -*- coding: utf-8 -*-
from bms.v1.action import Action


class CreateStratigraphy(Action):

    async def execute(self, id):
        # Check if domain is extracted from the correct schema
        id_cli = await self.conn.fetchval("""
            SELECT
                id_cli
            FROM
                codelist
            WHERE
                schema_cli = 'layer_kind'
            AND
                default_cli IS TRUE
        """)

        return {
            "id": (
                await self.conn.fetchval("""
                    INSERT INTO public.stratigraphy(id_bho_fk, kind_id_cli)
                    VALUES ($1, $2) RETURNING id_sty
                """, id, id_cli)
            )
        }
