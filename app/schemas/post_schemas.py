from pydantic import BaseModel

class PostCreate(BaseModel):
    title: str
    description: str
    category: str

class PostOut(BaseModel):
    id: str
    title: str
    description: str
    category: str
    author_id: str
    created_at: str

    class Config:
        from_attributes = True