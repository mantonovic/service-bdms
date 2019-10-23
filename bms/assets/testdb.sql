insert into boreholes (
    author_id, contact_id, created_bho, update_bho, updater_bho,
    locked_at, locked_by, id_wgp_fk, published_bho, public_bho, kind_id_cli,
    location_x_bho, location_y_bho, srs_id_cli, elevation_z_bho, hrs_id_cli,
    length_bho, date_bho, restriction_id_cli, restriction_until_bho,
    original_name_bho, public_name_bho, qt_location_id_cli,
    qt_elevation_id_cli, address_bho, landuse_id_cli, project_name_bho,
    canton_bho, city_bho, method_id_cli, drilling_date_bho,
    cuttings_id_cli, purpose_id_cli, drill_diameter_bho,
    status_id_cli, bore_inc_bho, bore_inc_dir_bho,
    qt_bore_inc_dir_id_cli, qt_length_id_cli, top_bedrock_bho,
    qt_top_bedrock_id_cli, groundwater_bho, geom_bho, mistakes_bho,
    remarks_bho, processing_status_id_cli, national_relevance_id_cli,
    lithology_id_cli, lithostrat_id_cli, chronostrat_id_cli, tecto_id_cli
) VALUES (
    SELECT md5(random()::text)
    FROM
        generate_Series(1,1000) as s
);
