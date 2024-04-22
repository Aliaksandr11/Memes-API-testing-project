from pydantic import BaseModel


class SchemaUserAuth(BaseModel):
    token: str
    user: str


class SchemaInfoMeme(BaseModel):
    rating: int
    type: list
    user: str


class SchemaAddMeme(BaseModel):
    id: int
    text: str
    url: str
    tags: list
    info: SchemaInfoMeme
    updated_by: str

