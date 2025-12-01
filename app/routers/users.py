from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session 
from app.utils import decode_token
from app.db.session import SessionLocal
from app.models import User
from app.schemas import UserProfile, UserUpdate

router = APIRouter()
security = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = decode_token(token)
    sub = payload.get('sub')
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == sub).first()
        if not user:
            raise Exception('Usuário não encontrado')
        return user
    finally:
        db.close()

@router.get('/me', response_model=UserProfile)
def user_return(current_user: User = Depends(get_current_user)):
    return UserProfile(username=current_user.name, email=current_user.email, steam_id=current_user.steam_id)

@router.patch('/me/update-nickname', response_model=UserProfile)
def update_nickname(
    user_in: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Atualiza o 'name' (nickname) do usuário autenticado.
    """
    current_user.name = user_in.name
    
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    
    return UserProfile(
        username=current_user.name, 
        email=current_user.email, 
        steam_id=current_user.steam_id
    )