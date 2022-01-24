from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	username = Column(String(30), nullable=False)
	password = Column(String(128), nullable=False)
	salt = Column(String(200), nullable=False)


class Note(Base):
	__tablename__ = "notes"

	id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
	text = Column(String(16000), nullable=False)
	is_encrypted = Column(Boolean, nullable=False)
	is_public = Column(Boolean, nullable=False)


class LastLogins(Base):
	__tablename__ = "last_logins"

	id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
	login_1 = Column(DateTime)
	login_2 = Column(DateTime)
	login_3 = Column(DateTime)
	login_4 = Column(DateTime)
	login_5 = Column(DateTime)


class KeysForNote(Base):
	__tablename__ = "keys_for_notes"

	id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	note_id = Column(Integer, ForeignKey("notes.id"), nullable=False)
	public_key = Column(String(100), nullable=False)
	private_key = Column(String(100), nullable=False)
	password = Column(String(128), nullable=False)
	salt = Column(String(200), nullable=False)


class ActiveCookie(Base):
	__tablename__ = "active_cookies"

	id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
	cookie = Column(String(100), nullable=False)
	expiration_date = Column(DateTime, nullable=False)
	user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
