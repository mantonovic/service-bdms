# -*- coding: utf-8 -*-
from bms.v1.action import Action


class CreateStratigraphy(Action):

    async def execute(self, id, kind):
        # Check if domain is extracted from the correct schema
        schema = await self.conn.fetchval("""
            SELECT
                schema_cli
            FROM
                codelist
            WHERE id_cli = $1
        """, kind)

        if schema != 'layer_kind':
            raise Exception(
                "Attribute id %s not part of schema layer_kind" % kind
            )

        return {
            "id": (
                await self.conn.fetchval("""
                    INSERT INTO public.stratigraphy(id_bho_fk, kind_id_cli)
                    VALUES ($1, $2) RETURNING id_sty
                """, id, kind)
            )
        }
