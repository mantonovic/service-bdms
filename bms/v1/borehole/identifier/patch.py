# -*- coding: utf-8 -*-
from bms import EDIT
from bms.v1.action import Action
from bms.v1.exceptions import NotFound


class PatchIdentifier(Action):

    async def execute(self, id, text):

        # Check if identifier exists
        check = await self.conn.fetchval("""
            SELECT
                schema_cli
            FROM
                bdms.codelist
            WHERE
                id_cli = $1
        """, id)

        if check != 'borehole_identifier':
            raise NotFound()

        await self.conn.fetchval("""
            UPDATE bdms.codelist
                SET text_cli_en = $1
            WHERE
                id_cli = $2
        """, text, id)

        return None
