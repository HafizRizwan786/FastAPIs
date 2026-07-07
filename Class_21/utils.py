import jwt
from config import secruity_Settings
from datetime import datetime,timedelta, timezone
from uuid import uuid4
from pathlib import Path
from itsdangerous import URLSafeTimedSerializer

_serializer=URLSafeTimedSerializer(secruity_Settings.JWT_SECRET)


APP_DIR=Path(__file__).resolve().parent
TEMPLATE_DIR=APP_DIR/"templates"




def generate_access_token(data: dict,expiry: timedelta=timedelta(minutes=1))->str:
    return jwt.encode(
            payload={
                **data,
                "jti":str(uuid4()),
                "exp": datetime.now(timezone.utc) + expiry
            },
            algorithm = secruity_Settings.JWT_ALGORITHM,
            key=secruity_Settings.JWT_SECRET
        )

def decode_access_token(token: str)->dict | None:
    # Clean the token if the client accidentally appended ", Bearer" or spaces
    print(f"DEBUG: Received token from Depends: {token!r}")
    clean_token = token.split(',')[0].strip()
    print(f"DEBUG: Clean token: {clean_token!r}")
    try:
        return jwt.decode(
            jwt=clean_token,
            key=secruity_Settings.JWT_SECRET,
            algorithms=[secruity_Settings.JWT_ALGORITHM]
        )
    except jwt.PyJWTError as e:
        print(f"JWT Decode Error: {e}")
        return None



def generate_url_safe_token(data: dict,salt: str|None = None)->str:
    return _serializer.dumps(data,salt=salt)


def decode_url_safe_token(token: str,salt: str | None = None, expiry: timedelta | None = None)->dict | None:
    try:
        return _serializer.loads(
            token,
            salt=salt,
            max_age=expiry.total_seconds() if expiry else None
        )
    except (BadSignature, SignatureExpired):
        return None
