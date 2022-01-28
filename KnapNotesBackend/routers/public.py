from fastapi import APIRouter, status
from db_utils.queries import query_for_public_notes

MODULE_TAG = "public"

router = APIRouter()


@router.get("/get-public", tags=[MODULE_TAG], status_code=status.HTTP_200_OK)
def get_public_notes():
	return query_for_public_notes()
