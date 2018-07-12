CREATE TABLE sessions
(
  id           int(11) NOT NULL AUTO_INCREMENT primary key,
  hashcode     varchar(255),
  active       int(1) NOT NULL DEFAULT 1,
  created_at   datetime,
  created_by   varchar(45),
  updated_at   datetime,
  updated_by   varchar(45)
);