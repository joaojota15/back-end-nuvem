from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import engine
from app.db.base import Base
from app.routers import auth, users, posts, steam_auth

app = FastAPI(title="API GameConnect", version="1.0")

<<<<<<< HEAD
# 🚀 CORS – localhost + Railway
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",                     # desenvolvimento
        "https://seu-projeto.up.railway.app",        # produção (troque quando tiver a URL real)
    ],
=======
# 🚀 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
>>>>>>> e5b4ec757330ba6b79850b145dd2efb94bc877a9
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

<<<<<<< HEAD
# Criar tabelas
Base.metadata.create_all(bind=engine)

# Rotas
=======
Base.metadata.create_all(bind=engine)

>>>>>>> e5b4ec757330ba6b79850b145dd2efb94bc877a9
app.include_router(auth.router, prefix="/api/auth", tags=["Autenticação"])
app.include_router(users.router, prefix="/api/usuarios", tags=["Usuários"])
app.include_router(posts.router, prefix="/api/posts", tags=["Postagens"])
app.include_router(steam_auth.router, prefix="/api/auth/steam", tags=["Autenticação (Steam)"])
