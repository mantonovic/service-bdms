# -*- coding: utf-8 -*-
from bms.v1.action import Action


class GetUser(Action):
    async def execute(self):
        return {
            "data": self._user
        }
