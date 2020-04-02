# -*- coding: utf-8 -*-
from bms import EDIT
from bms.v1.action import Action
from bms.v1.exceptions import NotFound


class DeleteIdentifier(Action):

    async def execute(self, id):

        # Check if identifier already exists
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

        await self.conn.execute("""
            DELETE FROM bdms.codelist
            WHERE id_cli = $1
        """, id)

        return None
