insert into commands(name, environment, statement) values ('paprika-hook-stop','dev','systemctl:stop -s paprika_hook.service -p oracle_user');
insert into commands(name, environment, statement) values ('paprika-hook-start','dev','systemctl:start -s paprika_hook.service -p oracle_user');
insert into commands(name, environment, statement) values ('paprika-message-stop','dev','systemctl:stop -s paprika_message.service -p oracle_user');
insert into commands(name, environment, statement) values ('paprika-message-start','dev','systemctl:start -s paprika_message.service -p oracle_user');
insert into commands(name, environment, statement) values ('paprika-pull-master','dev','paprika_pull_master.sh');
insert into commands(name, environment, statement) values ('paprika-install','dev','paprika_install.sh');