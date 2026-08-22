import sqlite3
import click

from flask import current_app, g

QUEUED_LABEL = "Queued"

"""Get the database connection"""
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
    return g.db

"""Close the database connection when request is finished"""
def close_db(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

"""Initialize the database"""
def init_db():
    db = get_db()

    with current_app.open_resource("./schema.sql") as f:
        db.executescript(f.read().decode("utf8"))

@click.command("init-db")
def init_db_command():
    init_db()
    click.echo("Initialized the database.")

"""Helper functions"""
def create_video(filename, input_path, target_size_mb):
    db = get_db()

    cursor = db.execute(
        """
        INSERT INTO Videos (filename, input_path, target_size_mb, status) VALUES (?, ?, ?, ?)
        """,
        (filename, input_path, target_size_mb, QUEUED_LABEL)
    )
    db.commit()
    return cursor.lastrowid

def update_video_status(video_id, target_status, error_message=None):
    db = get_db()

    cursor = db.execute(
        """
        UPDATE Videos SET status = ?, error_message = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?
        """,
        (target_status, error_message, video_id)
    )
    db.commit()

def get_video(video_id):
    db = get_db()

    return db.execute(
        """
        SELECT * FROM Videos WHERE id = ?
        """,
        (video_id,)
    ).fetchone()

def set_rq_job_id(video_id, rq_job_id):
    db = get_db()

    db.execute(
        """
        UPDATE videos
        SET rq_job_id = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """,
        (rq_job_id, video_id)
    )

    db.commit()

"""Tell Flask how to manage database"""
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)