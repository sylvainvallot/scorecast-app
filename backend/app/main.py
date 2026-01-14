from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.main import api_router

app = FastAPI(
    title=settings.TITLE,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    openapi_url=f"{settings.API_STR}/openapi.json",
    docs_url=f"{settings.API_STR}/docs",
)

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.include_router(api_router, prefix=settings.API_STR)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # dev only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
