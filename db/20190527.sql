DROP TABLE public.domains;

CREATE TABLE public.roles
(
    id_rol integer NOT NULL,
    name_rol character varying NOT NULL,
    config_rol json,
    PRIMARY KEY (id_rol)
);

INSERT INTO public.roles(
    id_rol, name_rol, config_rol
) VALUES (
    0, 'VIEW', '{}'
);

INSERT INTO public.roles(
    id_rol, name_rol, config_rol
) VALUES (
    1, 'EDIT', '{}'
);

INSERT INTO public.roles(
    id_rol, name_rol, config_rol
) VALUES (
    2, 'CONTROL', '{}'
);

INSERT INTO public.roles(
    id_rol, name_rol, config_rol
) VALUES (
    3, 'VALID', '{}'
);

INSERT INTO public.roles(
    id_rol, name_rol, config_rol
) VALUES (
    4, 'PUBLIC', '{}'
);

ALTER TABLE public.borehole
DROP CONSTRAINT borehole_version_id_cli_fkey;

ALTER TABLE public.borehole
DROP COLUMN version_id_cli;

-- ALTER TABLE public.borehole
-- ADD COLUMN id_grp_fk integer;

-- ALTER TABLE public.borehole
-- ADD COLUMN id_rol_fk integer;

-- ALTER TABLE public.borehole
-- ADD FOREIGN KEY (id_rol_fk)
--     REFERENCES public.roles (id_rol) MATCH SIMPLE
--     ON UPDATE NO ACTION
--     ON DELETE NO ACTION;

-- UPDATE public.borehole
-- SET id_rol_fk = 1;

CREATE TABLE public.workgroups
(
    id_wgp serial NOT NULL,
    name_wgp character varying NOT NULL,
    settings_wgp json,
    PRIMARY KEY (id_wgp),
    UNIQUE (name_wgp)
);

CREATE TABLE public.users_roles
(
    id_usr_fk integer NOT NULL,
    id_rol_fk integer NOT NULL,
    id_wgp_fk integer NOT NULL,
    PRIMARY KEY (id_rol_fk, id_usr_fk, id_wgp_fk)
    FOREIGN KEY (id_usr_fk)
        REFERENCES public.users (id_usr) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE,
    FOREIGN KEY (id_rol_fk)
        REFERENCES public.roles (id_rol) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    FOREIGN KEY (id_wgp_fk)
        REFERENCES public.workgroups (id_wgp) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);

ALTER TABLE public.users_roles
    ADD PRIMARY KEY (id_usr_fk, id_rol_fk, id_wgp_fk);

CREATE TABLE public.groups
(
    id_grp serial NOT NULL,
    name_grp character varying NOT NULL,
    PRIMARY KEY (id_grp)
);

ALTER TABLE public.users
    ADD COLUMN id_rol_fk integer;

ALTER TABLE public.users
    ADD COLUMN admin_usr boolean DEFAULT FALSE;

ALTER TABLE public.users
    ADD FOREIGN KEY (id_rol_fk)
    REFERENCES public.roles (id_rol) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;

ALTER TABLE public.users
    ADD COLUMN id_grp_fk integer;

ALTER TABLE public.users
    ADD FOREIGN KEY (id_grp_fk)
    REFERENCES public.groups (id_grp) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;

INSERT INTO public.users_roles
VALUES(1, 1);

INSERT INTO public.users_roles
VALUES(1, 2);

INSERT INTO public.users_roles
VALUES(2, 1);

INSERT INTO public.users_roles
VALUES(2, 2);

INSERT INTO public.groups(id_grp, name_grp) VALUES (0, 'admin');

-- UPDATE public.borehole
-- SET id_grp_fk = 0;

UPDATE public.users
SET
    admin_usr=TRUE,
    id_grp_fk = 0
WHERE
    username = 'admin';

-- Creating demo users

INSERT INTO public.users(
    id_usr,
    username, password,
    firstname, middlename, lastname,
    admin_usr, id_grp_fk
)
VALUES (
    4,
    'viewer', 'viewer',
    'Viewer', '', 'Demo',
    FALSE, 0
);

INSERT INTO public.users_roles
VALUES(4, 0);

INSERT INTO public.users(
    id_usr,
    username, password,
    firstname, middlename, lastname,
    admin_usr, id_grp_fk
)
VALUES (
    5,
    'editor', 'editor',
    'Editor', '', 'Demo',
    FALSE, 0
);

INSERT INTO public.users_roles
VALUES(5, 1);

INSERT INTO public.users(
    id_usr,
    username, password,
    firstname, middlename, lastname,
    admin_usr, id_grp_fk
)
VALUES (
    6,
    'controller', 'controller',
    'Controller', '', 'Demo',
    FALSE, 0
);

INSERT INTO public.users_roles
VALUES(6, 2);

INSERT INTO public.users(
    id_usr,
    username, password,
    firstname, middlename, lastname,
    admin_usr, id_grp_fk
)
VALUES (
    7,
    'validator', 'validator',
    'Validator', '', 'Demo',
    FALSE, 0
);

INSERT INTO public.users_roles
VALUES(7, 3);

INSERT INTO public.users(
    id_usr,
    username, password,
    firstname, middlename, lastname,
    admin_usr, id_grp_fk
)
VALUES (
    8,
    'publisher', 'publisher',
    'Publisher', '', 'Demo',
    FALSE, 0
);

INSERT INTO public.users_roles
VALUES(8, 4);

SELECT setval('public.user_id_usr_seq', 10, true);

