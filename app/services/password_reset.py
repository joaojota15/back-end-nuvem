from app.db.session import SessionLocal
from app.models import User
from app.utils import create_access_token, decode_token, hash_password
from app.services.sendgrid_service import send_reset_email
from app.core.config import settings

RESET_MINUTES = 15

async def send_reset_email_to_user(email: str, frontend_url: str | None = None):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return False
        token = create_access_token(subject=str(user.email), expires_minutes=RESET_MINUTES)
        link = f"{frontend_url or settings.FRONTEND_URL or 'https://seusite.com'}/reset-password?token={token}"
        html = f"<p>Olá {user.name},</p><p>Clique no link para redefinir sua senha:</p><p><a href='{link}'>Redefinir senha</a></p>"
        status = send_reset_email(email, 'Redefinição de senha', html)
        return 200 <= status < 300
    finally:
        db.close()

def reset_password(token: str, new_password: str):
    db = SessionLocal()
    try:
        payload = decode_token(token)
        email = payload.get('sub')
        if not email:
            return False
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return False
        user.password_hash = hash_password(new_password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return True
    except Exception:
        return False
    finally:
        db.close()
