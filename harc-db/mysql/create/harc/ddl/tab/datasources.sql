CREATE TABLE datasources
(
  id                int(11) NOT NULL AUTO_INCREMENT primary key,
  name              varchar(255),
  type              varchar(50),
  host              varchar(255),
  sid               varchar(255),
  db                varchar(255),
  username          varchar(255),
  password          varchar(255),
  created_at        datetime,
  created_by        varchar(45),
  updated_at        datetime,
  updated_by        varchar(45)
);
