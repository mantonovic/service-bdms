# -*- coding: utf-8 -*-
from bms import EDIT
from bms.v1.action import Action


class CreateBorehole(Action):

    async def execute(self, id, user):

        permit = False
        for w in user['workgroups']:
            if w['id'] == id and 'EDIT' in w['roles']:
                permit = True

        if permit is False:
            raise Exception("Not permitted action")

        bid = await self.conn.fetchval("""
            INSERT INTO bdms.borehole(
                author_id,
                updater_bho,
                id_wgp_fk
            )
            VALUES (
                $1, $2, $3
            ) RETURNING id_bho
        """, user['id'], user['id'], id)

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
