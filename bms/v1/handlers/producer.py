# -*- coding: utf-8 -*-
from bms import (
    BaseHandler,
    AuthorizationException
)


class Producer(BaseHandler):
    def authorize(self):
        if 'producer' not in self.user['roles']:
            raise AuthorizationException()
