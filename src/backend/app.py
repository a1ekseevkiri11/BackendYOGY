from fastapi import FastAPI
from .settings import settings
from .api import router as api_v1
from fastapi.middleware.cors import CORSMiddleware

# docs_url=None, redoc_url=None | Settings for deployment on prod
app = FastAPI(title="BackendYOGU", debug=settings.debug)
app.include_router(api_v1)


app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
