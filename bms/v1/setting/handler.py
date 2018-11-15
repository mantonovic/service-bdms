# -*- coding: utf-8 -*-S
from bms.v1.handlers import Producer
from bms.v1.setting import (
    GetSetting,
    PatchSetting
)


class SettingHandler(Producer):
    async def execute(self, request):
        action = request.pop('action', None)

        if action in [
                'GET',
                'PATCH']:

            async with self.pool.acquire() as conn:

                exe = None
                request['user_id'] = self.user['id']

                if action == 'GET':
                    exe = GetSetting(conn)

                elif action == 'PATCH':
                    exe = PatchSetting(conn)

                request.pop('lang', None)

                if exe is not None:
                    return (
                        await exe.execute(**request)
                    )

        raise Exception("Action '%s' unknown" % action)
