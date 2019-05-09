ALTER TABLE public.layer
    ADD COLUMN undefined_lay boolean DEFAULT FALSE;

INSERT INTO public.codelist(
    schema_cli,
    code_cli,
    text_cli_en, description_cli_en,
    text_cli_de, description_cli_de,
    text_cli_fr, description_cli_fr,
    text_cli_it, description_cli_it,
    text_cli_ro, description_cli_ro,

    order_cli, conf_cli, default_cli
)
VALUES (
    'custom.lit_pet_top_bedrock',
    'unknown',
    'Unknown', '',
    '', '',
    '', '',
    '', '',
    '', '',
    0, '{"img": "unknown.jpg"}', FALSE
);

COMMENT ON SCHEMA public
  IS 'v1.190509';
