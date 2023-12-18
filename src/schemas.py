from pydantic import BaseModel


class Tasks(BaseModel):
    id: int
    types: str
    price: float
    name_type: str
    username: str
    emails: str
    phone_number: str


class TasksCreate(BaseModel):
    types: str
    price: float
    name_type: str
    username: str
    emails: str
    phone_number: str
