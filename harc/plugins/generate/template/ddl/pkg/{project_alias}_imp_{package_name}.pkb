create or replace package body {project_alias}_imp_{package_name} as
  M_PACKAGE_NAME              constant varchar2(256) := lower($$plsql_unit);
  M_JOB_PREFIX                constant varchar2(255) := '{project_alias}_imp_{table_alias}$';
  M_FOLDER                    constant varchar2(255) := '{package_folder}';
  M_STAGE_TABLE               constant varchar2(255) := '{project_alias}_{table_name}_stage';



  -- raise an error when there are no rows imported.
  procedure fail_on_no_rows(p_job_name in varchar2) is

    l_count     number(12);
    l_prc_name  varchar2(255) := 'fail_on_no_rows';

  begin

    select count(0)
    into   l_count
    from   {project_alias}_{table_name}
    where  job_name = p_job_name;

    logger.debug(p_job_name, M_PACKAGE_NAME, l_prc_name, 'l_count: '||l_count);

    if l_count = 0 then
      raise_application_error(-20101, app_utl.G_NO_ROWS);
    end if;
  end fail_on_no_rows;


  -- raise an error when there are no rows imported.
  procedure fail_on_treshold
    (p_job_name      in varchar2
    ,p_treshold      in number
    ,p_records_total in number
    ,p_records_error in number) is

    l_actual    number(12);
    l_prc_name  varchar2(255) := 'fail_on_treshold';

  begin

    l_actual := p_records_error / p_records_total;
    logger.debug(p_job_name, M_PACKAGE_NAME, l_prc_name, 'actual: ' || l_actual || ' treshold: '|| p_treshold);

    if l_actual >= p_treshold then
      raise_application_error(-20107, app_utl.G_TRESHOLD);
    end if;
  end fail_on_treshold;


  function transform
    (p_test_mode in varchar2
    ,p_job_name in varchar2) return number is

    cursor c_stage is
      select *
      from   {project_alias}_{table_name}_stage
      where  job_name = p_job_name
      ;

    l_prc_name                 varchar2(255) := 'transform';
    l_count                    number(12) := 0;
    l_{table_alias}_id                   number(12);
    
  begin

    for r_stage in c_stage loop
      savepoint savepoint_stage;

      begin

        l_{table_alias}_id := maq_utl_{table_alias}.insert_(p_job_name, r_stage);
        l_count := l_count + 1;

      exception
        when others then
          logger.trace(p_job_name,M_PACKAGE_NAME,l_prc_name,substr(sqlerrm,1,4000));
          rollback to savepoint_stage;
      end;

    end loop;

    logger.info(p_job_name,M_PACKAGE_NAME,l_prc_name,l_count || ' record(s) ok.');
    return l_count;

  end;


  function start_import
    (p_job_name  in varchar2
    ,p_filename  in varchar2
    ,p_test_mode in varchar2 default 'Y') return varchar2 is

    l_result            varchar2(255) := app_utl.G_OK;
    l_file_header       varchar2(4000);
    l_treshold          number(12);
    l_skip_header_yn    varchar2(4000);
    l_ext_columns       varchar2(4000);
    l_field_list        app_utl.t_field_list;
    l_records_ok        number(12) := 0;
    l_records_staged_ok number(12) := 0;
    l_records_error     number(12) := 0;
    l_prc_name          varchar2(256) := 'start_import';
    l_file              files%rowtype;

    l_log_filename      varchar2(255);
    l_ni_filename       varchar2(255);


    e_invalid_file_header    exception;
    e_no_rows                exception;
    e_not_imported_rows      exception;
    e_unhandled_error        exception;
    e_treshold               exception;
    pragma exception_init(e_invalid_file_header, -20100);
    pragma exception_init(e_no_rows, -20101);
    pragma exception_init(e_not_imported_rows, -20103);
    pragma exception_init(e_unhandled_error, -20106);
    pragma exception_init(e_unhandled_error, -20107);


  begin
    logger.info(p_job_name, M_PACKAGE_NAME, l_prc_name, 'started');

    l_file.job_name    := p_job_name;
    l_file.filename    := p_filename;
    l_file.status_code := app_utl.G_STATUS_PROCESSING;
    l_file.filetype    := M_JOB_PREFIX;
    l_file             := register.register_file(p_file => l_file);

    l_skip_header_yn  := app_props.get_property('{project_alias}_imp_{package_name}.skip_header_yn');
    l_ext_columns     := app_props.get_property('{project_alias}_imp_{package_name}.ext_columns');
    l_file_header     := app_props.get_property('{project_alias}_imp_{package_name}.file_header');
    l_treshold        := app_props.get_property('{project_alias}_imp_{package_name}.treshold');

    app_utl.fail_on_invalid_file_header
      (p_job_name      => p_job_name
      ,p_folder        => M_FOLDER
      ,p_filename      => p_filename
      ,p_file_header   => l_file_header);

    -- Define external table columns
    l_field_list := app_utl.get_field_list_of_varchar4000(l_ext_columns,app_utl.G_DELIMITER_PIPE);

    app_utl.create_external_table
      (p_job_name               => p_job_name
      ,p_folder                 => M_FOLDER
      ,p_filename               => p_filename
      ,p_tablename              => p_job_name
      ,p_skip_header_yn         => l_skip_header_yn
      ,p_field_delimiter        => app_utl.G_DELIMITER_PIPE
      ,p_optionally_enclosed_yn => app_utl.G_YES
      ,p_field_list             => l_field_list);

    l_records_staged_ok := stager.stage
      (p_job_name         => p_job_name
      ,p_file_id          => l_file.id
      ,p_table_name       => p_job_name
      ,p_stage_table_name => M_STAGE_TABLE
      ,p_field_list       => l_field_list);

    -- transfer the records in stage table to the datamodel
    l_records_ok := transform
      (p_test_mode => p_test_mode
      ,p_job_name  => p_job_name);

    -- Log all errors that occured
    l_records_error := stager.errors
      (p_job_name         => p_job_name
      ,p_table_name       => M_STAGE_TABLE);

    -- Create <filename>.ORA file
    l_log_filename := app_utl.change_filename_extension(p_filename, 'ora');
    stager.create_log_file
      (p_job_name => p_job_name
      ,p_folder   => M_FOLDER
      ,p_filename => l_log_filename);


    -- When errors where found
    l_ni_filename := app_utl.change_filename_extension(p_filename, 'ni');
    if l_records_error <> 0 then
      stager.create_ni_file
        (p_job_name        => p_job_name
        ,p_folder          => M_FOLDER
        ,p_filename        => l_ni_filename
        ,p_file_header     => l_file_header
        ,p_table_name      => M_STAGE_TABLE
        ,p_field_list      => l_field_list
        ,p_delimiter       => app_utl.G_DELIMITER_PIPE);
    end if;


    app_utl.drop_external_table
      (p_job_name  => p_job_name
      ,p_tablename => p_job_name);

    -- Faal wanneer het stage totaal niet overeenkomt met het aantal geimporteerd (goed en fout)
    app_utl.fail_on_unhandled_error
      (p_job_name      => p_job_name
      ,p_records_total => l_records_staged_ok
      ,p_records_ok    => l_records_ok
      ,p_records_error => l_records_error);

    fail_on_no_rows(p_job_name => p_job_name);

    fail_on_treshold
      (p_job_name      => p_job_name
      ,p_treshold      => l_treshold
      ,p_records_total => l_records_staged_ok
      ,p_records_error => l_records_error);

    l_file.status_code   := app_utl.G_STATUS_IMPORTED;
    l_file.records_total := l_records_staged_ok;
    l_file.records_ok    := l_records_ok;
    l_file.records_error := l_records_error;
    l_file               := register.register_file(p_file  => l_file);

    if nvl(p_test_mode, app_utl.G_YES) = app_utl.G_NO then
      commit;
    end if;

    app_utl.fail_on_not_imported_rows
      (p_job_name      => p_job_name
      ,p_records_error => l_records_error);

    logger.info(p_job_name, M_PACKAGE_NAME, l_prc_name, 'finished');
    return l_result;

  exception

     when e_invalid_file_header then
      rollback;
      logger.error(p_job_name,M_PACKAGE_NAME,l_prc_name,app_utl.G_INVALID_FILE_HEADER);

      l_file.status_code := app_utl.G_STATUS_ERROR;
      l_file:=register.register_file
        (p_file  => l_file);

      apm_log.log_fatal
        (p_pcs_code => M_PACKAGE_NAME
        ,p_job_name => p_job_name
        ,p_message  => app_utl.G_INVALID_FILE_HEADER ||chr(10)||
                       p_filename
        );

      logger.info(p_job_name, M_PACKAGE_NAME, l_prc_name, 'finished');
      return app_utl.G_INVALID_FILE_HEADER;

    when e_no_rows then
      rollback;
      logger.error(p_job_name,M_PACKAGE_NAME,l_prc_name,app_utl.G_NO_ROWS);

      l_file.status_code := app_utl.G_STATUS_ERROR;
      l_file.records_total := l_records_staged_ok;
      l_file.records_ok := 0;
      l_file.records_error := l_records_staged_ok;
      l_file:=register.register_file
        (p_file  => l_file);
      logger.info(p_job_name, M_PACKAGE_NAME, l_prc_name, 'finished');

      apm_log.log_fatal
        (p_pcs_code => M_PACKAGE_NAME
        ,p_job_name => p_job_name
        ,p_message  => app_utl.G_NO_ROWS ||chr(10)||
                       p_filename
        );

      return app_utl.G_NO_ROWS;

    when e_treshold then
      rollback;
      logger.error(p_job_name,M_PACKAGE_NAME,l_prc_name,app_utl.G_TRESHOLD);

      l_file.status_code := app_utl.G_STATUS_ERROR;
      l_file.records_total := l_records_staged_ok;
      l_file.records_ok := 0;
      l_file.records_error := l_records_staged_ok;
      l_file:=register.register_file
        (p_file  => l_file);
      logger.info(p_job_name, M_PACKAGE_NAME, l_prc_name, 'finished');

      apm_log.log_fatal
        (p_pcs_code => M_PACKAGE_NAME
        ,p_job_name => p_job_name
        ,p_message  => app_utl.G_TRESHOLD ||chr(10)||
                       p_filename
        );

      return app_utl.G_TRESHOLD;

    when e_not_imported_rows then
      logger.error(p_job_name,M_PACKAGE_NAME,l_prc_name,app_utl.G_NOT_IMPORTED_ROWS);

      l_file.status_code := app_utl.G_STATUS_ERROR;
      l_file:=register.register_file
        (p_file  => l_file);

      apm_log.log_warning
        (p_pcs_code => M_PACKAGE_NAME
        ,p_job_name => p_job_name
        ,p_message  => app_utl.G_NOT_IMPORTED_ROWS ||chr(10)||
                       p_filename
        );

      logger.info(p_job_name, M_PACKAGE_NAME, l_prc_name, 'finished');
      return app_utl.G_NOT_IMPORTED_ROWS;

    when e_unhandled_error then
      rollback;
      logger.fatal(p_job_name,M_PACKAGE_NAME,l_prc_name,app_utl.G_UNHANDLED);
      l_file.status_code := app_utl.G_STATUS_ERROR;
      l_file.records_total := l_records_staged_ok;
      l_file.records_ok    := l_records_ok;
      l_file.records_error := l_records_error;
      l_file:=register.register_file
        (p_file  => l_file);

      apm_log.log_fatal
        (p_pcs_code => M_PACKAGE_NAME
        ,p_job_name => p_job_name
        ,p_message  => app_utl.G_UNHANDLED ||chr(10)||
                       p_filename
        );

      logger.info(p_job_name, M_PACKAGE_NAME, l_prc_name, 'finished');
      return app_utl.G_UNHANDLED;

    when others then
      rollback;
      logger.fatal(p_job_name, M_PACKAGE_NAME, l_prc_name, substr(sqlerrm, 1, 4000));

      app_utl.drop_external_table
        (p_job_name  => p_job_name
        ,p_tablename => p_job_name);

      if l_file.id is null then
         l_file.job_name    := p_job_name;
         l_file.filename    := p_filename;
         l_file.filetype    := M_JOB_PREFIX;
      end if;
      l_file.status_code := app_utl.G_STATUS_ERROR;
      l_file:=register.register_file
        (p_file  => l_file);

      apm_log.log_fatal
        (p_pcs_code => M_PACKAGE_NAME
        ,p_job_name => p_job_name
        ,p_message  => p_filename ||chr(10)||
                       substr(sqlerrm, 1, 200)
        );
      logger.info(p_job_name, M_PACKAGE_NAME, l_prc_name, 'finished');
      return substr(sqlerrm, 1, 255);
  end start_import;


  -- wrapper for ctm and fuse.
  procedure import
    (p_job_name   in varchar2 default null
    ,p_bestand    in varchar2
    ,po_resultaat out varchar2) is

    l_job_name varchar2(255):=p_job_name;
    l_prc_name varchar2(255) := 'import';

  begin
    if l_job_name is null then
      l_job_name := app_utl.get_job_name(M_JOB_PREFIX);
    end if;

    po_resultaat := start_import
      (p_job_name  => l_job_name
      ,p_filename  => p_bestand
      ,p_test_mode => app_utl.G_NO);

    logger.debug(l_job_name,M_PACKAGE_NAME,l_prc_name,'po_resultaat: '||po_resultaat);

  exception
    when others then
      logger.fatal(l_job_name,M_PACKAGE_NAME,l_prc_name,substr(sqlerrm, 1, 4000));
      po_resultaat := substr(sqlerrm, 1, 255);
  end;

end {project_alias}_imp_{package_name};
/
