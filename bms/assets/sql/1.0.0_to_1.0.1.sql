CREATE TABLE bdms.stratigraphy_codelist
(
    id_sty_fk integer NOT NULL,
    id_cli_fk integer NOT NULL,
    CONSTRAINT stratigraphy_codelist_pkey PRIMARY KEY (id_sty_fk, id_cli_fk),
    CONSTRAINT stratigraphy_codelist_id_cli_fk_fkey FOREIGN KEY (id_cli_fk)
        REFERENCES bdms.codelist (id_cli) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT stratigraphy_codelist_id_sty_fk_fkey FOREIGN KEY (id_sty_fk)
        REFERENCES bdms.stratigraphy (id_sty) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
);

INSERT INTO bdms.stratigraphy_codelist
    SELECT id_sty, kind_id_cli
    FROM bdms.stratigraphy;

ALTER TABLE bdms.stratigraphy DROP COLUMN kind_id_cli;
