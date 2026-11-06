from sqlmodel import Field, SQLModel


class Videos(SQLModel, table=True):
    id: int  | None = Field(default=None, primary_key=True)
    titulo: str
    source: str
    es_publico: bool
    categoria: str = Field(default="General")

class VideosCreate(SQLModel):
    titulo: str
    source: str
    es_publico: bool = True


class Comment(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    video_id: int = Field(foreign_key="videos.id")
    nombre: str
    texto: str


class CommentCreate(SQLModel):
    nombre: str
    texto: str


class CommentUpdate(SQLModel):
    nombre: str
    texto: str