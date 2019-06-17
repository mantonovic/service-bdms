# -*- coding: utf-8 -*-S
from bms import (
    AuthorizationException
)
from bms.v1.handlers import Viewer
from bms.v1.user import (
    ListUsers
)


class UserHandler(Viewer):
    async def execute(self, request):

        action = request.pop('action', None)

        if action in ['GET']:

            return {
                "data": {
                    "admin": self.user['admin'],
                    "viewer": self.user['viewer'],
                    "username": self.user['username'],
                    "roles": self.user['roles'],
                    "workgroups": self.user['workgroups'],
                    "name": self.user['name']
                }
            }

        raise Exception("Action '%s' unknown" % action)
