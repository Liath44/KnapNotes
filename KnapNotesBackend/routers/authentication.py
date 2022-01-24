from routers.models.registration_form import RegistrationForm
from routers.models.registration_form import validate_password, validate_username
from api_utils.response_bodies import DEFAULT_201_OK, INVALID_REGISTRATION_PASSWORD, INVALID_REGISTRATION_USERNAME, \
	COULD_NOT_CREATE_USER, INVALID_LOGIN_DATA, TOKEN_GENERATION_ERROR, TOKEN_KEY
from fastapi import APIRouter, status, Response
from utils.security_utils import get_hash, create_salt, hash_and_validate_password
from db_utils.queries import create_user, is_username_in_db, get_authentication_data, insert_token_to_db
from utils.cookie_id_factory import generate_token

MODULE_TAG = "authentication"
AUTHORISATION_INDEPENDENT_REQUESTS = {
	"register_path": "/register",
	"login_path": "/login"
}

router = APIRouter()


@router.post(AUTHORISATION_INDEPENDENT_REQUESTS["register_path"], tags=[MODULE_TAG], status_code=status.HTTP_201_CREATED)
async def register_user(registration_form: RegistrationForm, response: Response):
	username, password = extract_registration_data(registration_form)
	print("enter")
	if not validate_password(password):
		response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
		return INVALID_REGISTRATION_PASSWORD
	if not validate_username(username):
		response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
		return INVALID_REGISTRATION_USERNAME
	salt = create_salt()
	if not create_user(username, get_hash(password, salt), salt):
		response.status_code = status.HTTP_502_BAD_GATEWAY
		return COULD_NOT_CREATE_USER
	return DEFAULT_201_OK


def extract_registration_data(registration_form):
	return registration_form.username.strip(), registration_form.password.strip()


# What if token is already present
# TOODO: utilise max 5 attempts mechanism
@router.post(AUTHORISATION_INDEPENDENT_REQUESTS["login_path"], tags=[MODULE_TAG], status_code=status.HTTP_201_CREATED)
async def login(registration_form: RegistrationForm, response: Response):
	username, password = extract_registration_data(registration_form)
	if not is_username_in_db(username):
		response.status_code = status.HTTP_404_NOT_FOUND
		return INVALID_LOGIN_DATA
	user_id, real_password, salt = get_authentication_data(username)
	if not hash_and_validate_password(real_password, password, salt):
		response.status_code = status.HTTP_401_UNAUTHORIZED
		return INVALID_LOGIN_DATA
	token = generate_token()
	if not insert_token_to_db(token, user_id):
		response.status_code = status.HTTP_502_BAD_GATEWAY
		return TOKEN_GENERATION_ERROR
	response.headers[TOKEN_KEY] = token
	return {"username": username, "id": user_id}
