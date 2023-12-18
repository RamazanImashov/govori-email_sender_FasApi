from .database import Base, engine, SessionLocal
from fastapi import FastAPI, status, Depends, BackgroundTasks
from src import schemas, models
from src.tasks import send_email_bg
from sqlalchemy.orm import Session


Base.metadata.create_all(engine)

app = FastAPI()


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@app.post('/task', response_model=schemas.Tasks, status_code=status.HTTP_201_CREATED)
def send_email_client(background_tasks: BackgroundTasks, tasks: schemas.TasksCreate, session: Session = Depends(get_session)):
    tasks = models.Tasks(types=tasks.types, price=tasks.price,
                         name_type=tasks.name_type, username=tasks.username,
                         emails=tasks.emails, phone_number=tasks.phone_number)
    background_tasks.add_task(send_email_bg, types=tasks.types, price=tasks.price,
                              name_type=tasks.name_type, username=tasks.username,
                              emails=tasks.emails, phone_number=tasks.phone_number)
    session.add(tasks)
    session.commit()
    return tasks
