UPDATE public.stratigraphy
SET kind_id_cli=(
	SELECT
		id_cli
	FROM
		codelist
	WHERE
		schema_cli = 'layer_kind'
	AND
		default_cli IS TRUE	
);

COMMENT ON SCHEMA public
  IS 'v1.190521';
