# -*- coding: utf-8 -*-
from bms import EDIT
from bms.v1.action import Action
from bms.v1.exceptions import DuplicateException


class CreateIdentifier(Action):

    async def execute(self, text):

        # Check if identifier already exists
        check = await self.conn.fetchval("""
            SELECT
                text_cli_en
            FROM
                bdms.codelist
            WHERE
                text_cli_en = $1
            AND
                schema_cli = 'borehole_identifier'
        """, text)

        if check:
            raise DuplicateException()

        bid = await self.conn.fetchval("""
            INSERT INTO bdms.codelist(
                code_cli,
                text_cli_en,
                description_cli_en,
                schema_cli
            )
            VALUES (
                '', $1, ' ', 'borehole_identifier'
            ) RETURNING id_cli
        """, text)

        await self.conn.fetchval("""
            UPDATE bdms.codelist
                SET
                    code_cli = id_cli,
                    geolcode = id_cli
            WHERE
                id_cli = $1
        """, bid)

        return {
            "id": bid
        }
