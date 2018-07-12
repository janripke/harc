begin
  dbms_errlog.create_error_log('{project_alias}_{table_name}_stage','{project_alias}_{table_name}_stage_err');
end;
/