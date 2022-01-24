from fastapi import APIRouter, status, Response, Header
from routers.models.note_data import NewNote, SavedNote, Note
from routers.models.registration_form import validate_password
from api_utils.response_bodies import INVALID_NOTE_PASSWORD, COULD_NOT_CREATE_NOTE, COULD_NOT_SAVE_NOTE, \
	COULD_NOT_ACCESS_NOTE, TOKEN_VALIDATION_ERROR
from api_utils.token_picker import get_user_id_from_token
from db_utils.queries import create_new_note, save_note, get_note, get_all_notes
from typing import List, Optional

MODULE_TAG = "notes"

router = APIRouter()


# Check if user exists - might not be necessary (foreign key) - create smoother exceptioning
# what happens if passphrase not present? - create smoother exceptioning
@router.post("/note/new", tags=[MODULE_TAG], status_code=status.HTTP_201_CREATED)
async def create_note(new_note: NewNote, response: Response, token: Optional[List[str]] = Header(None)):
	owner_id = get_user_id_from_token(token)
	if not owner_id:
		response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
		return TOKEN_VALIDATION_ERROR
	is_encrypted = new_note.is_encrypted
	passphrase = new_note.passphrase.strip() if new_note.passphrase is not None else None
	if is_encrypted and not validate_password(passphrase):
		response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
		return INVALID_NOTE_PASSWORD
	query_result = create_new_note(owner_id, is_encrypted, passphrase)
	if not query_result:
		response.status_code = status.HTTP_502_BAD_GATEWAY
		return COULD_NOT_CREATE_NOTE
	return query_result


@router.put("/note/save", tags=[MODULE_TAG], status_code=status.HTTP_200_OK)
async def request_saving_note(saved_note: SavedNote, response: Response, token: Optional[List[str]] = Header(None)):
	owner_id = get_user_id_from_token(token)
	if not owner_id:
		response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
		return TOKEN_VALIDATION_ERROR
	query_result = save_note(saved_note.note_id, owner_id, saved_note.text)
	if not query_result:
		response.status_code = status.HTTP_502_BAD_GATEWAY
		return COULD_NOT_SAVE_NOTE
	return query_result


@router.get("/note/get", tags=[MODULE_TAG], status_code=status.HTTP_200_OK)
async def request_get_note(note: Note, response: Response, token: Optional[List[str]] = Header(None)):
	owner_id = get_user_id_from_token(token)
	if not owner_id:
		response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
		return TOKEN_VALIDATION_ERROR
	query_result = get_note(note.note_id, owner_id, note.passphrase)
	if not query_result:
		response.status_code = status.HTTP_403_FORBIDDEN
		return COULD_NOT_ACCESS_NOTE
	return query_result


@router.get("/note/get-all", tags=[MODULE_TAG], status_code=status.HTTP_200_OK)
async def request_all_notes(response: Response, token: Optional[List[str]] = Header(None)):
	owner_id = get_user_id_from_token(token)
	if not owner_id:
		response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
		return TOKEN_VALIDATION_ERROR
	return get_all_notes(owner_id)
