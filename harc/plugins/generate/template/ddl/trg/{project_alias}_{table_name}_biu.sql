create or replace trigger {project_alias}_{table_name}_bui
  before insert or update on {project_alias}_{table_name}
  for each row
declare
  -- local variables here
begin
  if inserting
  then
    if :new.id is null
    then
      select {project_alias}_{table_alias}_seq.nextval
      into   :new.id
      from   dual;
    end if;
    :new.created_by := user;
    :new.created_at := sysdate;
  end if;
  :new.updated_by := user;
  :new.updated_at := sysdate;
end;
/