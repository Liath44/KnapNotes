from db_utils.queries import is_username_in_db
from pydantic import BaseModel

PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 50
USERNAME_MAX_LENGTH = 30

LOWER_CASE_KEY = "has_lower"
LOWER_CASE_BEGINNING = ord('a')
LOWER_CASE_ENDING = ord('z')

UPPER_CASE_KEY = "has_upper"
UPPER_CASE_BEGINNING = ord('A')
UPPER_CASE_ENDING = ord('Z')

DIGIT_KEY = "has_digit"
DIGIT_BEGINNING = ord('0')
DIGIT_ENDING = ord('9')

SPECIAL_KEY = "has_special"
PASSWORD_SPECIAL_SYMBOLS = "!@#$%^&*()_-+={[}]:;\"'|\\<,>.?/~`"

EMAIL_SPECIAL_SYMBOLS = "!#$%&'*+-/=?^_`{|}~."


class RegistrationForm(BaseModel):
	username: str  # must be email
	password: str


def validate_password(password):
	if not (PASSWORD_MIN_LENGTH <= len(password) <= PASSWORD_MAX_LENGTH):
		return False  # too short/long
	report = generate_empty_report()
	for c in password:
		is_valid_char = update_report(c, report)
		if not is_valid_char:
			return False  # invalid char
	for value in report.values():
		if value is False:
			return False  # too weak
	return True  # ok


def generate_empty_report():
	return {
		LOWER_CASE_KEY: False,
		UPPER_CASE_KEY: False,
		DIGIT_KEY: False,
		SPECIAL_KEY: False
	}


def update_report(c, report):
	c_code = ord(c)
	outcome = False
	if LOWER_CASE_BEGINNING <= c_code <= LOWER_CASE_ENDING:
		outcome = report[LOWER_CASE_KEY] = True
	elif UPPER_CASE_BEGINNING <= c_code <= UPPER_CASE_ENDING:
		outcome = report[UPPER_CASE_KEY] = True
	elif DIGIT_BEGINNING <= c_code <= DIGIT_ENDING:
		outcome = report[DIGIT_KEY] = True
	elif c in PASSWORD_SPECIAL_SYMBOLS:
		outcome = report[SPECIAL_KEY] = True
	return outcome


def validate_username(username):
	if len(username) > USERNAME_MAX_LENGTH:
		return False
	parts = username.split('@')
	if len(parts) != 2:
		return False  # no @ or more than one
	domain_parts = parts[1].split('.')
	if len(domain_parts) != 2:
		return False  # improper domain
	if len(domain_parts[0]) == 0 or len(domain_parts[1]) == 0:
		return False  # improper part of domain
	if not (validate_domain_name(domain_parts[0]) and validate_country_domain(domain_parts[1])):
		return False
	if len(parts[0]) == 0:
		return False  # too short user
	prev_was_dot = False
	for c in parts[0]:
		if not is_valid_email_character(c):
			return False  # invalid email char
		if c == '.':
			if prev_was_dot:
				return False  # two dots in a row
			prev_was_dot = True
		else:
			prev_was_dot = False
	return not is_username_in_db(username)


def validate_domain_name(domain_part):
	if domain_part[0] == '-' or domain_part[-1] == '-':
		return False
	for c in domain_part:
		c_code = ord(c)
		if not (LOWER_CASE_BEGINNING <= c_code <= LOWER_CASE_ENDING or c == '-'):
			return False
	return True


def validate_country_domain(domain_part):
	for c in domain_part:
		c_code = ord(c)
		if not LOWER_CASE_BEGINNING <= c_code <= LOWER_CASE_ENDING:
			return False
	return True


def is_valid_email_character(c):
	c_code = ord(c)
	if LOWER_CASE_BEGINNING <= c_code <= LOWER_CASE_ENDING:
		return True
	elif UPPER_CASE_BEGINNING <= c_code <= UPPER_CASE_ENDING:
		return True
	elif DIGIT_BEGINNING <= c_code <= DIGIT_ENDING:
		return True
	elif c in EMAIL_SPECIAL_SYMBOLS:
		return True
	return False
