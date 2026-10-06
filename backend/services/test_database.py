from sqlmodel import SQLModel, Session, select

from ..database import engine
from ..models import Job, Thumbnail


SQLModel.metadata.create_all(engine)

with Session(engine) as session:
    job = Job(
        id="test-job-1",
        prompt="Test thumbnail",
        headshot_url="example.png",
        status="pending"
    )

    session.add(job)

    thumbnail1 = Thumbnail(
        job_id=job.id,
        style_name="style1",
        status="pending"
    )

    session.add(thumbnail1)

    session.commit()
    print("Job created:", job.id)
    print("Thumbnail 1:", thumbnail1.id)

with Session(engine) as session:
    job = session.get(Job, "test-job-1")
    print("Retrived:")
    print(job)

with Session(engine) as session:

    thumbnails = session.exec(
        select(Thumbnail).where(
            Thumbnail.job_id == "test-job-1"
        )
    ).all()

    for thumbnail in thumbnails:
        print(
            thumbnail.id,
            thumbnail.style_name,
            thumbnail.status
        )   
