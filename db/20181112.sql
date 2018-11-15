ALTER TABLE public.borehole
    ADD COLUMN lithology_id_cli integer;

ALTER TABLE public.borehole
    ADD COLUMN lithostrat_id_cli integer;

ALTER TABLE public.borehole
    ADD COLUMN chronostrat_id_cli integer;

ALTER TABLE public.borehole
    ADD COLUMN tecto_id_cli integer;

CREATE INDEX bho_idx
    ON public.borehole USING gist
    (geom_bho)
    TABLESPACE pg_default;

ALTER TABLE public."user"
    ADD COLUMN settings_usr character varying;

ALTER TABLE public."user"
    RENAME TO users;
