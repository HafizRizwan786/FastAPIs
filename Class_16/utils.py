import jwt
from config import secruity_Settings
from datetime import datetime,timedelta, timezone
from uuid import uuid4

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