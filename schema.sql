drop table if exists users;

create table users (
  id integer primary key autoincrement,
  fullname char(35) not null,
  email char(35) not null,
  pw_hash char(35) not null
);
