drop table if exists videos;

create table videos (
    id integer primary key autoincrement,
    rq_job_id TEXT,
    filename text not null,
    input_path text not null,
    output_path text,
    target_size_mb real,
    status text not null check(status in ('Queued', 'Processing', 'Completed', 'Failed')),
    error_message text,
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp
);