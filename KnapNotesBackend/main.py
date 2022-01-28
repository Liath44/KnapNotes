from routers.authentication import router as authentication_router
from fastapi.middleware.cors import CORSMiddleware
from routers.notes import router as notes_router
from routers.public import router as public_notes_router
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
app.include_router(public_notes_router)
app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
	expose_headers=["*"]
)
