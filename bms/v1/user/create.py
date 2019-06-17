# -*- coding: utf-8 -*-
from bms.v1.action import Action


class CreateUser(Action):

    async def execute(
        self, username, password,
        firstname = '', middlename = '', lastname = ''
    ):
        return {
            "id": (
                await self.conn.fetchval("""
                    INSERT INTO bdms.users(
                        admin_usr,
                        viewer_usr,
                        username,
                        password,
                        firstname,
                        middlename,
                        lastname
                    )
                    VALUES (
                        False,
                        True,
                        $1,
                        $2,
                        $3,
                        $4,
                        $5
                    )
                    RETURNING id_usr
                    """,
                    username,
                    password,
                    firstname if firstname != '' else username,
                    middlename,
                    lastname
                )
            )
        }
