# -*- coding: utf-8 -*-S
from bms import Locked
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
from datetime import datetime
from datetime import timedelta


class BoreholeProducerHandler(Producer):

    async def check_lock(self, id, user_id, conn):
        rec = await conn.fetchrow("""
            SELECT
                locked_at,
                locked_by,
                firstname || ' ' || lastname
            FROM
                borehole
            LEFT JOIN users
            ON users.id_usr = borehole.locked_by
            WHERE
                id_bho = $1
        """, id)

        if rec is None:
            raise Exception(f"Borehole with id: '{id}' not exists")

        if rec is not None:

            now = datetime.now()

            td = timedelta(minutes=Lock.lock_timeout)

            locked_at = rec[0]
            locked_by = rec[1]
            locked_by_name = rec[2]

            if (
                locked_at is not None and  # Locked by someone
                locked_by != user_id and   # Someone is not the current user
                (now - locked_at) < (td)   # Timeout not finished
            ):
                raise Locked(
                    id, 
                    {
                        "user": locked_by_name,
                        "datetime": locked_at.isoformat()
                    }
                )

        # Lock row for current user
        await conn.execute("""
            UPDATE borehole SET
                locked_at = $1,
                locked_by = $2
            WHERE id_bho = $3;
        """, now, user_id, id)

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
                    await self.check_lock(
                        request['id'], self.user['id'], conn
                    )

                if action == 'CREATE':
                    exe = CreateBorehole(conn)
                    request['user_id'] = self.user['id']

                if action == 'LOCK':
                    exe = Lock(conn)
                    request['user_id'] = self.user['id']

                if action == 'UNLOCK':
                    exe = Unlock(conn)
                    request['user_id'] = self.user['id']

                if action == 'EDIT':
                    exe = StartEditing(conn)
                    request['user_id'] = self.user['id']

                elif action == 'DELETE':
                    exe = DeleteBorehole(conn)

                elif action == 'DELETELIST':
                    exe = DeleteBoreholes(conn)

                elif action == 'PATCH':
                    exe = PatchBorehole(conn)
                    request['user_id'] = self.user['id']

                elif action == 'MULTIPATCH':
                    exe = MultiPatchBorehole(conn)
                    request['user_id'] = self.user['id']

                elif action == 'CHECK':
                    exe = CheckBorehole(conn)

                elif action == 'IDS':
                    exe = BoreholeIds(conn)
                
                elif action == 'LIST':
                    exe = ListEditingBorehole(conn)

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
