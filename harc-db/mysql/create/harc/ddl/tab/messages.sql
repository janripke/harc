CREATE TABLE messages
(
  id                int(11) NOT NULL AUTO_INCREMENT primary key,
  hashcode          varchar(255),
  state             varchar(50),
  payload           varchar(4000),
  agent             varchar(100),
  consumer          varchar(512),
  message           varchar(4000),
  backtrace         varchar(4000),
  created_at        datetime,
  created_by        varchar(45),
  updated_at        datetime,
  updated_by        varchar(45)
);