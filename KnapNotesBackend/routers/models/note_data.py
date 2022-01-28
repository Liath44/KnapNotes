from pydantic import BaseModel
from typing import Optional


class NewNote(BaseModel):
	is_encrypted: bool
	passphrase: Optional[str] = None


class SavedNote(BaseModel):
	note_id: int
	text: str


class Note(BaseModel):
	note_id: int
	passphrase: Optional[str] = None


class PublicNoteUpdate(BaseModel):
	note_id: int
