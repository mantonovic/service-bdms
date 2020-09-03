# -*- coding: utf-8 -*-
from bms.v1.action import Action
from bms import Locked
from datetime import datetime
from datetime import timedelta


class DeleteStratigraphy(Action):

    async def execute(self, id, user_id):

        # First check if the user has a lock on row
        # rec = await self.conn.fetchrow("""
        #     SELECT
        #         locked_at,
        #         locked_by
        #     FROM
        #         bdms.borehole
        #     LEFT JOIN
        #         bdms.users
        #     ON
        #         users.id_usr = borehole.locked_by
        #     WHERE
        #         id_bho = $1
        # """, id)

        # if rec is not None:
            
        #     now = datetime.now()
        #     td = timedelta(minutes=self.lock_timeout)

        #     locked_at = rec[0]
        #     locked_by = rec[1]

        #     # Check if not locked or not locked by current user
        #     if (
        #         locked_by is None or
        #         (
        #             locked_by != user_id
        #             or (now - locked_at) > (td)
        #         )
        #     ):
        #         raise Locked(
        #             id, None
        #         )

        # Check if deleting the primary startigraphy
        rec = await self.conn.fetchrow("""
            SELECT
                primary_sty,
                COALESCE(cnt, 0),
                s.id_bho_fk
            FROM
                bdms.stratigraphy as s
            LEFT JOIN (
                SELECT
                    id_bho_fk,
                    COUNT(*) cnt
                FROM
                    bdms.stratigraphy
                WHERE
                    primary_sty IS FALSE
                GROUP BY id_bho_fk
            ) a
                ON s.id_bho_fk = a.id_bho_fk
            WHERE
                id_sty = $1
        """, id)

        await self.conn.execute("""
                DELETE FROM
                    bdms.stratigraphy
                WHERE
                    id_sty = $1
            """, id)

        if rec[0] and rec[1] > 0:  # The stratigraphy layer is primary
            # Setting the last created stratigraphy as primary
            id_sty = await self.conn.fetchval("""
                SELECT
                    id_sty
                FROM
                    bdms.stratigraphy
                WHERE
                    id_bho_fk = $1
                ORDER BY
                    creation_sty DESC
                LIMIT 1;
            """, rec[2])

            await self.conn.execute("""
                UPDATE bdms.stratigraphy
                SET
                    primary_sty = True
                WHERE
                    id_sty = $1
            """, id_sty)

        return None
