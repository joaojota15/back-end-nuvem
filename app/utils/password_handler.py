from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    bcrypt__ident="2b",  
    deprecated="auto",
)

def _truncate_password(password: str, max_bytes: int = 72) -> str:
    """Trunca a senha"""
    if not isinstance(password, str):
        password = str(password)

    b = password.encode("utf-8")
    if len(b) > max_bytes:
        b = b[:max_bytes]
    return b.decode("utf-8", errors="ignore")

def hash_password(password: str) -> str:
    """Cria hash da senha com bcrypt"""
    safe_password = _truncate_password(password)
    return pwd_context.hash(safe_password)

def verify_password(password: str, hashed: str) -> bool:
    """Verifica senha"""
    safe_password = _truncate_password(password)
    return pwd_context.verify(safe_password, hashed)
