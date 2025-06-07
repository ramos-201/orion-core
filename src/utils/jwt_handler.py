from datetime import (
    datetime,
    timedelta,
    timezone,
)
from typing import Optional
from uuid import UUID

import jwt

from configs import (
    ALGORITHM_JWT,
    MINUTES_EXPIRATION_JWT,
    PRIVATE_KEY_JWT,
)


def create_access_token(user_id: UUID) -> str:
    now = datetime.now(timezone.utc)
    expiration = now + timedelta(minutes=int(MINUTES_EXPIRATION_JWT))

    payload = {
        'sub': str(user_id),
        'exp': expiration,
    }

    return jwt.encode(payload, PRIVATE_KEY_JWT, algorithm=ALGORITHM_JWT)


def decode_access_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(token, PRIVATE_KEY_JWT, algorithms=[ALGORITHM_JWT])
        return payload.get('sub')
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None
