# -*- coding: utf-8 -*-
from bms.v1.action import Action
from bms.v1.borehole.stratigraphy.layer import ListLayers, CreateLayer


class CloneStratigraphy(Action):

    async def execute(self, id, user_id):

        id_sty = (
            await self.conn.fetchval("""
                INSERT INTO public.stratigraphy(
                    id_bho_fk,
                    kind_id_cli,
                    date_sty
                )
                SELECT
                    id_bho_fk,
                    kind_id_cli,
                    now()
                FROM
                    stratigraphy
                WHERE id_sty = $1
            RETURNING id_sty
            """, id)
        )

        # Copy layers
        await self.conn.execute(f"""
            INSERT INTO public.layer(
                id_sty_fk,
                depth_from_lay,
                depth_to_lay,
                description_lay,
                geology_lay,
                last_lay,
                qt_description_id_cli,
                lithology_id_cli,
                chronostratigraphy_id_cli,
                tectonic_unit_id_cli,
                symbol_id_cli,
                plasticity_id_cli,
                consistance_id_cli,
                alteration_id_cli,
                compactness_id_cli,
                soil_state_id_cli,
                grain_size_1_id_cli,
                grain_size_2_id_cli,
                cohesion_id_cli,
                uscs_1_id_cli,
                uscs_2_id_cli,
                uscs_original_lay,
                uscs_determination_id_cli,
                kirost_id_cli,
                notes_lay,
                lithostratigraphy_id_cli,
                humidity_id_cli,
                striae_lay,
                unconrocks_id_cli,
                lithok_id_cli,
                creation_lay,
                creator_lay,
                update_lay,
                updater_lay
            )
            SELECT
                {id_sty} as id_sty_fk,
                depth_from_lay,
                depth_to_lay,
                description_lay,
                geology_lay,
                last_lay,
                qt_description_id_cli,
                lithology_id_cli,
                chronostratigraphy_id_cli,
                tectonic_unit_id_cli,
                symbol_id_cli,
                plasticity_id_cli,
                consistance_id_cli,
                alteration_id_cli,
                compactness_id_cli,
                soil_state_id_cli,
                grain_size_1_id_cli,
                grain_size_2_id_cli,
                cohesion_id_cli,
                uscs_1_id_cli,
                uscs_2_id_cli,
                uscs_original_lay,
                uscs_determination_id_cli,
                kirost_id_cli,
                notes_lay,
                lithostratigraphy_id_cli,
                humidity_id_cli,
                striae_lay,
                unconrocks_id_cli,
                lithok_id_cli,
                now(),
                {user_id} as creator_lay,
                now(),
                {user_id} as updater_lay
            FROM
                public.layer
            WHERE
                id_sty_fk = $1
        """, id)

        return {
            "id": id_sty
        }
