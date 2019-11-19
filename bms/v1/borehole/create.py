# -*- coding: utf-8 -*-
from bms import EDIT
from bms.v1.action import Action


class CreateBorehole(Action):

    async def execute(self, id, user):

        # Default SRS (2056)
        srs = 20104001

        # Default HRS (LN02)
        hrs = 20106001

        bid = await self.conn.fetchval("""
            INSERT INTO bdms.borehole(
                author_id,
                updater_bho,
                id_wgp_fk,
                srs_id_cli,
                hrs_id_cli
            )
            VALUES (
                $1, $2, $3, $4, $5
            ) RETURNING id_bho
        """, user['id'], user['id'], id, srs, hrs)

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
