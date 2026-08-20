drop table if exists videos;

create table videos (
    id integer primary key autoincrement,
    filename text unique not null,
    filesize integer
);

create table jobs (
    job_id integer primary key autoincrement,
    job_status text unique not null,
    timestamp datetime default current_timestamp
);