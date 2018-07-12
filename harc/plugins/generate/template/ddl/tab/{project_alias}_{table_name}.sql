create table {project_alias}_[table_name}
  (id                         number(12) not null,
   file_id                    number(12),
   stage_id                   number(12),
   job_name                   varchar2(255),
   created_at                 date,
   created_by                 varchar2(45),
   updated_at                 date,
   updated_by                 varchar2(45),
   {table_fields}
) nologging;

alter table {project_alias}_{table_name} add constraint {project_alias}_{table_alias}id_pk primary key (id) using index nologging;
alter table {project_alias}_{table_name} add constraint {project_alias}_{table_alias}created_at_nn check (created_at is not null);
alter table {project_alias}_{table_name} add constraint {project_alias}_{table_alias}created_by_nn check (created_by is not null);
alter table {project_alias}_{table_name} add constraint {project_alias}_{table_alias}job_name_nn   check (job_name   is not null);
alter table {project_alias}_{table_name} add constraint {project_alias}_{table_alias}updated_at_nn check (updated_at is not null);
alter table {project_alias}_{table_name} add constraint {project_alias}_{table_alias}updated_by_nn check (updated_by is not null);

{table_field_constraints}