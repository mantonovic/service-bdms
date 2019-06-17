# -*- coding: utf-8 -*-S
from bms import (
    AuthorizationException
)
from bms.v1.handlers.admin import Admin
from bms.v1.user.workgrpup import (
    ListWorkgroups,
    CreateWorkgroup,
    SetRole
)


class WorkgroupAdminHandler(Admin):
    async def execute(self, request):

        action = request.pop('action', None)

        if action in ['LIST', 'CREATE', 'SET']:

            async with self.pool.acquire() as conn:

                exe = None

                if action in [
                    'LIST', 'CREATE', 'SET'
                ]:
                    if self.user['admin'] is False: 
                        raise AuthorizationException() 

                if action == 'LIST':
                    exe = ListWorkgroups(conn)

                elif action == 'CREATE':
                    exe = CreateWorkgroup(conn)

                elif action == 'SET':
                    exe = SetRole(conn)

                if exe is not None:
                    return (
                        await exe.execute(**request)
                    )

        raise Exception("Action '%s' unknown" % action)
