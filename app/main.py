from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import engine
from app.db.base import Base
from app.routers import auth, users, posts, steam_auth

app = FastAPI(title="API GameConnect", version="1.0")

# 🚀 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix="/api/auth", tags=["Autenticação"])
app.include_router(users.router, prefix="/api/usuarios", tags=["Usuários"])
app.include_router(posts.router, prefix="/api/posts", tags=["Postagens"])
app.include_router(steam_auth.router, prefix="/api/auth/steam", tags=["Autenticação (Steam)"])
