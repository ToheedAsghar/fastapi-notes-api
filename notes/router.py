from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status

from database import get_db
from notes.models import Note
from users.models import User
from users.security import get_current_user
from notes.schemas import NoteCreate, NoteResponse, NoteUpdate
from notes.storage import filter_notes, get_note_or_404, toggle_archive, delete_note, update_note, create_note

router = APIRouter(prefix="/notes", tags=["notes"])

@router.get("", response_model=list[NoteResponse])
def list_notes_endpoint(
    notes: Annotated[list[Note], Depends(filter_notes)]
):
    return notes

@router.get("/{note_id}", response_model=NoteResponse)
def get_note_endpoint(
    note: Annotated[Note, Depends(get_note_or_404)],
):
    return note

@router.post("", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def create_note_endpoint(
    note: NoteCreate,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)]
):
    return create_note(note, user, db)

@router.put("/{note_id}", response_model=NoteUpdate)
def update_note_endpoint(
        user: Annotated[User, Depends(get_current_user)],
        note: Annotated[Note, Depends(get_note_or_404)],
        updated_note: NoteCreate,
        db: Annotated[Session, Depends(get_db)]
):
    return update_note(note, updated_note, user, db)

@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note_endpoint(
    note: Annotated[Note, Depends(get_note_or_404)],
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
):
    return delete_note(note, db, user)

@router.patch("/{note_id}", response_model=NoteUpdate)
def toggle_archieve(
    note: Annotated[Note, Depends(get_note_or_404)],
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
):
    return toggle_archive(note, user, db)
