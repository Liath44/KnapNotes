from routers.authentication import router as authentication_router
from fastapi.middleware.cors import CORSMiddleware
from routers.notes import router as notes_router
from fastapi import FastAPI

origins = [
	"http://localhost:3000",
	"https://localhost:3000",
	"http://localhost",
	"https://localhost",
]

app = FastAPI()
app.include_router(authentication_router)
app.include_router(notes_router)
app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
	expose_headers=["*"]
)

"""
@app.middleware("http")
async def validate(request: Request, call_next):
	print("entry point")
	user_id = ""
	if not (request.url.path in AUTHORISATION_INDEPENDENT_REQUESTS.values()):
		print("why am i here")
		token = get_token(request.headers.raw)
		if token is None:
			return JSONResponse(STARLETTE_RESPONSE_VALIDATION_ERROR, status_code=422)
		user_id = get_user_id(token)
		if not user_id:
			return JSONResponse(STARLETTE_INVALID_TOKEN_ERROR, status_code=422)
	print("ok... where the problem at?")
	request.state.user_id = user_id
	response = await call_next(request)
	print(response)
	#return response
	return JSONResponse({"asd": "asd"}, headers={"Access-Control-Allow-Origin": "*"})


def get_token(headers_list):
	for key, value in headers_list:
		if key.decode() == TOKEN_KEY:
			return value.decode()
	return None
"""
