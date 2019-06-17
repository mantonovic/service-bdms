# -*- coding: utf-8 -*-S
from bms import (
    AuthorizationException
)
from bms.v1.handlers.admin import Admin
from bms.v1.user import (
    ListUsers,
    CreateUser
)


class AdminHandler(Admin):
    async def execute(self, request):

        action = request.pop('action', None)

        if action in ['LIST', 'CREATE']:

            async with self.pool.acquire() as conn:

                exe = None

                if action in [
                    'LIST', 'CREATE'
                ]:
                    if self.user['admin'] is False: 
                        raise AuthorizationException() 

                if action == 'LIST':
                    exe = ListUsers(conn)

                elif action == 'CREATE':
                    exe = CreateUser(conn)

                if exe is not None:
                    return (
                        await exe.execute(**request)
                    )

        raise Exception("Action '%s' unknown" % action)
