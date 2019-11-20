# -*- coding: utf-8 -*-
from bms.v1.action import Action


class CreateStratigraphy(Action):

    async def execute(self, id, user_id):
        # find default stratigraphy type
        id_cli = await self.conn.fetchval("""
            SELECT
                id_cli
            FROM
                bdms.codelist
            WHERE
                schema_cli = 'layer_kind'
            AND
                default_cli IS TRUE
        """)

        cnt = await self.conn.fetchval("""
            SELECT
                count(id_sty)
            FROM
                bdms.stratigraphy
            WHERE
                id_bho_fk = $1
        """, id)

        return {
            "id": (
                await self.conn.fetchval("""
                    INSERT INTO bdms.stratigraphy(
                        id_bho_fk, kind_id_cli, primary_sty, author_sty
                    )
                    VALUES ($1, $2, $3, $4) RETURNING id_sty
                """, id, id_cli, True if cnt == 0 else False, user_id)
            )
        }
