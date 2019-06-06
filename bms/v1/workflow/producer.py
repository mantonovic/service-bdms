# -*- coding: utf-8 -*-S
from bms import (
    Locked,
    EDIT,
    AuthorizationException
)
from bms.v1.handlers import Producer
from bms.v1.workflow import (
    ListWorkflows,
    PatchWorkflow
)


class WorkflowProducerHandler(Producer):

    async def execute(self, request):
        action = request.pop('action', None)

        if action in ['LIST', 'PATCH', 'FINISH']:

            async with self.pool.acquire() as conn:

                exe = None
                id_bho = None

                if action in [
                    'PATCH', 'FINISH'
                ]:
                    # Get Borehole id
                    id_bho = await conn.fetchval("""
                        SELECT
                            id_bho_fk
                        FROM
                            public.workflow
                        WHERE
                            id_wkf = $1;
                    """, request['id'])

                    # Lock check
                    await self.check_lock(
                        id_bho, self.user, conn
                    )

                if action == 'LIST':
                    exe = ListWorkflows(conn)

                elif action == 'PATCH':
                    exe = PatchWorkflow(conn)
                    request['user'] = self.user

                elif action == 'FINISH':
                    exe = PatchWorkflow(conn)
                    request['user'] = self.user
                    request['bid'] = id_bho

                request.pop('lang', None)

                if exe is not None:
                    return (
                        await exe.execute(**request)
                    )

        raise Exception("Action '%s' unknown" % action)
