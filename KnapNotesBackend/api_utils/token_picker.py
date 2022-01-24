from db_utils.queries import get_user_id


def get_user_id_from_token(token):
	if token is None:
		return False
	token = token[0]
	user_id = get_user_id(token)
	if not user_id:
		return False
	return user_id
