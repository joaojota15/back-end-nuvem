try:
    from .password_handler import hash_password, verify_password  
except Exception:
    hash_password = None
    verify_password = None

try:
    from .jwt_handler import create_access_token, decode_token, get_current_user  
except Exception:
    create_access_token = None
    decode_token = None
    get_current_user = None

__all__ = [
    "hash_password",
    "verify_password",
    "create_access_token",
    "decode_token",
    "get_current_user",
]