from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import videos
from db import create_all_table



app = FastAPI(lifespan=create_all_table)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(videos.router)

@app.get("/")
def root():
    return{"hello world"}
