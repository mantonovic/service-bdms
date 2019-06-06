# -*- coding: utf-8 -*-
from bms.v1.action import Action
from bms.v1.exceptions import (
    PatchAttributeException
)
from bms import Locked

from bms.v1.workflow import ListWorkflows


class FinishWorkflow(Action):

    async def execute(self, id, user, bid = None):
        try:

            if bid is None:
                bid = await self.conn.fetchval("""
                    SELECT
                        id_bho_fk
                    FROM
                        public.workflow
                    WHERE
                        id_wkf = $1;
                """, id)

            # Get current workflows
            workflows = (
                ListWorkflows(self.conn)
            ).execute(bid)

            # Check that requested workflow is the last and open
            if len(workflows['data']) == 0:
                raise Exception("Workflow list empty")

            if workflows['data'][-1]['id'] != id:
                raise Exception("Finishing wrong workflow")

            await self.conn.execute("""
                UPDATE public.workflow
                SET
                    finished_wkf = now(),
                    id_usr_fk = $1
                WHERE id_wkf = $2;
            """, user['id'], id)

            await self.conn.execute("""
                UPDATE public.borehole
                SET
                    update_bho = now(),
                    updater_bho = $1
                WHERE id_bho = $2
            """, user['id'], bid)

            return {
                "data": {
                    "id": id
                }
            }

        except Exception:
            raise Exception("Error while updating borehole")
