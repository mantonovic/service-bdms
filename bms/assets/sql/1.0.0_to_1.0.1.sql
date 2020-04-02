CREATE TABLE bdms.stratigraphy_codelist
(
    id_sty_fk integer NOT NULL,
    id_cli_fk integer NOT NULL,
    code_cli character varying NOT NULL,
    CONSTRAINT stratigraphy_codelist_pkey PRIMARY KEY (id_sty_fk, id_cli_fk),
    CONSTRAINT stratigraphy_codelist_id_sty_fk_id_cli_fk_code_cli_key
        UNIQUE (id_sty_fk, id_cli_fk, code_cli),
    CONSTRAINT stratigraphy_codelist_id_cli_fk_fkey FOREIGN KEY (id_cli_fk)
        REFERENCES bdms.codelist (id_cli) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT stratigraphy_codelist_id_sty_fk_fkey FOREIGN KEY (id_sty_fk)
        REFERENCES bdms.stratigraphy (id_sty) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
);

DELETE FROM bdms.codelist
WHERE id_cli = 3000;

DELETE FROM bdms.codelist
WHERE id_cli = 3001;

INSERT INTO bdms.codelist (
    id_cli, geolcode,
    schema_cli, code_cli,
    text_cli_de, description_cli_de,
    text_cli_fr, description_cli_fr,
    text_cli_it, description_cli_it,
    text_cli_en, description_cli_en,
    order_cli, conf_cli,
    default_cli, path_cli
) VALUES (
    3000, 3000,
    'layer_kind', 'Geol',
    'Geologie', '',
    'Géologie', '',
    'Geologia', '',
    'Geology', '',
    1, 
    '{"color": "lithostratigraphy", "colorNS": "custom.lit_str_top_bedrock", "pattern": "lithology", "patternNS": "custom.lit_pet_top_bedrock", "fields": {"color": false, "notes": true, "debris": false, "striae": false, "uscs_1": false, "uscs_2": false, "uscs_3": false, "geology": false, "cohesion": false, "humidity": false, "jointing": false, "lithology": true, "alteration": false, "plasticity": false, "soil_state": false, "compactness": false, "consistance": false, "description": true, "grain_shape": false, "lit_pet_deb": false, "grain_size_1": false, "grain_size_2": false, "tectonic_unit": false, "uscs_original": false, "qt_description": false, "grain_granularity": false, "lithostratigraphy": true, "organic_component": false, "chronostratigraphy": true, "further_properties": false, "uscs_determination": false}}',
    TRUE,
    ''
);

INSERT INTO bdms.codelist (
    id_cli, geolcode,
    schema_cli, code_cli,
    text_cli_de, description_cli_de,
    text_cli_fr, description_cli_fr,
    text_cli_it, description_cli_it,
    text_cli_en, description_cli_en,
    order_cli, conf_cli,
    default_cli, path_cli
) VALUES (
    3001, 3001,
    'layer_kind', 'GTec',
    'Geotechnische', '',
    'Géotechnique', '',
    'Geotecnica', '',
    'Geotechnical', '',
    2,
    '{"color": null, "colorNS": null, "pattern": "uscs_1", "patternNS": "mcla101", "fields": {"color": false, "notes": true, "debris": false, "striae": false, "uscs_1": false, "uscs_2": false, "uscs_3": false, "geology": false, "cohesion": false, "humidity": false, "jointing": false, "lithology": true, "alteration": false, "plasticity": false, "soil_state": false, "compactness": false, "consistance": false, "description": true, "grain_shape": false, "lit_pet_deb": false, "grain_size_1": false, "grain_size_2": false, "tectonic_unit": false, "uscs_original": false, "qt_description": false, "grain_granularity": false, "lithostratigraphy": true, "organic_component": false, "chronostratigraphy": true, "further_properties": false, "uscs_determination": false}}',
    FALSE, ''
);

INSERT INTO bdms.stratigraphy_codelist
    SELECT id_sty, 3000, 'layer_kind'
    FROM bdms.stratigraphy;

DELETE FROM bdms.codelist
WHERE id_cli = 3002;

--ALTER TABLE bdms.stratigraphy DROP COLUMN kind_id_cli;

