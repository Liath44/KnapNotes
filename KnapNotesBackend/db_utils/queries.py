from db_utils.connector import create_session
from db_utils.base_models import User, ActiveCookie, Note, KeysForNote
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from logging import exception
from datetime import datetime
from utils.security_utils import create_new_key_pair, encrypt, decrypt, create_salt, get_hash, \
	hash_and_validate_password

# at some point I will have to greatly refactor this module...
DEFAULT_NOTE = "My new awesome note :^]"
MESSAGES_KEY = "messages"


def is_username_in_db(username):
	session = create_session()
	n_users = session.query(User).filter_by(username=username).count()
	session.close()
	return n_users >= 1


def create_user(username, password, salt):
	user = User(username=username, password=password, salt=salt)
	session = create_session()
	session.add(user)
	try:
		session.commit()
		return True
	except SQLAlchemyError as error:
		exception(error)
		session.rollback()
		return False
	finally:
		session.close()


def get_authentication_data(username):
	session = create_session()
	user_data = session.query(User.username, User.id, User.password, User.salt).filter_by(username=username).first()
	session.close()
	return user_data.id, user_data.password, user_data.salt


def insert_token_to_db(token, user_id):
	expiration_date = func.adddate(func.now(), +1)
	active_cookie = ActiveCookie(cookie=token, expiration_date=expiration_date, user_id=user_id)
	session = create_session()
	session.add(active_cookie)
	try:
		session.commit()
		return True
	except SQLAlchemyError as error:
		exception(error)
		session.rollback()
		return False
	finally:
		session.close()


def create_new_note(owner_id, is_encrypted, passphrase):
	note = None
	keys_for_note = None
	private_key = None
	public_key = None
	text = None
	if is_encrypted:
		# use hashed passphrase instead of raw one ???
		private_key, public_key = create_new_key_pair(passphrase)
		text = encrypt(public_key, DEFAULT_NOTE)
		note = Note(owner_id=owner_id, text=text, is_encrypted=is_encrypted, is_public=False)
	else:
		text = DEFAULT_NOTE
		note = Note(owner_id=owner_id, text=text, is_encrypted=is_encrypted, is_public=False)
	session = create_session()
	session.add(note)
	try:
		session.commit()
		note_id = note.id
		if is_encrypted:
			salt = create_salt()
			passphrase = get_hash(passphrase, salt)
			keys_for_note = KeysForNote(
				note_id=note_id,
				public_key=public_key,
				private_key=private_key,
				password=passphrase,
				salt=salt
			)
			session.add(keys_for_note)
			session.commit()
		return {
			"note_id": note_id,
			"text": text,
			"is_encrypted": is_encrypted
		}
	except SQLAlchemyError as error:
		exception(error)
		session.rollback()
		return False
	finally:
		session.close()


def get_user_id(token):
	session = create_session()
	token_data = session.query(ActiveCookie.user_id, ActiveCookie.cookie, ActiveCookie.expiration_date).filter_by(cookie=token).first()
	if token_data is None or token_data.expiration_date < datetime.now():
		return False
	session.close()
	return token_data.user_id


# check if user is owner
def save_note(note_id, user_id, text):
	session = create_session()
	try:
		note_entry = session.query(Note.id, Note.owner_id, Note.text, Note.is_encrypted).filter_by(id=note_id)
		note_data = note_entry.first()
		if note_data is None or not note_data.owner_id == user_id:
			return False  # invalid user or note_id
		if note_data.is_encrypted:
			key_data = session.query(KeysForNote.note_id, KeysForNote.public_key).filter_by(note_id=note_id).first()
			text = encrypt(key_data.public_key, text)
		session.query(Note).filter(Note.id == note_id).update({"text": text})
		session.commit()
		return {
			"text": text,
			"owner_id": note_data.owner_id,
			"note_id": note_data.id,
			"is_encrypted": note_data.is_encrypted
		}
	except SQLAlchemyError as error:
		exception(error)
		session.rollback()
		return False
	finally:
		session.close()


def get_note(note_id, user_id, passphrase):
	session = create_session()
	try:
		note_entry = session.query(Note.id, Note.owner_id, Note.text, Note.is_encrypted).filter_by(id=note_id)
		note_data = note_entry.first()
		if note_data is None or not note_data.owner_id == user_id:
			return False  # invalid user or note_id
		text = note_data.text
		if note_data.is_encrypted:
			passphrase = passphrase.strip()
			key_data = session.query(
				KeysForNote.note_id,
				KeysForNote.private_key,
				KeysForNote.salt,
				KeysForNote.password
			).filter_by(note_id=note_id).first()
			if not hash_and_validate_password(key_data.password, passphrase, key_data.salt):
				return False
			text = decrypt(key_data.private_key, passphrase, text)
		session.commit()
		return {
			"text": text,
			"owner_id": note_data.owner_id,
			"note_id": note_data.id,
			"is_encrypted": note_data.is_encrypted
		}
	except SQLAlchemyError as error:
		exception(error)
		session.rollback()
		return False
	finally:
		session.close()


def get_all_notes(user_id):
	session = create_session()
	notes = session.query(Note.id, Note.owner_id, Note.text, Note.is_encrypted).filter_by(owner_id=user_id).all()
	outcome = {MESSAGES_KEY: []}
	for note_record in notes:
		outcome[MESSAGES_KEY].append({
			"note_id": note_record[0],
			"owner_id": note_record[1],
			"text": note_record[2],
			"is_encrypted": note_record[3]
		})
	return outcome
