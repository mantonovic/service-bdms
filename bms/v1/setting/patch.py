# -*- coding: utf-8 -*-
from bms.v1.action import Action
from bms.v1.exceptions import (
    PatchAttributeException
)
from bms.v1.borehole.geom.patch import PatchGeom
import json


class PatchSetting(Action):

    async def execute(self, user_id, field, value):
        try:
            # Updating character varing, boolean fields
            path = field.split('.')
            l = len(path)

            rec = await self.conn.fetchrow("""
                SELECT
                    settings_usr
                FROM
                    users
                WHERE id_usr = $1
            """, user_id)

            setting = self.decode(rec[0]) if rec[0] is not None else None
            tmp = setting

            if tmp is not None:
                for idx in range(0, l):
                    if idx < (l-1) and path[idx] not in tmp:
                        tmp[path[idx]] = {}
                    elif idx == (l-1):
                        tmp[path[idx]] = value
                    tmp = tmp[path[idx]]

            else:
                setting = {}
                tmp = setting
                for idx in range(0, l):
                    if idx < (l-1):
                        tmp[path[idx]] = {}
                    else:
                        tmp[path[idx]] = value
                    tmp = tmp[path[idx]]

            await self.conn.execute("""
                UPDATE public.users
                SET
                    settings_usr = $1
                WHERE id_usr = $2
            """, json.dumps(setting), user_id)

            return {
                "data": setting
            }

        except PatchAttributeException as bmsx:
            raise bmsx

        except Exception:
            raise Exception("Error while updating borehole")
