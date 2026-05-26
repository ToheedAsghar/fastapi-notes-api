from fastapi import APIRouter, status

from notes.schemas import NoteCreate, NoteResponse, NoteUpdate

router = APIRouter(prefix="/notes", tags=["notes"])

@router.get("", response_model=NoteResponse)
def list_notes_endpoint():
    ...

@router.get("/{note_id}", response_model=NoteResponse)
def get_note_endpoint():
    ...

@router.post("", response_model=NoteResponse)
def create_note_endpoint():
    ...

@router.put("/{note_id}", response_model=NoteUpdate):
def update_note_endpoint():
    ...

@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note_endpoint():
    ...

@router.patch("/{note_id}", response_model=NoteUpdate)
def toggle_archieve():
    ...