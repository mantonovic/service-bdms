# -*- coding: utf-8 -*-
import json
from bms import (
    PUBLIC,
    EDIT
)


class Action():

    lock_timeout = 10

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

        elif orderby == 'author':
            _orderby = 'author_id'

        elif orderby == 'creation':
            _orderby = 'created_bho'

        else:
            orderby = 'original_name'

        if direction not in ['DESC', 'ASC']:
            direction = 'ASC'

        return _orderby, direction

    def filterPermission(self, user, exclude = []):
        
        where = []

        roles = user['roles'].copy()
        if len(exclude) > 0:
            for role in exclude:
                if role in roles:
                    roles.pop(
                        roles.index(role)
                    )

        # If user is a viewer then he/she can see all published boreholes
        if 'VIEW' not in exclude and user['viewer'] == True:
            where.append(f"""
                borehole.public_bho IS TRUE
            """)

        # If the user belongs to a workgroups then he can see all
        # the belonging boreholes with his role active
        for workgroup in user['workgroups']:

            # role_filter = ""
            # if len(workgroup['roles']) == 1:
            #     role_filter = f" = '{workgroup['roles'][0]}'"
            # else:
            #     role_filter = f"""
            #         IN ('{ "', '".join(workgroup['roles'])}')
            #     """

            # where.append(f"""
            #     id_wgp_fk = {workgroup['id']}
            #     AND (
            #         status[
            #             array_length(status, 1)
            #         ]  ->> 'role'
            #     ) {role_filter}
            # """)

            # User can see not finished data belonging to his workgroups 
            where.append(f"""
                id_wgp_fk = {workgroup['id']}
            """)

        return '({})'.format(
            ' OR '.join(where)
        )

    def filterBorehole(self, filter={}):
        params = []
        where = []

        keys = filter.keys()

        if 'id' in keys and filter['id'] != '':
            _or = []
            for bid in filter['id'].split(','):
                params.append(int(bid))
                _or.append("""
                    borehole.id_bho = %s
                """ % self.getIdx())
            where.append("(%s)" % " OR ".join(_or))
            # print(where)

        else:

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

            if (
                'role' in keys and
                filter['role'] != '' and
                filter['role'] != 'all'
            ):
                params.append(filter['role'])
                where.append("""
                    status[
                        array_length(status, 1)
                    ]  ->> 'role' = %s
                """ % self.getIdx())

            if (
                'workgroup' in keys and
                filter['workgroup'] != ''
                and filter['workgroup'] != 'all'
            ):
                params.append(filter['workgroup'])
                where.append("""
                    id_wgp_fk = %s
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

            if 'public_name' in keys and filter['public_name'] != '':
                if filter['public_name'] == '$null':
                    where.append("""
                        public_name_bho IS NULL
                    """)
                else:
                    params.append("%%%s%%" % filter['public_name'])
                    where.append("""
                        public_name_bho ILIKE %s
                    """ % self.getIdx())

            if 'project' in keys and filter['project'] is not None:
                params.append(filter['project'])
                where.append("""
                    project_id = %s
                """ % self.getIdx())

            if 'project_name' in keys and filter['project_name'] != '':
                if filter['project_name'] == '$null':
                    where.append("""
                        project_name_bho IS NULL
                    """)
                else:
                    params.append("%%%s%%" % filter['project_name'])
                    where.append("""
                        project_name_bho ILIKE %s
                    """ % self.getIdx())

            if 'address' in keys and filter['address'] != '':
                if filter['address'] == '$null':
                    where.append("""
                        address_bho IS NULL
                    """)
                else:
                    params.append("%%%s%%" % filter['address'])
                    where.append("""
                        address_bho ILIKE %s
                    """ % self.getIdx())

            if 'kind' in keys and filter['kind'] is not None:
                params.append(int(filter['kind']))
                where.append("""
                    kind_id_cli = %s
                """ % self.getIdx())

            if 'cuttings' in keys and filter['cuttings'] is not None:
                params.append(int(filter['cuttings']))
                where.append("""
                    cuttings_id_cli = %s
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

            if 'method' in keys and filter[
                    'method'] is not None:
                params.append(int(filter['method']))
                where.append("""
                    method_id_cli = %s
                """ % self.getIdx())

            if 'purpose' in keys and filter['purpose'] is not None:
                params.append(int(filter['purpose']))
                where.append("""
                    purpose_id_cli = %s
                """ % self.getIdx())

            if 'landuse' in keys and filter['landuse'] is not None:
                params.append(int(filter['landuse']))
                where.append("""
                    landuse_id_cli = %s
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

            if 'groundwater' in keys and filter['groundwater'] != -1:
                if filter['groundwater'] == None:
                    where.append("""
                        groundwater_bho IS NULL
                    """)
                else:
                    params.append(filter['groundwater'])
                    where.append("""
                        groundwater_bho = %s
                    """ % self.getIdx())

            if 'creation' in keys and filter['creation'] != '':
                params.append(filter['creation'])
                where.append("""
                    created_bho::date = to_date(%s, 'YYYY-MM-DD')
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

            if 'drill_diameter_from' in keys and filter['drill_diameter_from'] != '':
                params.append(float(filter['drill_diameter_from']))
                where.append("""
                    drill_diameter_bho >= %s
                """ % self.getIdx())

            if 'drill_diameter_to' in keys and filter['drill_diameter_to'] != '':
                params.append(float(filter['drill_diameter_to']))
                where.append("""
                    drill_diameter_bho <= %s
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

            if 'bore_inc_from' in keys and filter['bore_inc_from'] != '':
                params.append(float(filter['bore_inc_from']))
                where.append("""
                    bore_inc_bho >= %s
                """ % self.getIdx())

            if 'bore_inc_to' in keys and filter['bore_inc_to'] != '':
                params.append(float(filter['bore_inc_to']))
                where.append("""
                    bore_inc_bho <= %s
                """ % self.getIdx())

            if 'bore_inc_dir_from' in keys and filter['bore_inc_dir_from'] != '':
                params.append(float(filter['bore_inc_dir_from']))
                where.append("""
                    bore_inc_dir_bho >= %s
                """ % self.getIdx())

            if 'bore_inc_dir_to' in keys and filter['bore_inc_dir_to'] != '':
                params.append(float(filter['bore_inc_dir_to']))
                where.append("""
                    bore_inc_dir_bho <= %s
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

            if 'top_bedrock_from' in keys and filter['top_bedrock_from'] != '':
                params.append(float(filter['top_bedrock_from']))
                where.append("""
                    top_bedrock_bho >= %s
                """ % self.getIdx())

            if 'top_bedrock_to' in keys and filter['top_bedrock_to'] != '':
                params.append(float(filter['top_bedrock_to']))
                where.append("""
                    top_bedrock_bho <= %s
                """ % self.getIdx())

            if 'lit_pet_top_bedrock' in keys and filter[
                    'lit_pet_top_bedrock'] is not None:
                params.append(int(filter['lit_pet_top_bedrock']))
                where.append("""
                    lithology_id_cli = %s
                """ % self.getIdx())

            if 'lit_str_top_bedrock' in keys and filter[
                    'lit_str_top_bedrock'] is not None:
                params.append(int(filter['lit_str_top_bedrock']))
                where.append("""
                    lithostrat_id_cli = %s
                """ % self.getIdx())

            if 'chro_str_top_bedrock' in keys and filter[
                    'chro_str_top_bedrock'] is not None:
                params.append(int(filter['chro_str_top_bedrock']))
                where.append("""
                    lithostrat_id_cli = %s
                """ % self.getIdx())

        return where, params
