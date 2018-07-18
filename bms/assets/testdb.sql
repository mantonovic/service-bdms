insert into boreholes (name_brh)
  (
      select md5(random()::text)
      from generate_Series(1,1000) as s
  );
