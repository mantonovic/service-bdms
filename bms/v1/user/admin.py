# -*- coding: utf-8 -*-S
from bms import (
    AuthorizationException
)
from bms.v1.handlers.admin import Admin
from bms.v1.user import (
    ListUsers,
    CreateUser,
    UpdateUser
)


class AdminHandler(Admin):
    async def execute(self, request):

        action = request.pop('action', None)

        if action in ['LIST', 'CREATE', 'UPDATE']:

            async with self.pool.acquire() as conn:

                exe = None

                if action in [
                    'LIST', 'CREATE', 'UPDATE'
                ]:
                    if self.user['admin'] is False: 
                        raise AuthorizationException() 

                if action == 'LIST':
                    exe = ListUsers(conn)

                elif action == 'CREATE':
                    exe = CreateUser(conn)

                elif action == 'UPDATE':
                    exe = UpdateUser(conn)

                if exe is not None:
                    return (
                        await exe.execute(**request)
                    )

        raise Exception("Action '%s' unknown" % action)
