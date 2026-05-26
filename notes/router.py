from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status

from database import get_db
from notes.models import Note
from notes.storage import filter_notes, get_note_or_404, toggle_archive, delete_note, update_note, create_note
from notes.schemas import NoteCreate, NoteResponse, NoteUpdate

router = APIRouter(prefix="/notes", tags=["notes"])

@router.get("", response_model=NoteResponse)
def list_notes_endpoint(notes: Annotated[list[Note], Depends(filter_notes)]):
    return notes

@router.get("/{note_id}", response_model=NoteResponse)
def get_note_endpoint(
    note: Annotated[Note, Depends(get_note_or_404)],
):
    return note

@router.post("", response_model=NoteResponse)
def create_note_endpoint(
    note: NoteCreate,
    db: Annotated[Session, Depends(get_db)]
):
    return create_note(note, None, db)

@router.put("/{note_id}", response_model=NoteUpdate):
def update_note_endpoint(
        note: Annotated[Note, Depends(get_note_or_404)],
        updated_note: NoteCreate,
        db: Annotated[Session, Depends(get_db)]
):
    return update_note(note, updated_note, db)

@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note_endpoint(
    note: Annotated[Note, get_note_or_404],
    db: Annotated[Session, Depends(get_db)]
):
    return delete_note(note, db)

@router.patch("/{note_id}", response_model=NoteUpdate)
def toggle_archieve(
    note: Annotated[Note, get_note_or_404],
    db: Annotated[Session, Depends(get_db)]
):
    return toggle_archive(note, db)
