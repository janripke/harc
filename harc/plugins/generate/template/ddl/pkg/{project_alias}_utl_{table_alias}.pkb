create or replace package body {project_alias}_utl_{table_alias} as

  M_PACKAGE_NAME               constant varchar2(50) := lower($$plsql_unit);


  function count_by_job_name
    (p_job_name in varchar2) return number is

    l_count  number(12);

  begin
    select count(0)
    into   l_count
    from   {project_alias}_{table_name}
    where  job_name = p_job_name
    ;

    return l_count;
  end;


  function get_
    (p_{table_alias}_id in {project_alias}_{table_name}.id%type) return {project_alias}_{table_name}%rowtype is

    cursor c_get (b_{table_alias}_id {project_alias}_{table_name}.id%type) is
      select *
      from   {project_alias}_{table_name}
      where  id = b_{table_alias}_id;
    r_get c_get%rowtype;

  begin
    open c_get(b_{table_alias}_id => p_{table_alias}_id);
    fetch c_get into r_get;
    close c_get;
    return r_get;
  end;


  function insert_
    (p_job_name in varchar2
    ,p_{stage_table_alias}      in {project_alias}_{table_name}_stage%rowtype) return number is

    l_id   number(12);
    l_prc_name   varchar2(255):='insert_';

  begin
    insert into {project_alias}_{table_name}
      (  file_id
       , stage_id
       , job_name
       , {table_field}
       ) values
      ( p_{stage_table_alias}.file_id
      , p_{stage_table_alias}.id
      , p_{stage_table_alias}.job_name
      , p_{stage_table_alias}.{table_field}
      )
      returning id into l_id
      log errors into {project_alias}_{table_name}_err reject limit 0;

      logger.debug(p_job_name, M_PACKAGE_NAME, l_prc_name, 'inserted {project_alias}_{table_name} with id :' || l_id);
      return l_id;
  end;


end maq_utl_ssn;
/