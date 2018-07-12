create table {project_alias}_{table_name}_stage
  (id                         number(12) not null,
   file_id                    number(12),
   line_id                    number(12),
   job_name                   varchar2(255),
   created_at                 date,
   created_by                 varchar2(45),
   updated_at                 date,
   updated_by                 varchar2(45),
   {table_fields_stage}
) nologging;

alter table {project_alias}_{table_name}_stage add constraint {project_alias}_{table_alias}_id_pk primary key (id) using index nologging;