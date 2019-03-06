ALTER TABLE public.users
    ADD COLUMN firstname character varying;

ALTER TABLE public.users
    ADD COLUMN middlename character varying;

ALTER TABLE public.users
    ADD COLUMN lastname character varying;

COMMENT ON SCHEMA public
  IS 'v1.190306';
