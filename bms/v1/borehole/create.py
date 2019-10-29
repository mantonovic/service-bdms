# -*- coding: utf-8 -*-
from bms import EDIT
from bms.v1.action import Action


class CreateBorehole(Action):

    async def execute(self, id, user):

        srs = await self.conn.fetchval("""
            SELECT id_cli
            FROM
                bdms.codelist
            WHERE
                schema_cli = 'srs'
            AND
                code_cli = '2056'
        """)

        bid = await self.conn.fetchval("""
            INSERT INTO bdms.borehole(
                author_id,
                updater_bho,
                id_wgp_fk,
                srs_id_cli
            )
            VALUES (
                $1, $2, $3, $4
            ) RETURNING id_bho
        """, user['id'], user['id'], id, srs)

        await self.conn.fetchval("""
            INSERT INTO bdms.workflow(
                id_bho_fk,
                id_usr_fk,
                id_rol_fk
            ) VALUES (
                $1, $2, $3
            ) RETURNING id_wkf
        """, bid, user['id'], EDIT)

        return {
            "id": bid
        }
