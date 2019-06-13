# -*- coding: utf-8 -*-S
from bms import (
    Locked,
    EDIT,
    AuthorizationException
)
from bms.v1.handlers import Producer
from bms.v1.borehole import (
    CheckBorehole,
    StartEditing,
    Lock,
    Unlock,
    CreateBorehole,
    DeleteBorehole,
    DeleteBoreholes,
    ListEditingBorehole,
    MultiPatchBorehole,
    PatchBorehole,
    BoreholeIds
)
from bms.v1.setting import (
    PatchSetting
)


class BoreholeProducerHandler(Producer):

    async def execute(self, request):
        action = request.pop('action', None)

        if action in [
                'CREATE',
                'LOCK',
                'UNLOCK',
                'EDIT',
                'DELETE',
                'DELETELIST',
                'PATCH',
                'MULTIPATCH',
                'CHECK',
                'LIST',
                'IDS']:

            async with self.pool.acquire() as conn:

                exe = None

                if action in [
                    'LOCK',
                    'UNLOCK',
                    'EDIT',
                    'DELETE',
                    'PATCH',
                ]:
                    # Lock check
                    res = await self.check_lock(
                        request['id'], self.user, conn
                    )

                    if action in [
                        'PATCH'
                    ] and res['role'] != 'EDIT': 
                        raise AuthorizationException() 

                if action == 'CREATE':
                    exe = CreateBorehole(conn)
                    request['user'] = self.user

                elif action == 'LOCK':
                    exe = Lock(conn)
                    request['user'] = self.user

                elif action == 'UNLOCK':
                    exe = Unlock(conn)

                elif action == 'EDIT':
                    exe = StartEditing(conn)
                    request['user'] = self.user

                elif action == 'DELETE':
                    exe = DeleteBorehole(conn)

                elif action == 'DELETELIST':
                    exe = DeleteBoreholes(conn)

                elif action == 'PATCH':
                    exe = PatchBorehole(conn)
                    request['user'] = self.user

                elif action == 'MULTIPATCH':
                    exe = MultiPatchBorehole(conn)
                    request['user'] = self.user

                elif action == 'CHECK':
                    exe = CheckBorehole(conn)

                elif action == 'IDS':
                    exe = BoreholeIds(conn)
                    request['user'] = self.user
                
                elif action == 'LIST':
                    exe = ListEditingBorehole(conn)
                    request['user'] = self.user

                    # update only if ordering changed
                    if 'orderby' in request and (
                        request['orderby'] is not None
                    ) and (
                        self.user[
                            'setting'
                        ]['eboreholetable']['orderby'] != request['orderby']
                    ):
                        await (PatchSetting(conn)).execute(
                            self.user['id'],
                            'eboreholetable.orderby',
                            request['orderby']
                        )
                    else:
                        request['orderby'] = self.user[
                            'setting'
                        ]['eboreholetable']['orderby']

                    if 'direction' in request and (
                        request['direction'] is not None
                    ) and (
                        self.user[
                            'setting'
                        ]['eboreholetable']['direction'] != request['direction']
                    ):
                        await (PatchSetting(conn)).execute(
                            self.user['id'],
                            'eboreholetable.direction',
                            request['direction']
                        )
                    else:
                        request['direction'] = self.user[
                            'setting'
                        ]['eboreholetable']['direction']

                request.pop('lang', None)

                if exe is not None:
                    return (
                        await exe.execute(**request)
                    )

        raise Exception("Action '%s' unknown" % action)
