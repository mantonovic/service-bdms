# -*- coding: utf-8 -*-
import json


class Action():
    def __init__(self, conn=None, pool=None):
        self.conn = conn
        self.pool = pool
        self.idx = 0

    def decode(self, text):
        return json.loads(text)

    async def execute(self, *arg, **args):
        pass

    def getIdx(self):
        self.idx += 1
        return "$%s" % self.idx

    def getordering(self, orderby, direction):
        _orderby = 'original_name_bho'
        if orderby == 'original_name':
            _orderby = 'original_name_bho'

        elif orderby == 'restriction':
            _orderby = 'restriction_id_cli'

        elif orderby == 'elevation_z':
            _orderby = 'elevation_z_bho'

        elif orderby == 'length':
            _orderby = 'length_bho'

        elif orderby == 'kind':
            _orderby = 'kind_id_cli'

        elif orderby == 'restriction_until':
            _orderby = 'restriction_until_bho'

        elif orderby == 'drilling_date':
            _orderby = 'drilling_date_bho'

        elif orderby == 'status':
            _orderby = 'status_id_cli'

        elif orderby == 'completness':
            _orderby = 'percentage'

        else:
            orderby = 'original_name'

        if direction not in ['DESC', 'ASC']:
            direction = 'ASC'

        return _orderby, direction

    def filterBorehole(self, filter={}):
        params = []
        where = []

        keys = filter.keys()

        if 'completness' in keys and filter['completness'] != '':
            if filter['completness'] == 'complete':
                params.append(100)
                where.append("""
                    percentage = %s
                """ % self.getIdx())
            elif filter['completness'] == 'incomplete':
                params.append(0)
                where.append("""
                    percentage > %s
                """ % self.getIdx())
                params.append(100)
                where.append("""
                    percentage < %s
                """ % self.getIdx())
            if filter['completness'] == 'empty':
                params.append(0)
                where.append("""
                    percentage = %s
                """ % self.getIdx())

        if 'identifier' in keys and filter['identifier'] != '':
            if filter['identifier'] == '$null':
                where.append("""
                    original_name_bho IS NULL
                """)
            else:
                params.append("%%%s%%" % filter['identifier'])
                where.append("""
                    original_name_bho ILIKE %s
                """ % self.getIdx())

        if 'original_name' in keys and filter['original_name'] != '':
            if filter['original_name'] == '$null':
                where.append("""
                    original_name_bho IS NULL
                """)
            else:
                params.append("%%%s%%" % filter['original_name'])
                where.append("""
                    original_name_bho ILIKE %s
                """ % self.getIdx())

        if 'project' in keys and filter['project'] is not None:
            params.append(filter['project'])
            where.append("""
                project_id = %s
            """ % self.getIdx())

        if 'kind' in keys and filter['kind'] is not None:
            params.append(int(filter['kind']))
            where.append("""
                kind_id_cli = %s
            """ % self.getIdx())

        if 'restriction' in keys and filter[
                'restriction'] is not None:
            params.append(int(filter['restriction']))
            where.append("""
                restriction_id_cli = %s
            """ % self.getIdx())

        if 'status' in keys and filter[
                'status'] is not None:
            params.append(int(filter['status']))
            where.append("""
                status_id_cli = %s
            """ % self.getIdx())

        if 'extent' in keys and filter['extent'] is not None:
            for coord in filter['extent']:
                params.append(coord)
            where.append("""
                ST_Intersects(
                    geom_bho,
                    ST_MakeEnvelope(
                        %s, %s, %s, %s, 2056
                    )
                )
            """ % (
                self.getIdx(),
                self.getIdx(),
                self.getIdx(),
                self.getIdx()
            ))

        if 'canton' in keys and filter['canton'] is not None:
            params.append(int(filter['canton']))
            where.append("""
                canton_bho = %s
            """ % self.getIdx())

        if 'municipality' in keys and filter['municipality'] is not None:
            params.append(int(filter['municipality']))
            where.append("""
                city_bho = %s
            """ % self.getIdx())

        if 'restriction_until_from' in keys and filter['restriction_until_from'] != '':
            params.append(filter['restriction_until_from'])
            where.append("""
                restriction_until_bho >= to_date(%s, 'YYYY-MM-DD')
            """ % self.getIdx())

        if 'restriction_until_to' in keys and filter['restriction_until_to'] != '':
            params.append(filter['restriction_until_to'])
            where.append("""
                restriction_until_bho <= to_date(%s, 'YYYY-MM-DD')
            """ % self.getIdx())

        if 'drilling_date_from' in keys and filter['drilling_date_from'] != '':
            params.append(filter['drilling_date_from'])
            where.append("""
                drilling_date_bho >= to_date(%s, 'YYYY-MM-DD')
            """ % self.getIdx())

        if 'drilling_date_to' in keys and filter['drilling_date_to'] != '':
            params.append(filter['drilling_date_to'])
            where.append("""
                drilling_date_bho <= to_date(%s, 'YYYY-MM-DD')
            """ % self.getIdx())

        if 'elevation_z_from' in keys and filter['elevation_z_from'] != '':
            params.append(float(filter['elevation_z_from']))
            where.append("""
                elevation_z_bho >= %s
            """ % self.getIdx())

        if 'elevation_z_to' in keys and filter['elevation_z_to'] != '':
            params.append(float(filter['elevation_z_to']))
            where.append("""
                elevation_z_bho <= %s
            """ % self.getIdx())

        if 'length_from' in keys and filter['length_from'] != '':
            params.append(float(filter['length_from']))
            where.append("""
                length_bho >= %s
            """ % self.getIdx())

        if 'length_to' in keys and filter['length_to'] != '':
            params.append(float(filter['length_to']))
            where.append("""
                length_bho <= %s
            """ % self.getIdx())

        return where, params