CREATE TABLE bdms.config
(
    name_cfg character varying NOT NULL,
    value_cfg character varying,
    PRIMARY KEY (name_cfg)
);

INSERT INTO bdms.config(
    name_cfg, value_cfg
)
VALUES
    ('VERSION', '1.0.0'),
    ('PREVIOUS', NULL),
    ('GEOLCODES', '1.0.0-beta'),
    ('INSTALLATION', to_char(now(), 'YYYY-MM-DD"T"HH24:MI:SSOF')),
    ('PG_UPGRADE', NULL),
    (
        'SETTINGS',
        '{'
        '   "defaults": {'
        '       "stratigraphy": 3002'
        '   },'
        '   "filter": {},'
        '   "efilter": {},'
        '   "boreholetable": {'
        '        "orderby": "original_name",'
        '        "direction": "ASC"'
        '    },'
        '    "eboreholetable": {'
        '        "orderby": "creation",'
        '        "direction": "DESC"'
        '    },'
        '   "map": {'
        '       "explorer": {},'
        '       "editor": {}'
        '   },'
        '   "appearance": {'
        '       "explorer": 1'
        '   }'
        '}'
    );

-- Merging any exisitng user settings
UPDATE
    bdms.users
SET
    settings_usr = (
        (
            SELECT value_cfg::jsonb
            FROM bdms.config
            WHERE name_cfg = 'SETTINGS'
        ) || settings_usr::jsonb
    )::text
WHERE
    settings_usr IS NOT NULL;

CREATE TABLE bdms.borehole_codelist
(
    id_bho_fk integer NOT NULL,
    id_cli_fk integer NOT NULL,
    code_cli character varying NOT NULL,
    value_bco character varying NOT NULL,
    CONSTRAINT borehole_codelist_pkey PRIMARY KEY (id_bho_fk, id_cli_fk),
    CONSTRAINT borehole_codelist_id_bho_fk_id_cli_fk_code_cli_key
        UNIQUE (id_bho_fk, id_cli_fk, code_cli),
    CONSTRAINT borehole_codelist_id_cli_fk_fkey FOREIGN KEY (id_cli_fk)
        REFERENCES bdms.codelist (id_cli) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT borehole_codelist_id_bho_fk_fkey FOREIGN KEY (id_bho_fk)
        REFERENCES bdms.borehole (id_bho) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
);

INSERT INTO bdms.codelist (
    id_cli, geolcode,
    schema_cli, code_cli,
    text_cli_de, description_cli_de,
    text_cli_fr, description_cli_fr,
    text_cli_it, description_cli_it,
    text_cli_en, description_cli_en,
    order_cli, conf_cli,
    default_cli, path_cli
) VALUES (
    1036, 1036,
    'borehole_form', 'borehole_identifier',
    'Kennung', '',
    'Identificateur', '',
    'Identificatore', '',
    'Identifier', '',
    37, NULL,
    false, ''
);
INSERT INTO bdms.codelist (
    id_cli, geolcode,
    schema_cli, code_cli,
    text_cli_de, description_cli_de,
    text_cli_fr, description_cli_fr,
    text_cli_it, description_cli_it,
    text_cli_en, description_cli_en,
    order_cli, conf_cli,
    default_cli, path_cli
) VALUES (
    1037, 1037,
    'borehole_form', 'identifier_value',
    'Codice', '',
    'Code', '',
    'Code', '',
    'Code', '',
    38, NULL,
    false, ''
);

INSERT INTO bdms.codelist (
    geolcode,
    schema_cli, code_cli,
    text_cli_de, description_cli_de,
    text_cli_fr, description_cli_fr,
    text_cli_it, description_cli_it,
    text_cli_en, description_cli_en,
    order_cli, conf_cli,
    default_cli, path_cli
) VALUES (
    100000000, 100000000,
    'borehole_identifier', 'GTec',
    'Eindeutige ID', '',
    'Identifiant unique', '',
    'ID univoco', '',
    'Unique id', '',
    1, NULL,
    FALSE, ''
);

SELECT setval('bdms.codelist_id_cli_seq', 100000001, true);