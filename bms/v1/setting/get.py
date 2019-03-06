# -*- coding: utf-8 -*-
from bms.v1.action import Action


class GetSetting(Action):

    async def execute(self, user_id):
        print("Fetching user: %s" % user_id)
        rec = await self.conn.fetchrow("""
            SELECT
                settings_usr
            FROM
                users
            WHERE id_usr = $1
        """, user_id)

        return {
            "data": self.decode(rec[0]) if rec[0] is not None else None
        }
