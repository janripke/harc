alter table {project_alias}_{table_name}stage add constraint {project_alias}_{stage_table_alias}file_fk foreign key(file_id) references files(id) novalidate;