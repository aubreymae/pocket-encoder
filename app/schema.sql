drop table if exists videos;

create table videos (
    id integer primary key autoincrement,
    filename text unique not null,
    filesize integer
);