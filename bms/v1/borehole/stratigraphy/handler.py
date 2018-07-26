# -*- coding: utf-8 -*-S
from bms.v1.handlers import Viewer
from bms.v1.borehole.stratigraphy import (
    ListStratigraphies,
    CreateStratigraphy,
    GetStratigraphy
)


class StratigraphyHandler(Viewer):
    async def execute(self, request):
        action = request.pop('action', None)

        if action in [
                'CREATE',
                'PATCH',
                'LIST',
                'GET',
                'CHECK']:

            async with self.pool.acquire() as conn:

                exe = None

                if action == 'GET':
                    exe = GetStratigraphy(conn)

                if action == 'CREATE':
                    exe = CreateStratigraphy(conn)

                elif action == 'LIST':
                    exe = ListStratigraphies(conn)

                request.pop('lang', None)

                if exe is not None:
                    return (
                        await exe.execute(**request)
                    )

        raise Exception("Action '%s' unknown" % action)
