# -*- coding: utf-8 -*-S
from bms.v1.handlers import Viewer
from bms.v1.borehole import (
    ListBorehole,
    GetBorehole,
    ListGeojson
)


class BoreholeViewerHandler(Viewer):
    async def execute(self, request):
        action = request.pop('action', None)

        if action in [
                'LIST',
                'GET',
                'GEOJSON']:

            async with self.pool.acquire() as conn:

                exe = None
                
                if action == 'LIST':
                    exe = ListBorehole(conn)

                elif action == 'GET':
                    exe = GetBorehole(conn)

                elif action == 'GEOJSON':
                    exe = ListGeojson(conn)

                request.pop('lang', None)

                if exe is not None:
                    return (
                        await exe.execute(**request)
                    )

        raise Exception("Action '%s' unknown" % action)
