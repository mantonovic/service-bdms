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

            workgroups = []
            roles = []

            for workgroup in self.user['workgroups']:
                print(workgroup)
                if workgroup['disabled'] is not None:
                    workgroup['roles'] = ['VIEWER']
                
                workgroups.append(workgroup)
            
                for role in workgroup['roles']:
                    if role not in roles:
                        roles.append(role)

            return {
                "data": {
                    "admin": self.user['admin'],
                    "viewer": self.user['viewer'],
                    "username": self.user['username'],
                    "roles": roles,  # self.user['roles'],
                    "workgroups": workgroups, #  self.user['workgroups'],
                    "name": self.user['name']
                }
            }

        raise Exception("Action '%s' unknown" % action)
