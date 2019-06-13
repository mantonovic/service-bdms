# -*- coding: utf-8 -*-
from bms.v1.action import Action
import math


class ListWorkflows(Action):

    async def execute(self, id):
        val = await self.conn.fetchval(
            """
            SELECT
                    array_to_json(
                        array_agg(
                            row_to_json(t) 
                        )
                    ) as flow
                FROM (
                    SELECT
                        id_wkf as "id",
                        r.name_rol as "role",
                        to_char(
                            started_wkf,
                            'YYYY-MM-DD"T"HH24:MI:SS'
                        ) as started,
                        to_char(
                            finished_wkf,
                            'YYYY-MM-DD"T"HH24:MI:SS'
                        ) as finished,
                        COALESCE(
                            notes_wkf, ''
                        ) as notes,
                        COALESCE(
                            mentions_wkf, '{}'::character varying[]
                        ) as mentions,
                        (
                            select row_to_json(t)
                            FROM (
                                SELECT
                                    u.id_usr as id,
                                    u.username as username,
                                    firstname || ' ' || lastname as "name"
                            ) t
                        ) as author

                    FROM bdms.workflow

                    INNER JOIN bdms.users as u
                        ON id_usr_fk = u.id_usr

                    INNER JOIN bdms.roles as r
                        ON id_rol_fk = r.id_rol

                    WHERE
                        id_bho_fk = $1

                    ORDER BY
                        id_wkf

                ) as t

            """, id
        )
        return {
            "data": self.decode(val) if val is not None else []
        }
