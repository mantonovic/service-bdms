# -*- coding: utf-8 -*-
from bms.v1.action import Action
import math


class ListBorehole(Action):

    async def execute(
            self, limit=None, page=None,
            filter={}, orderby=None, direction=None, user=None
        ):

        permissions = None
        if user is not None:
            permissions = self.filterPermission(user)

        paging = ''

        where, params = self.filterBorehole(filter)

        if limit is not None and page is not None:
            paging = """
                LIMIT %s
                OFFSET %s
            """ % (self.getIdx(), self.getIdx())
            params += [
                limit, (int(limit) * (int(page) - 1))
            ]

        rowsSql = """
            SELECT
                id_bho as id,
                (
                    select row_to_json(t)
                    FROM (
                        SELECT
                            author.id_usr as id,
                            author.username as username,
                            to_char(
                                created_bho,
                                'YYYY-MM-DD"T"HH24:MI:SS'
                            ) as date
                    ) t
                ) as author,
                original_name_bho as original_name,
                kind_id_cli as kind,
                restriction_id_cli as restriction,
                to_char(
                    restriction_until_bho,
                    'YYYY-MM-DD'
                ) as restriction_until,
                location_x_bho as location_x,
                location_y_bho as location_y,
                srs_id_cli as srs,
                elevation_z_bho as elevation_z,
                hrs_id_cli as hrs,
                drilling_date_bho as drilling_date,
                length_bho as length,
                (
                    select row_to_json(t)
                    FROM (
                        SELECT
                            status_id_cli as status
                    ) t
                ) as extended,
                /*
                array_to_json(status) as workflow,
                */
                status[array_length(status, 1)] as workflow,
                status[array_length(status, 1)]  ->> 'role' as "role"
            FROM
                bdms.borehole

            INNER JOIN
                bdms.users as author
            ON
                author_id = author.id_usr

            INNER JOIN (
                SELECT
                    id_bho_fk,
                    array_agg(
                        json_build_object(
                            'workflow', id_wkf,
                            'role', name_rol,
                            'username', username,
                            'started', started,
                            'finished', finished
                        )
                    ) as status
                FROM (
                    SELECT
                        id_bho_fk,
                        name_rol,
                        id_wkf,
                        username,
                        started_wkf as started,
                        finished_wkf as finished
                    FROM
                        bdms.workflow,
                        bdms.roles,
                        bdms.users
                    WHERE
                        id_rol = id_rol_fk
                    AND
                        id_usr = id_usr_fk
                    ORDER BY
                        id_wkf
                ) t
                GROUP BY
                    id_bho_fk
            ) as v
            ON
                v.id_bho_fk = id_bho
        """

        cntSql = """
            SELECT count(*) AS cnt
            FROM bdms.borehole
            INNER JOIN (
                SELECT
                    id_bho_fk,
                    array_agg(
                        json_build_object(
                            'workflow', id_wkf,
                            'role', name_rol,
                            'username', username,
                            'started', started,
                            'finished', finished
                        )
                    ) as status
                FROM (
                    SELECT
                        id_bho_fk,
                        name_rol,
                        id_wkf,
                        username,
                        started_wkf as started,
                        finished_wkf as finished
                    FROM
                        bdms.workflow,
                        bdms.roles,
                        bdms.users
                    WHERE
                        id_rol = id_rol_fk
                    AND
                        id_usr = id_usr_fk
                    ORDER BY
                        id_wkf
                ) t
                GROUP BY
                    id_bho_fk
            ) as v
            ON
                v.id_bho_fk = id_bho
        """

        if len(where) > 0:
            rowsSql += """
                WHERE {}
            """.format(
                " AND ".join(where)
            )
            cntSql += """
                WHERE {}
            """.format(
                " AND ".join(where)
            )

        if permissions is not None:
            operator = 'AND' if len(where) > 0 else 'WHERE'
            rowsSql += """
                {} {}
            """.format(
                operator, permissions
            )
            cntSql += """
                {} {}
            """.format(
                operator, permissions
            )

        _orderby, direction = self.getordering(orderby, direction)

        sql = """
            SELECT
                array_to_json(
                    array_agg(
                        row_to_json(t)
                    )
                ),
                COALESCE((
                    %s
                ), 0)
            FROM (
                %s
            ORDER BY %s %s NULLS LAST
                %s
            ) AS t
        """ % (
            cntSql,
            rowsSql,
            _orderby,
            direction,
            paging
        )

        rec = await self.conn.fetchrow(
            sql, *(params)
        )
        return {
            "data": self.decode(rec[0]) if rec[0] is not None else [],
            "orderby": orderby,
            "direction": direction,
            "page": page if page is not None else 1,
            "pages": math.ceil(rec[1]/limit) if limit is not None else 1,
            "rows": rec[1]
        }
