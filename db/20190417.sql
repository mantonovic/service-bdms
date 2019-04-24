ALTER TABLE public.borehole
    ADD COLUMN locked_at timestamp without time zone;

ALTER TABLE public.borehole
    ADD COLUMN locked_by integer;
    
ALTER TABLE public.borehole
    ADD FOREIGN KEY (locked_by)
    REFERENCES public.users (id_usr) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE SET NULL;

ALTER TABLE public.borehole
    ADD COLUMN version_id_cli integer;

ALTER TABLE public.borehole
    ADD FOREIGN KEY (version_id_cli)
    REFERENCES public.codelist (id_cli) MATCH SIMPLE
    ON UPDATE CASCADE
    ON DELETE NO ACTION;

INSERT INTO public.codelist(
	schema_cli, code_cli,
	text_cli_en, description_cli_en,
	text_cli_de, description_cli_de,
	text_cli_fr, description_cli_fr,
	text_cli_it, description_cli_it,
	text_cli_ro, description_cli_ro,
	order_cli
)
VALUES (
	'version', 'E',
	'Editing', '', -- English
	'Bearbeitung', '', -- German
	'Édition', '', -- French
	'Modifica', '', -- Italian
	'Editing', '', -- Romancio
	1
);

INSERT INTO public.codelist(
	schema_cli, code_cli,
	text_cli_en, description_cli_en,
	text_cli_de, description_cli_de,
	text_cli_fr, description_cli_fr,
	text_cli_it, description_cli_it,
	text_cli_ro, description_cli_ro,
	order_cli
)
VALUES (
	'version', 'R',
	'Review', '', -- English
	'Überprüfen', '', -- German
	'Revue', '', -- French
	'Revisione', '', -- Italian
	'Review', '', -- Romancio
	2
);

INSERT INTO public.codelist(
	schema_cli, code_cli,
	text_cli_en, description_cli_en,
	text_cli_de, description_cli_de,
	text_cli_fr, description_cli_fr,
	text_cli_it, description_cli_it,
	text_cli_ro, description_cli_ro,
	order_cli
)
VALUES (
	'version', 'R',
	'Validation', '', -- English
	'Validierung', '', -- German
	'Validation', '', -- French
	'Validazione', '', -- Italian
	'Validation', '', -- Romancio
	3
);

INSERT INTO public.codelist(
	schema_cli, code_cli,
	text_cli_en, description_cli_en,
	text_cli_de, description_cli_de,
	text_cli_fr, description_cli_fr,
	text_cli_it, description_cli_it,
	text_cli_ro, description_cli_ro,
	order_cli
)
VALUES (
	'version', 'R',
	'Published', '', -- English
	'Veröffentlicht', '', -- German
	'Publié', '', -- French
	'Pubblicato', '', -- Italian
	'Published', '', -- Romancio
	4
);

UPDATE public.borehole
SET version_id_cli=(
	select id_cli
	from codelist
	where schema_cli = 'version'
	and code_cli = 'E'
);

COMMENT ON SCHEMA public
  IS 'v1.190417';
