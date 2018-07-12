CREATE TABLE jobs
(
  id          int(11) NOT NULL AUTO_INCREMENT primary key,
  created_at  datetime,
  created_by  varchar(45),
  updated_at  datetime,
  updated_by  varchar(45)
);