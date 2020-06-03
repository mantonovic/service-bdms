
UPDATE
  bdms.config
SET
  value_cfg = '1.0.1-RC1'
WHERE
  name_cfg = 'VERSION';

UPDATE
  bdms.config
SET
  value_cfg = '1.0.0'
WHERE
  name_cfg = 'PREVIOUS';

UPDATE
  bdms.config
SET
  value_cfg = '1.0.0-RC1'
WHERE
  name_cfg = 'GEOLCODES';

CREATE TABLE bdms.files (
    id_fil serial,
    id_usr_fk integer,
    name_fil character varying NOT NULL,
    description_fil character varying NOT NULL,
    hash_fil character varying NOT NULL,
    type_fil character varying NOT NULL,
    uploaded_fil timestamp with time zone DEFAULT now(),
    conf_fil json,
    PRIMARY KEY (id_fil),
    CONSTRAINT files_id_usr_fkey FOREIGN KEY (id_usr_fk)
        REFERENCES bdms.users (id_usr) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
);

CREATE TABLE bdms.borehole_files
(
    id_bho_fk integer NOT NULL,
    id_fil_fk integer NOT NULL,
    id_usr_fk integer,
    attached_bfi timestamp with time zone DEFAULT now(),
    update_bfi timestamp with time zone DEFAULT now(),
    updater_bfi integer,
    description_bfi character varying,
    public_bfi boolean DEFAULT true,
    PRIMARY KEY (id_bho_fk, id_fil_fk),
    CONSTRAINT borehole_files_id_usr_fkey FOREIGN KEY (id_usr_fk)
        REFERENCES bdms.users (id_usr) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
);
