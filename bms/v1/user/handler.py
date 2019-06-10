# -*- coding: utf-8 -*-S
from bms.v1.handlers import Viewer


class UserHandler(Viewer):
    async def execute(self, request):

        action = request.pop('action', None)

        if action in ['GET']:

            if action == 'GET':
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
