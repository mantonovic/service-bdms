# -*- coding: utf-8 -*-
from bms.v1.action import Action
import math


class ListStratigraphies(Action):

    async def execute(self, limit=None, page=None, filter={}):

        paging = ''
        params = []
        where = []
        fkeys = filter.keys()

        if 'borehole' in fkeys and filter['borehole'] != '':
            params.append(filter['borehole'])
            where.append("""
                id_bho_fk = %s
            """ % self.getIdx())

        if 'kind' in fkeys and filter['kind'] != '':
            params.append(filter['kind'])
            where.append("""
                kind_id_cli = %s
            """ % self.getIdx())

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
                id_sty as id,
                id_bho_fk as borehole,
                kind_id_cli as kind,
                name_sty as name,
                primary_sty as primary,
                to_char(
                    date_sty,
                    'YYYY-MM-DD'
                ) as date
            FROM
                stratigraphy
            INNER JOIN codelist AS lk
            ON lk.id_cli = kind_id_cli
        """

        cntSql = """
            SELECT count(*) AS cnt
            FROM stratigraphy
        """

        if len(where) > 0:
            rowsSql += """
                WHERE %s
            """ % " AND ".join(where)
            cntSql += """
                WHERE %s
            """ % " AND ".join(where)

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
            ORDER BY order_cli, date_sty desc
                %s
            ) AS t
        """ % (cntSql, rowsSql, paging)

        rec = await self.conn.fetchrow(
            sql, *(params)
        )
        return {
            "data": self.decode(rec[0]) if rec[0] is not None else [],
            "page": page if page is not None else 1,
            "pages": math.ceil(rec[1]/limit) if limit is not None else 1,
            "rows": rec[1]
        }
