create index {project_alias}_{table_alias}_file_id_idx on {project_alias}_{table_name}(file_id) nologging tablespace ts_index;
create index {project_alias}_{table_alias}_job_name_idx on {project_alias}_{table_name}(job_name) nologging tablespace ts_index;
create index {project_alias}_{table_alias}_stage_id_idx on {project_alias}_{table_name}(stage_id) nologging tablespace ts_index;