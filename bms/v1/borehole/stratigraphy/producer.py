# -*- coding: utf-8 -*-S
from bms.v1.handlers import Producer
from bms.v1.borehole.stratigraphy import (
    CreateStratigraphy,
    PatchStartigraphy,
    DeleteStratigraphy,
    CloneStratigraphy
)


class StratigraphyProducerHandler(Producer):
    async def execute(self, request):
        action = request.pop('action', None)

        if action in [
            'CREATE',
            'PATCH',
            'DELETE',
            'CHECK',
            'CLONE'
        ]:

            async with self.pool.acquire() as conn:

                exe = None

                id_bho = None

                if action in [
                    'CREATE'
                ]:
                    # Lock check
                    await self.check_lock(
                        request['id'], self.user, conn
                    )

                elif action in [
                    'PATCH', 'DELETE', 'CHECK', 'CLONE'
                ]:
                    # Get Borehole id
                    id_bho = await conn.fetchval("""
                        SELECT
                            id_bho_fk
                        FROM
                            bdms.stratigraphy
                        WHERE
                            id_sty = $1;
                    """, request['id'])

                    # Lock check
                    await self.check_lock(
                        id_bho, self.user, conn
                    )

                if action == 'CREATE':
                    exe = CreateStratigraphy(conn)

                elif action == 'DELETE':
                    exe = DeleteStratigraphy(conn)
                    request['user_id'] = self.user['id']

                elif action == 'PATCH':
                    exe = PatchStartigraphy(conn)
                    request['user_id'] = self.user['id']

                elif action == 'CLONE':
                    exe = CloneStratigraphy(conn)
                    request['user_id'] = self.user['id']

                request.pop('lang', None)

                if exe is not None:
                    return (
                        await exe.execute(**request)
                    )

        raise Exception("Action '%s' unknown" % action)
