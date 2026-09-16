from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends
from backend.app.auth import (
    authenticate_user,
    create_access_token,
    create_user,
    verify_credentials,
)
from pymongo.errors import DuplicateKeyError

from backend.app.agent.agent import run_agent

from backend.app.routes.employees import (
    router as employees_router,
)

from backend.app.routes.tickets import (
    router as tickets_router,
)

from backend.app.routes.policies import (
    router as policies_router,
)

from backend.app.routes.documents import (
    router as documents_router,
)

from backend.app.routes.document_chunks import (
    router as document_chunks_router,
)


app = FastAPI(
    title="Company AI Assistant API",
    description="Internal AI assistant backend for the fictional company.",
    version="0.1.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(employees_router)
app.include_router(tickets_router)
app.include_router(policies_router)
app.include_router(documents_router)
app.include_router(document_chunks_router)


class ChatRequest(BaseModel):
    message: str
    session_id: str


class ChatResponse(BaseModel):
    response: str


class AuthRequest(BaseModel):
    username: str
    password: str


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str


@app.post("/auth/signup", response_model=AuthResponse, status_code=201)
async def signup(request: AuthRequest):
    username = request.username.strip().lower()

    if len(username) < 3 or len(username) > 40:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username must be between 3 and 40 characters.",
        )

    if len(request.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must contain at least 8 characters.",
        )

    try:
        create_user(username, request.password)
    except DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="That username is already registered.",
        )

    return AuthResponse(
        access_token=create_access_token(username),
        username=username,
    )


@app.post("/auth/login", response_model=AuthResponse)
async def login(request: AuthRequest):
    username = request.username.strip().lower()

    if not authenticate_user(username, request.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password.",
        )

    return AuthResponse(
        access_token=create_access_token(username),
        username=username,
    )


@app.get("/")
async def root():
    return {
        "message": "Company AI Assistant API is running"
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy"
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    username: str = Depends(verify_credentials),
):
    result = run_agent(
        user_message=request.message,
        session_id=request.session_id,
        username=username,
    )

    return {
        "response": result["final_answer"],
    }