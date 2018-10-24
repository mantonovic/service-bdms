# -*- coding: utf-8 -*-S
from bms.v1.handlers import Producer
from bms.v1.borehole import (
    CreateBorehole,
    DeleteBorehole,
    PatchBorehole,
    CheckBorehole,
    ListEditingBorehole
)


class BoreholeProducerHandler(Producer):
    async def execute(self, request):
        action = request.pop('action', None)

        if action in [
                'CREATE',
                'DELETE',
                'PATCH',
                'CHECK',
                'LIST']:

            async with self.pool.acquire() as conn:

                exe = None

                if action == 'CREATE':
                    exe = CreateBorehole(conn)
                    request['user_id'] = self.user['id']

                if action == 'DELETE':
                    exe = DeleteBorehole(conn)

                elif action == 'PATCH':
                    exe = PatchBorehole(conn)
                    request['user_id'] = self.user['id']

                elif action == 'CHECK':
                    exe = CheckBorehole(conn)
                
                if action == 'LIST':
                    exe = ListEditingBorehole(conn)

                request.pop('lang', None)

                if exe is not None:
                    return (
                        await exe.execute(**request)
                    )

        raise Exception("Action '%s' unknown" % action)
