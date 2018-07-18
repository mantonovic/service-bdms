# -*- coding: utf-8 -*-S
from bms.v1.handlers import Viewer
from bms.v1.borehole.codelist.listcodelist import ListCodeList


class CodeListHandler(Viewer):
    async def execute(self, request):
        action = request.pop('action', None)

        if action in [
                'CREATE',
                'LIST',
                'GET',
                'CHECK']:

            async with self.pool.acquire() as conn:
                if action == 'LIST':
                    action = ListCodeList(conn=conn)

                request.pop('lang', None)  # removing lang
                if action is not None:
                    return (
                        await action.execute(**request)
                    )

        raise Exception("Action '%s' unknown", action)
