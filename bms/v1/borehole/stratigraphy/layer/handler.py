# -*- coding: utf-8 -*-S
from bms.v1.handlers import Viewer
from bms.v1.borehole.stratigraphy.layer import (
    CreateLayer,
    ListLayers,
    GetLayer,
    PatchLayer,
    DeleteLayer
)


class LayerHandler(Viewer):
    async def execute(self, request):
        action = request.pop('action', None)

        if action in [
                'CREATE',
                'DELETE',
                'PATCH',
                'LIST',
                'GET',
                'CHECK']:

            async with self.pool.acquire() as conn:

                exe = None

                if action == 'CREATE':
                    exe = CreateLayer(conn)

                elif action == 'DELETE':
                    exe = DeleteLayer(conn)

                elif action == 'GET':
                    exe = GetLayer(conn)

                elif action == 'LIST':
                    exe = ListLayers(conn)

                elif action == 'PATCH':
                    exe = PatchLayer(conn)
                    request['user_id'] = self.user['id']

                request.pop('lang', None)

                if exe is not None:
                    return (
                        await exe.execute(**request)
                    )

        raise Exception("Layer action '%s' unknown" % action)
