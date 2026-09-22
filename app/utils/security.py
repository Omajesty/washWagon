from datetime import datetime, timedelta, timezone
from app.utils.config import settings
import bcrypt
import jwt


def hash_password(password: str) -> str:

    password_bytes = password.encode("utf-8")
    
    hashed = bcrypt.hashpw(
        password_bytes, 
        bcrypt.gensalt()
        )
    
    return hashed.decode("utf-8")


def verify_password(
        password: str, 
        hashed_password: str
        ) -> bool:
    
    password_bytes = password.encode("utf-8")
    hashed_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(password_bytes, hashed_bytes)


def create_access_token(
        user_id: int,
        role: str,
        ) -> str:

    expire = datetime.now(timezone.utc) + timedelta(
        seconds=settings.ACCESS_TOKEN_EXPIRE_SECONDS
    )
    payload = {
        "sub": str(user_id),
        "role": str(role), 
        "exp": expire}
    
    return jwt.encode(
        payload, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM,
        )

