# -*- coding: utf-8 -*-S
from bms.v1.handlers import Viewer
from bms.v1.borehole import (
    CreateBorehole,
    PatchBorehole,
    ListBorehole,
    GetBorehole,
    CheckBorehole,
    ListGeojson
)


class BoreholeHandler(Viewer):
    async def execute(self, request):
        action = request.pop('action', None)

        if action in [
                'CREATE',
                'PATCH',
                'LIST',
                'GET',
                'CHECK',
                'GEOJSON']:

            async with self.pool.acquire() as conn:

                exe = None

                if action == 'CREATE':
                    exe = CreateBorehole(conn)
                    request['user_id'] = self.user['id']

                elif action == 'PATCH':
                    exe = PatchBorehole(conn)
                    request['user_id'] = self.user['id']

                elif action == 'LIST':
                    exe = ListBorehole(conn)

                elif action == 'GET':
                    exe = GetBorehole(conn)

                elif action == 'CHECK':
                    exe = CheckBorehole(conn)

                elif action == 'GEOJSON':
                    exe = ListGeojson(conn)

                request.pop('lang', None)

                if exe is not None:
                    return (
                        await exe.execute(**request)
                    )

        raise Exception("Action '%s' unknown" % action)
