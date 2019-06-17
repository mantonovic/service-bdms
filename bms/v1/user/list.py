# -*- coding: utf-8 -*-
from bms.v1.action import Action
import math


class ListUsers(Action):

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
                        id_usr as id,
                        admin_usr as admin,
                        viewer_usr as viewer,
                        username,
                        COALESCE(
                            firstname, ''
                        ) AS firstname,
                        COALESCE(
                            middlename, ''
                        ) AS middlename,
                        COALESCE(
                            lastname, ''
                        ) AS lastname,
                        (
                            SELECT
                                row_to_json(t)
                            FROM (
                                SELECT
                                    groups.id_grp as id,
                                    groups.name_grp as name
                            ) t
                        ) as group,
                        COALESCE(
                            workgroups, '{}'::json[]
                        ) AS workgroups

	                FROM
                        bdms.users

                    LEFT JOIN
                        bdms.groups
                    ON
                        id_grp = id_grp_fk

                    LEFT JOIN (
                        SELECT
                            id_usr_fk,
                            array_agg(
                                json_build_object(
                                    'id', id_wgp_fk,
                                    'roles', roles
                                )
                            ) as workgroups
                        FROM (
                            SELECT
                                id_usr_fk,
                                id_wgp_fk,
                                array_agg(name_rol) as roles
                            FROM
                                bdms.users_roles
                            INNER JOIN
                                bdms.roles
                            ON
                                id_rol = id_rol_fk

                            GROUP BY
                                id_usr_fk, id_wgp_fk
                        )
                        AS wg
                        GROUP BY
                            id_usr_fk
                    ) as w
                    ON
                        w.id_usr_fk = id_usr

                    /*WHERE
                        admin_usr IS FALSE*/

                    ORDER BY
                        username
                ) as t
            """
        )

        return {
            "data": self.decode(val) if val is not None else []
        }
