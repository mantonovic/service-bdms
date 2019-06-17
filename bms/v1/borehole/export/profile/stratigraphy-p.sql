SELECT
	row_to_json(t2)
	FROM
		(SELECT
			id_bho as idb,
			'Switzerland' as country,
		 	cant_j.name as canton,
			mun_j.name as city,
			address_bho as address,
		 	cli_kind.text_cli_{} as kind,
			location_x_bho as location_e,
			location_y_bho as location_n,
		 	elevation_z_bho as elevation_z,
		 	cli_srs.text_cli_{} as srs,
            cli_hrs.text_cli_{} as hrs,
            length_bho as length,
		 	drilling_date_bho as drilling_date,
			cli_restriction.text_cli_{} as restriction,
			to_char(
				restriction_until_bho,
				'YYYY-MM-DD'
			) as restrictoin_until,
		 	cli_purpose.text_cli_{} as purpose,
			cli_landuse.text_cli_{} as landuse,
			cli_cuttings.text_cli_{} as cuttings,
			cli_method.text_cli_{} as method,
			cli_status.text_cli_{} as status,
			drill_diameter_bho as drill_diameter,
			bore_inc_bho as bore_inc,
			bore_inc_dir_bho as bore_inc_dir,
		 	project_name_bho as project_name,
			'12345' as auth_n,
		    original_name_bho as original_name,
		    public_name_bho as public_name,
            strat_j.name_sty as strataname,
            strat_j.date_sty as stratadate,
			'IFEC' as logged_by,
			'swisstopo' as checked_by,
			groundwater_bho as groundwater,

			(SELECT
				array_to_json(
					array_agg(
						row_to_json(t)
					)
				)
				FROM (
					SELECT
						id_lay as id,
						id_sty as id_sty,
						depth_from_lay as depth_from,
						depth_to_lay as depth_to,
						CASE
							WHEN elevation_z_bho is NULL THEN NULL
							ELSE elevation_z_bho - depth_from_lay
						END AS msm_from,
						CASE
							WHEN elevation_z_bho is NULL THEN NULL
							ELSE elevation_z_bho - depth_to_lay
						END AS msm_to,
						cli_lithostra.text_cli_{} as lithostratigraphy,
                        cli_lithostra.conf_cli as conf_lithostra,
						cli_lithostra.geolcode as geolcode_lithostra,
						cli_lithology.text_cli_{} as lithology,
                        cli_lithology.conf_cli as conf_lithology,
						description_lay as layer_desc,
						geology_lay as geol_desc,
						name_sty as name_st,
						notes_lay as notes
					FROM
						{}.layer
							LEFT JOIN {}.codelist as cli_lithostra
								ON cli_lithostra.id_cli = lithostratigraphy_id_cli
							LEFT JOIN {}.codelist as cli_lithology
								ON cli_lithology.id_cli = lithology_id_cli,
						{}.stratigraphy,
						{}.borehole
					WHERE
						id_sty_fk = id_sty
					AND
						id_sty = %s
					AND
						id_bho_fk = id_bho
					AND
						id_bho = strat_j.id_bho_fk
					ORDER BY depth_from_lay, id_lay

			) AS t
		 ) AS layers 
		 FROM 
		 	{}.borehole
		 LEFT JOIN {}.codelist as cli_kind
			ON cli_kind.id_cli = kind_id_cli
		 LEFT JOIN {}.codelist as cli_srs
			ON cli_srs.id_cli = srs_id_cli
		 LEFT JOIN {}.codelist as cli_hrs
			ON cli_hrs.id_cli = hrs_id_cli
		 LEFT JOIN {}.codelist as cli_restriction
			ON cli_restriction.id_cli = restriction_id_cli
		 LEFT JOIN {}.codelist as cli_purpose
			ON cli_purpose.id_cli = purpose_id_cli
		 LEFT JOIN {}.codelist as cli_method
		 	ON cli_method.id_cli = method_id_cli
		 LEFT JOIN {}.codelist as cli_landuse
			ON cli_landuse.id_cli =landuse_id_cli
		 LEFT JOIN {}.codelist as cli_status
			ON cli_status.id_cli =status_id_cli
		 LEFT JOIN {}.codelist as cli_cuttings
			ON cli_cuttings.id_cli = cuttings_id_cli
         LEFT JOIN {}.municipalities as mun_j
			ON mun_j.gid = city_bho
         LEFT JOIN {}.cantons as cant_j
			ON cant_j.gid = canton_bho
         LEFT JOIN (
             SELECT id_sty, date_sty, name_sty, id_bho_fk 
             FROM {}.stratigraphy
             --WHERE primary_sty = true
         ) as strat_j ON strat_j.id_sty = %s
         		 
		 WHERE
		 	id_bho = id_bho_fk
            AND
            strat_j.id_sty = %s
	 ) AS t2
	
    
    