INSERT INTO public.codelist(
    schema_cli, code_cli,
    text_cli_en, description_cli_en,
    text_cli_de, description_cli_de,
    text_cli_it, description_cli_it,
    order_cli
)
VALUES
(
    'borehole_form', 'original_name',
    'Original name', '',
    'Originalname', '',
    'Nome originario', '',
    1
),
(
    'borehole_form', 'public_name',
    'Public name', '',
    'Öffentlicher Name', '',
    'Nome pubblico', '',
    2
),
(
    'borehole_form', 'kind',
    'Drilling type', '',
    'Bohrtyp', '',
    'Tipologia di perforazione', '',
    2
),
(
    'borehole_form', 'method',
    'Drilling method', '',
    'Bohrmethode', '',
    'Metodologia di perforazione', '',
    3
),
(
    'borehole_form', 'project_name',
    'Project name', '',
    'Projektname', '',
    'Nome progetto', '',
    4
),
(
    'borehole_form', 'restriction',
    'Restriction', '',
    'Restriktion', '',
    'Restrizione', '',
    5
),
(
    'borehole_form', 'restriction_until',
    'Restriction date', '',
    'Restriktion Datum', '',
    'Data restrizione', '',
    6
),
(
    'borehole_form', 'landuse',
    'Land use', '',
    'Landnutzung', '',
    'Uso del suolo', '',
    7
),
(
    'borehole_form', 'canton',
    'Canton', '',
    'Kanton', '',
    'Cantone', '',
    8
),
(
    'borehole_form', 'city',
    'City', '',
    'Gemeinde', '',
    'Città', '',
    9
),
(
    'borehole_form', 'address',
    'Address', '',
    'Addresse', '',
    'Indirizzo', '',
    10
),
(
    'borehole_form', 'elevation_z',
    'Elevation (masl)', '',
    'Ansatzhöhe (müM)', '',
    'Altitudine (msl)', '',
    11
),
(
    'borehole_form', 'length',
    'Depth (MD) (m)', '',
    'Tiefe (MD) (m)', '',
    'Profondità (MD) (m)', '',
    12
),
(
    'borehole_form', 'groundwater',
    'Groundwater', '',
    'Grundwasser', '',
    'Groundwater', '',
    13
),
(
    'borehole_form', 'top_bedrock',
    'Top bedrock', '',
    'Top Fels', '',
    'Top substrato', '',
    14
),
(
    'borehole_form', 'status',
    'Status of borehole', '',
    'Status Bohrloch', '',
    'Stato del sondaggio', '',
    15
),
(
    'borehole_form', 'purpose',
    'Purpose', '',
    'Bohrzweck', '',
    'Scopo', '',
    16
),
(
    'borehole_form', 'cuttings',
    'Cuttings', '',
    'Schnitt', '',
    'Taglio', '',
    17
),
(
    'borehole_form', 'drilling_date',
    'Drill end date', '',
    'Bohrende Datum', '',
    'Data fine perforazione', '',
    18
),
(
    'borehole_form', 'drill_diameter',
    'Drill diameter (m)', '',
    'Bohrdurchmesser (m)', '',
    'Diametro perforazione (m)', '',
    19
),
(
    'borehole_form', 'bore_inc',
    'Inclination (°)', '',
    'Inklination (°)', '',
    'Inclinazione (°)', '',
    20
),
(
    'borehole_form', 'lit_pet_top_bedrock',
    'Lit/Pet Top bedrock', '',
    'Lit/Pet Top Fels', '',
    'Lit/Pet Top substrato', '',
    21
),
(
    'borehole_form', 'lit_str_top_bedrock',
    'Litstrati top bedrock', '',
    'Litstrati Top Fels', '',
    'Litstrati top substrato', '',
    22
),
(
    'borehole_form', 'chro_str_top_bedrock',
    'Chronostrati top bedrock', '',
    'Chronostrati Top Fels', '',
    'Chronostrati top substrato', '',
    23
);

CREATE TABLE public.workflow
(
    id_wkf serial NOT NULL,
    id_bho_fk integer NOT NULL,
    id_usr_fk integer NOT NULL,
    id_rol_fk integer NOT NULL,
    started_wkf timestamp without time zone,
    finished_wkf timestamp without time zone,
    mentions_wkf character varying[],
    notes_wkf character varying,
    PRIMARY KEY (id_wkf),
    FOREIGN KEY (id_bho_fk)
        REFERENCES public.borehole (id_bho) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE,
    FOREIGN KEY (id_usr_fk)
        REFERENCES public.users (id_usr) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    FOREIGN KEY (id_rol_fk)
        REFERENCES public.roles (id_rol) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);

-- ALTER TABLE public.users_roles
--     ADD COLUMN id_wgp_fk integer;

-- ALTER TABLE public.users_roles
--     ADD UNIQUE (id_usr_fk, id_rol_fk, id_wgp_fk);

ALTER TABLE public.users_roles
    ADD FOREIGN KEY (id_wgp_fk)
    REFERENCES public.workgroups (id_wgp) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;

ALTER TABLE public.borehole
    ADD COLUMN id_wgp_fk integer;

ALTER TABLE public.borehole
    ADD FOREIGN KEY (id_wgp_fk)
    REFERENCES public.workgroups (id_wgp) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;

INSERT INTO public.workgroups(
    id_wgp, name_wgp, settings_wgp)
    VALUES (0, 'default', '{}');

UPDATE public.borehole
    SET id_wgp_fk=0;

UPDATE public.users_roles
    SET id_wgp_fk=0;

UPDATE public.users_roles
    SET id_wgp_fk=0;

COMMENT ON SCHEMA public
  IS 'v1.190527';
