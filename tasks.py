from app import create_app
from app.db import get_video, update_video_status

QUEUED_LABEL = "Queued"
PROCESSING_LABEL = "Processing"
COMPLETED_LABEL = "Completed"
FAILED_LABEL = "Failed"

app = create_app()

def process_video(video_id):
    with app.app_context():
        video = get_video(video_id)
    
        if video is None:
            print(f"Video {video_id} was not found.")
            return

        update_video_status(video_id, PROCESSING_LABEL)
    
        print(f"Processing {video['filename']}")
    
        # Add video processing here
        print("Doing fake video processing...")

        update_video_status(
            video_id,
            COMPLETED_LABEL
        )

        update_video_status(video_id, COMPLETED_LABEL)