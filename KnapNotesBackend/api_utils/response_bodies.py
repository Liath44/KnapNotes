def create_message(message):
	return {"message": message}


TOKEN_KEY = "token"

DEFAULT_201_OK = create_message("OK")

INVALID_REGISTRATION_PASSWORD = create_message("Invalid password. Must be in range 8 to 50 and contain at least one of each: letter (both upper and lower), digit, special sign")
INVALID_REGISTRATION_USERNAME = create_message("Invalid username. Must be no longer than 30 characters and contain at least one of each: letter (both upper and lower), digit, special sign")
COULD_NOT_CREATE_USER = create_message("Could not create user due to database connection error")

INVALID_LOGIN_DATA = create_message("Invalid login data")
TOKEN_GENERATION_ERROR = create_message("Could not log in due to database connection error")

LOGIN_OK = create_message("OK - login")

INVALID_NOTE_PASSWORD = create_message("Invalid note password. Must be in range 8 to 50 and contain at least one of each: letter (both upper and lower), digit, special sign")
COULD_NOT_CREATE_NOTE = create_message("Could not generate user due to database connection error")

STARLETTE_RESPONSE_VALIDATION_ERROR = create_message("Requested restricted method without providing a token")
STARLETTE_INVALID_TOKEN_ERROR = create_message("Provided authentication token is either expired or invalid")

COULD_NOT_SAVE_NOTE = create_message("Could not save note due to database connection error")
COULD_NOT_ACCESS_NOTE = create_message("Could not get requested note")

TOKEN_VALIDATION_ERROR = create_message("Token validation error")
