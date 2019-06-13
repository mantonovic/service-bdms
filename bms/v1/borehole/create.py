# -*- coding: utf-8 -*-
from bms import EDIT
from bms.v1.action import Action
from bms.v1.workflow import CreateWorkflow


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

        await (
            CreateWorkflow(self.conn)
        ).execute(bid, user, EDIT)

        return {
            "id": bid
        }
