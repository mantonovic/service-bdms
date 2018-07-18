# -*- coding: utf-8 -*-
import json


class Action():
    def __init__(self, conn=None, pool=None):
        self.conn = conn
        self.pool = pool

    def decode(self, text):
        return json.loads(text)

    async def execute(self, *arg, **args):
        pass
