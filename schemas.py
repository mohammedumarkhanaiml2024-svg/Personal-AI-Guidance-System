from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

class DailyLogCreate(BaseModel):
    date: str
    habits: str
    mood: str
    activities: str

class DailyLogOut(BaseModel):
    id: int
    date: str
    habits: str
    mood: str
    activities: str

    class Config:
        orm_mode = True