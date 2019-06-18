# -*- coding: utf-8 -*-
from bms.v1.action import Action


class UpdateUser(Action):

    async def execute(
        self, user_id, username, password,
        firstname = '', middlename = '', lastname = '',
        admin = False
    ):
        return {
            "id": (
                await self.conn.fetchval("""
                    UPDATE
                        bdms.users
                    
                    SET
                        admin_usr = $1,
                        username = $2,
                        password = crypt($3, gen_salt('md5')),
                        firstname = $4,
                        middlename = $5,
                        lastname = $6

                    WHERE
                        id_usr = $7
                    """,
                    admin,
                    username,
                    password,
                    firstname if firstname != '' else username,
                    middlename,
                    lastname,
                    user_id
                )
            )
        }
