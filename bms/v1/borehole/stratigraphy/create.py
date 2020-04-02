# -*- coding: utf-8 -*-
from bms.v1.action import Action


class CreateStratigraphy(Action):

    async def execute(self, id, user_id, kind=None):
        try:
            await self.conn.execute("BEGIN;")

            # Check if this is the first inserted stratigraphy
            # if assertion is true, then set as primary
            cnt = await self.conn.fetchval("""
                SELECT
                    count(id_sty)
                FROM
                    bdms.stratigraphy
                WHERE
                    id_bho_fk = $1
            """, id)

            primary_sty = True if cnt == 0 else False

            # Insert the new stratigraphy
            id_sty = await self.conn.fetchval("""
                INSERT INTO bdms.stratigraphy(
                    id_bho_fk, primary_sty, author_sty
                )
                VALUES ($1, $2, $3) RETURNING id_sty
            """, id, primary_sty, user_id)

            if kind is None:
                # find default stratigraphy type
                kind = [
                    await self.conn.fetchval("""
                        SELECT
                            id_cli
                        FROM
                            bdms.codelist
                        WHERE
                            schema_cli = 'layer_kind'
                        AND
                            default_cli IS TRUE
                    """)
                ]

            for id_cli in kind:
                await self.conn.fetchval("""
                    INSERT INTO bdms.stratigraphy_codelist(
                        id_sty_fk, id_cli_fk, code_cli
                    )
                    VALUES (
                        $1, $2, 'layer_kind'
                    );
                """, id_sty, id_cli)

            await self.conn.execute("COMMIT;")

            return {
                "id": id_sty
            }

        except Exception as ex:
            await self.conn.execute("ROLLBACK;")
            raise ex

