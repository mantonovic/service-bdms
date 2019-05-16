UPDATE public.codelist
	SET
		code_cli='U'
		text_cli_en='Unfinished',
		text_cli_de='Unfertig', 
		text_cli_fr='Incomplet', 
		text_cli_it='Incompleto'
	WHERE
		schema_cli = 'version'
	AND
		text_cli_en = 'Editing';

UPDATE public.codelist
	SET
		code_cli='V'
	WHERE
		schema_cli = 'version'
	AND
		text_cli_en = 'Validation';

UPDATE public.codelist
	SET
		code_cli='P'
	WHERE
		schema_cli = 'version'
	AND
		text_cli_en = 'Published';

COMMENT ON SCHEMA public
  IS 'v1.190516';
