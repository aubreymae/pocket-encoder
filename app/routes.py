import os

from flask import Blueprint, current_app, request
from werkzeug.utils import secure_filename
from redis import Redis
from rq import Queue

from .db import create_video, set_rq_job_id

ALLOWED_EXTENSIONS = {"mp4", "mov"}

api = Blueprint("api", __name__)

redis_connection = Redis.from_url("redis://localhost:6379")

queue = Queue(
    connection=redis_connection
)

def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )

@api.route("/process", methods=["POST"])
def process_video():
    # 1. Check that a file was uploaded
    if "file" not in request.files:
        return {"error": "No file provided."}, 400

    file = request.files["file"]

    # 2. Check that the file has a name
    if file.filename == "":
        return {"error": "No selected file provided."}, 400

    # 3. Check that the file type is allowed
    if not allowed_file(file.filename):
        return {"error": "File type not allowed."}, 400

    # 4. Make the filename safe
    filename = secure_filename(file.filename)

    # 5. Save the uploaded file
    upload_path = os.path.join(
        current_app.config["UPLOAD_FOLDER"],
        filename
    )

    file.save(upload_path)

    # 6. Get target size
    raw_size = request.form.get("target_size_mb")
    target_size_mb = float(raw_size) if raw_size else 25.0

    # 7. Create database record
    video_id = create_video(
        filename,
        upload_path,
        target_size_mb
    )

    from tasks import process_video as process_video_task

    # 8. Queue the video for processing
    job = queue.enqueue(process_video_task, video_id)

    set_rq_job_id(
    video_id,
    job.id
)

    return {
        "message": "Upload successful",
        "video_id": video_id,
        "filename": filename,
        "status": "Queued"
    }, 202