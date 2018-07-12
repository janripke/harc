begin
  dbms_errlog.create_error_log('{project_alias}_{table_name}','{project_alias}_{table_name}_err');
end;
/