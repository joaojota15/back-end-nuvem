from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models import User
from app.schemas import UserCreate, UserOut, LoginIn, Token
from app.utils import hash_password, verify_password, create_access_token
from app.services.password_reset import send_reset_email_to_user, reset_password as service_reset
from pydantic import BaseModel, EmailStr

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/register', response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail='Email já cadastrado')
    name = getattr(user_in, 'name', None) or getattr(user_in, 'username', None) or user_in.email.split('@')[0]
    user = User(name=name, email=user_in.email, password_hash=hash_password(user_in.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserOut(id=str(user.id), username=user.name, email=user.email)

@router.post('/login', response_model=Token)
def login(data: LoginIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Credenciais inválidas')
    token = create_access_token(subject=str(user.id))
    return Token(access_token=token)

class ForgotPasswordRequest(BaseModel):
    email: EmailStr
    frontend_url: str | None = None

@router.post('/forgot-password')
async def forgot_password(req: ForgotPasswordRequest):
    ok = await send_reset_email_to_user(req.email, frontend_url=req.frontend_url)
    if not ok:
        raise HTTPException(status_code=404, detail='Usuário não encontrado')
    return {'message': 'E-mail de redefinição enviado com sucesso.'}

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

@router.post('/reset-password')
def reset_password(req: ResetPasswordRequest):
    ok = service_reset(req.token, req.new_password)
    if not ok:
        raise HTTPException(status_code=400, detail='Token inválido ou expirado.')
    return {'message': 'Senha redefinida com sucesso.'}
