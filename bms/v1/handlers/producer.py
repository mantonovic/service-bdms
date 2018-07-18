# -*- coding: utf-8 -*-
from bms.v1.basehandler import BaseHandler
from bms.v1.borehole.list import List
from bms.v1.borehole.get import Get


class Producer(BaseHandler):
    async def execute(self, request):
        # self.user
        action = request.pop('action', '').lower()
        try:
            conn = await self.db.getconn()
            response = None
            with self.db.manage(conn):
                await conn.execute("BEGIN")
                if action == 'list':
                    action = List(self.db)
                elif action == 'get':
                    action = Get(self.db)
                if action is not None:
                    response = await action.execute(**request)
                await conn.execute("COMMIT")
                return response
            raise Exception("Action '%s' unknown")
        except Exception as ex:
            await conn.execute("ROLLBACK")
