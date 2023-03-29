from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import auth, appmain
from utils.db_utils import get_db
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="KKWST Backend App",
              description="",
              version="0.0.1")

app.mount("/static", StaticFiles(directory="resources/static"), name="static")

# set CORS
origins = [
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get database session
db = get_db()

# Set routers
app.include_router(auth.router)
app.include_router(appmain.router)


@app.get("/")
async def home():
    return RedirectResponse("http://127.0.0.1:8000/docs")

