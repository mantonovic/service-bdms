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

    def filterBorehole(self, filter={}):
        params = []
        where = []

        if 'identifier' in filter.keys() and filter['identifier'] != '':
            params.append("%%%s%%" % filter['identifier'])
            where.append("""
                original_name_bho ILIKE %s
            """ % self.getIdx())

        if 'project' in filter.keys():
            params.append(filter['project'])
            where.append("""
                project_id = %s
            """ % self.getIdx())

        if 'kind' in filter.keys() and filter['kind'] != None:
            params.append(int(filter['kind']))
            where.append("""
                kind_id_cli = %s
            """ % self.getIdx())

        if 'restriction' in filter.keys() and filter[
                'restriction'] != None:
            params.append(int(filter['restriction']))
            where.append("""
                restriction_id_cli = %s
            """ % self.getIdx())

        if 'status' in filter.keys() and filter[
                'status'] != None:
            params.append(int(filter['status']))
            where.append("""
                status_id_cli = %s
            """ % self.getIdx())

        if 'extent' in filter.keys() and filter['extent'] != None:
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

        return where, params
