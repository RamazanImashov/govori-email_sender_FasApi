from .database import Base, engine, SessionLocal
from fastapi import FastAPI, status, Depends, BackgroundTasks
from src import schemas, models
from src.tasks import send_email_bg
from sqlalchemy.orm import Session
from typing import List
from fastapi.middleware.cors import CORSMiddleware


Base.metadata.create_all(engine)

app = FastAPI()


origins = [
    "http://localhost:3000",
    "http://localhost",
    "https://course-lake.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)


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


@app.get('/get_task', response_model=List[schemas.Tasks], status_code=status.HTTP_200_OK)
def get_task(session: Session = Depends(get_session)):
    task = session.query(models.Tasks).all()
    return task


@app.get('/get_task/{task_id}', response_model=List[schemas.Tasks], status_code=status.HTTP_200_OK)
def get_task_id(task_id: int, session: Session = Depends(get_session)):
    tasks = session.query(models.Tasks).all()
    return [tas for tas in tasks if tas.id == task_id]
