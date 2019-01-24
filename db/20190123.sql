ALTER TABLE public.stratigraphy
    ADD COLUMN primary_sty boolean;
    
ALTER TABLE public.stratigraphy
    ALTER COLUMN primary_sty SET DEFAULT FALSE;

ALTER TABLE public.stratigraphy
    ADD COLUMN date_sty date;

ALTER TABLE public.stratigraphy
    ADD COLUMN update_sty timestamp without time zone DEFAULT now();

ALTER TABLE public.stratigraphy
    ADD COLUMN updater_sty integer;
    
ALTER TABLE public.stratigraphy DROP CONSTRAINT stratigraphy_id_bho_fk_kind_id_cli_key;

ALTER TABLE public.codelist
    ADD COLUMN default_cli boolean DEFAULT FALSE;
    
UPDATE public.codelist
	SET default_cli=TRUE
	WHERE schema_cli='layer_kind'
	AND code_cli='Or';
	
{
    "fields": [
        "depth_from",
        "depth_to",
        "description",
        "geology",
        "last",
        "qt_description",
        "lithology",
        "lithostratigraphy",
        "chronostratigraphy",
        "tectonic_unit",
        "color",
        "plasticity",
        "humidity",
        "consistance",
        "alteration",
        "compactness",
        "jointing",
        "soil_state",
        "organic_component",
        "striae",
        "grain_size_1",
        "grain_size_2",
        "grain_shape",
        "grain_granularity",
        "cohesion",
        "further_properties",
        "uscs_1",
        "uscs_2",
        "uscs_3",
        "uscs_original",
        "uscs_determination",
        "debris",
        "lit_pet_deb",
        "notes"
    ]
}
