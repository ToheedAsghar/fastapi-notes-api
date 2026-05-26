from pydantic import Field, BaseModel

class NoteCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1, max_length=10000)
    is_archived: bool = Field(default=False)

class NoteResponse(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1, max_length=10000)

    model_config = {"from_attributes": True}

class NoteUpdate(BaseModel):
    id: int = Field(default=-1)
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1, max_length=10000)
    is_archived: bool = Field(default=False)
