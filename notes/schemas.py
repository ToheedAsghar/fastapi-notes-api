from pydantic import Field, BaseModel

class NoteCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1, max_length=10000)
    is_archived: bool = Field(default=False)

class NoteResponse(BaseModel):
    id: int
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1, max_length=10000)
    is_archived: bool = Field(default=False)

    model_config = {"from_attributes": True}
