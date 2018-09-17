# -*- coding: utf-8 -*-
from bms import (
    BaseHandler,
    AuthorizationException
)


class Viewer(BaseHandler):
    def authorize(self):
        if 'viewer' not in self.user['roles']:
            raise AuthorizationException()
