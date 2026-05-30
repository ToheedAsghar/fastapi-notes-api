from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, Query,status

from database import get_db
from users.models import User
from notes.models import Note
from notes.schemas import NoteCreate
from users.security import get_current_user

def get_note_or_404(
        note_id: int,
        db: Annotated[Session, Depends(get_db)],
        user: Annotated[User, Depends(get_current_user)],
) -> Note:
    note = db.query(Note).filter(Note.id == note_id, Note.owner_id == user.id).first()

    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

def create_note(
        note_data: NoteCreate,
        current_user: User,
        db: Session,
) -> Note:
    new_note = Note(
        **note_data.model_dump(),
        owner_id = current_user.id
    )
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

def delete_note(
        note: Note,
        db: Session,
        user: User,
) -> None:
    if int(note.owner_id) != user.id:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Note not found")
    db.delete(note)
    db.commit() 

def update_note(
        note: Note,
        updated_note: NoteCreate,
        user: User,
        db: Session,
) -> Note:
    if int(note.owner_id) != user.id:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Note not found")
    
    for field, value in updated_note.model_dump().items():
        setattr(note, field, value)
    
    db.commit()
    db.refresh(note)
    return note

def toggle_archive(
        note: Note,
        user: User,
        db: Session,
) -> Note:
    if int(note.owner_id) != user.id:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="Note not found")
    
    note.is_archived = not bool(note.is_archived)
    db.commit()
    db.refresh(note)
    return note

def filter_notes(
        db: Annotated[Session, Depends(get_db)],
        user: Annotated[User, Depends(get_current_user)],
        title: str = Query(default=""),
        skip: int = Query(default=0, ge=0),
        limit: int = Query(default=10, ge=1, le=20),
        
) -> list[Note]:
    
    query = db.query(Note)

    if title is not None:
        query = query.filter(Note.title.ilike(f"%{title}%"), Note.owner_id == user.id)
    
    return query.offset(skip).limit(limit).all()

def get_no_of_notes(db: Session):
    return db.query(Note).count()