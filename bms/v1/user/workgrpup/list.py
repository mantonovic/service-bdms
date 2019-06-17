# -*- coding: utf-8 -*-
from bms.v1.action import Action
import math


class ListWorkgroups(Action):

    async def execute(self):

        val = await self.conn.fetchval(
            """
                SELECT
                    array_to_json(
                        array_agg(
                            row_to_json(t)
                        )
                    )
                FROM (
                    SELECT
                        id_wgp as id,
                        name_wgp as name
                        
                    FROM bdms.workgroups

                    ORDER BY
                        name_wgp
                ) as t
            """
        )

        return {
            "data": self.decode(val) if val is not None else []
        }
