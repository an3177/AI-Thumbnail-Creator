import asyncio
import logging

from sqlmodel import Session, select
from database import engine
from models import Job, Thumbnail
from services.openai_service import generate_thumbnail
from services.imagekit_service import upload_file

logger = logging.getLogger(__name__)

STYLES = {
    #add later
}

STYLE_ORDER =[]

async def generate_single_thumbnail(thumbnail_id:str, prompt:str, headshot_url: str):
    # DB mark _> generating
    with Session(engine) as session:
        thumb = session.get(Thumbnail, thumbnail_id)
        thumb.status = "generating"
        style_name = thumb.style_name
        session.add(thumb)
        session.commit()

    style_prompt = STYLES[style_name]
    # AI call
    try:
        image_byte = await generate_thumbnail(prompt, style_prompt, headshot_url)
        with Session(engine) as session:
            thumb = session.get(Thumbnail, thumbnail_id)
            job_id = thumb.job_id
        # upload this image
        url = upload_file(
           file_bytes=image_byte,
           file_name=f"{thumbnail_id}.png",
           folder_path=f"thumbnails/{job_id}/",
        )
            # DB call save the url + mark uploaded
        with Session(engine) as session:
           thumb = session.get(Thumbnail, thumbnail_id)
           thumb.imagekit_url = url
           thumb.status = "uploaded"
           session.add(thumb)
           session.commit()
        logger.info(f"Thumbnail {thumbnail_id} generated and uploaded successfully")
    except Exception as e:
        logger.error(f"Error generating thumbnail {thumbnail_id}: {e}")
        with Session(engine) as session:
           thumb = session.get(Thumbnail, thumbnail_id)
           thumb.status = "error"
           thumb.error_message = str(e)[:500]
           session.add(thumb)
           session.commit()

async def process_job(job_id:str):
   #mark job as processing
   #find all thumbnails for this job
   #start one worker for each thumbnail
   #wait for all wrokers to finish
   #mark job as completed/failed
    with Session(engine) as session:
       job = session.get(Job, job_id)
       job.status = "processing"
       prompt = job.prompt
       headshot_url = job.headshot_url
       session.add(job)
       session.commit()
           

