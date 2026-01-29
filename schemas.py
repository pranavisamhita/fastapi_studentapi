from pydantic import BaseModel, Field

class Book(BaseModel):
    title: str = Field(min_length=1)
    author: str
    description: str
    rating: int = Field(gt=-1, lt=101)

    class Config:
        orm_mode = True

