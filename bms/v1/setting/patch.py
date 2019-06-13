# -*- coding: utf-8 -*-
from bms.v1.action import Action
from bms.v1.exceptions import (
    PatchAttributeException
)
from bms.v1.borehole.geom.patch import PatchGeom
import json


class PatchSetting(Action):

    async def execute(self, user_id, tree, value, key=None):
        try:
            # Updating character varing, boolean fields
            pathList = tree.split('.')
            l = len(pathList)

            if key is not None:
                l += 1
                pathList.append(key)

            rec = await self.conn.fetchrow("""
                SELECT
                    settings_usr
                FROM
                    bdms.users
                WHERE id_usr = $1
            """, user_id)

            setting = self.decode(rec[0]) if rec[0] is not None else None
            tmp = setting

            if tmp is not None:
                for idx in range(0, l):
                    if idx < (l-1) and pathList[idx] not in tmp:
                        tmp[pathList[idx]] = {}
                    elif idx == (l-1):
                        if value is None:
                            del tmp[pathList[idx]]
                            break
                        else:
                            tmp[pathList[idx]] = value
                    tmp = tmp[pathList[idx]]

            else:
                setting = {
                    "filter": {},
                    "boreholetable": {
                        "orderby": "original_name",
                        "direction": "ASC"
                    },
                    "eboreholetable": {
                        "orderby": "creation",
                        "direction": "DESC"
                    },
                    "map": {
                        "explorer": {},
                        "editor": {}
                    },
                    "appearance": {
                        "explorer": 1
                    }
                }
                tmp = setting
                for idx in range(0, l):
                    if idx < (l-1):
                        tmp[pathList[idx]] = {}
                    else:
                        if value is None:
                            del tmp[pathList[idx]]
                            break
                        else:
                            tmp[pathList[idx]] = value
                    tmp = tmp[pathList[idx]]

            await self.conn.execute("""
                UPDATE bdms.users
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
