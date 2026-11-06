from fastapi import APIRouter, HTTPException, Response, status
from sqlmodel import delete, func, select

from db import SessionDep
from models import Comment, CommentCreate, CommentUpdate, Videos, VideosCreate

router = APIRouter(prefix="/videos")


def find_video(video_id: int, session: SessionDep):
    video = session.get(Videos, video_id)
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El video no fue encontrado",
        )
    return video


@router.get("/")
def get_videos(
    session: SessionDep,
    categoria: str | None = None,
    q: str | None = None,
):
    query = select(Videos).where(Videos.es_publico == True)
    if categoria:
        query = query.where(Videos.categoria == categoria)
    if q:
        query = query.where(Videos.titulo.contains(q))
    return session.exec(query.order_by(Videos.id)).all()


@router.get("/categorias")
def get_categories(session: SessionDep):
    query = (
        select(Videos.categoria)
        .where(Videos.es_publico == True)
        .distinct()
        .order_by(Videos.categoria)
    )
    return session.exec(query).all()


@router.get("/{video_id}/recomendaciones")
def get_recommendations(video_id: int, session: SessionDep):
    video = find_video(video_id, session)
    query = (
        select(Videos)
        .where(
            Videos.es_publico == True,
            Videos.categoria == video.categoria,
            Videos.id != video_id,
        )
        .order_by(func.random())
        .limit(10)
    )
    return session.exec(query).all()


@router.get("/{video_id}")
def get_video_by_id(video_id: int, session: SessionDep):
    return find_video(video_id, session)


@router.delete("/{video_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_video(video_id: int, session: SessionDep):
    video = find_video(video_id, session)
    session.exec(delete(Comment).where(Comment.video_id == video_id))
    session.delete(video)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_videos(video_data: VideosCreate, session: SessionDep):
    video = Videos.model_validate(video_data.model_dump())
    session.add(video)
    session.commit()
    session.refresh(video)
    return video


@router.get("/{video_id}/comentarios")
def get_comments(video_id: int, session: SessionDep):
    find_video(video_id, session)
    query = select(Comment).where(Comment.video_id == video_id).order_by(Comment.id)
    return session.exec(query).all()


@router.post(
    "/{video_id}/comentarios", status_code=status.HTTP_201_CREATED
)
def create_comment(video_id: int, comment_data: CommentCreate, session: SessionDep):
    find_video(video_id, session)
    comment = Comment(video_id=video_id, **comment_data.model_dump())
    session.add(comment)
    session.commit()
    session.refresh(comment)
    return comment


@router.put("/comentarios/{comment_id}")
def update_comment(
    comment_id: int, comment_data: CommentUpdate, session: SessionDep
):
    comment = session.get(Comment, comment_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El comentario no fue encontrado",
        )
    comment.nombre = comment_data.nombre
    comment.texto = comment_data.texto
    session.add(comment)
    session.commit()
    session.refresh(comment)
    return comment


@router.delete(
    "/comentarios/{comment_id}", status_code=status.HTTP_204_NO_CONTENT
)
def delete_comment(comment_id: int, session: SessionDep):
    comment = session.get(Comment, comment_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El comentario no fue encontrado",
        )
    session.delete(comment)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)