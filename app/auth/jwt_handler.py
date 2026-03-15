import jwt
from datetime import datetime, timedelta
from app.config import JWT_SECRET

ALGORITHM = "HS256"
TOKEN_EXPIRY_HOURS = 24*7 # 1 week


def create_token(user_id: str):
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=TOKEN_EXPIRY_HOURS)
    }

    return jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHM)


def decode_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None