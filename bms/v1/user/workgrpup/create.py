# -*- coding: utf-8 -*-
from bms.v1.action import Action


class CreateWorkgroup(Action):

    async def execute(self, name):
        return {
            "id": (
                await self.conn.fetchval("""
                    INSERT INTO bdms.workgroups(
                        name_wgp,
                        settings_wgp
                    )
                    VALUES (
                        $1,
                        '{}'
                    )
                    RETURNING id_wgp
                """,
                    name
                )
            )
        }
