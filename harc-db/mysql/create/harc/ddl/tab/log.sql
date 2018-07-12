CREATE TABLE log
(
  id                     int(11) NOT NULL AUTO_INCREMENT primary key,
  logtype_code           varchar(50),
  job_name               varchar(255),
  package_name           varchar(255),
  method_name            varchar(255),
  message                mediumtext,
  uniq_session_id        varchar(255),
  format_error_backtrace varchar(4000),
  format_error_stack     varchar(4000),
  format_call_stack      varchar(4000),
  created_at             datetime,
  created_by             varchar(45),
  updated_at             datetime,
  updated_by             varchar(45)
);
