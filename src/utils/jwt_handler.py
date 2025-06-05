from datetime import (
    datetime,
    timedelta,
    timezone,
)
from typing import Optional
from uuid import UUID

import jwt

from configs import (
    ACCESS_TOKEN_EXPIRE_MINUTES_TOKEN,
    ALGORITHM_TOKEN,
    SECRET_KEY_TOKEN,
)


def create_access_token(user_id: UUID) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES_TOKEN))
    payload = {
        'sub': str(user_id),
        'exp': expire,
    }
    return jwt.encode(payload, SECRET_KEY_TOKEN, algorithm=ALGORITHM_TOKEN)


def decode_access_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(token, SECRET_KEY_TOKEN, algorithms=[ALGORITHM_TOKEN])
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None
    else:
        return payload.get('sub')
