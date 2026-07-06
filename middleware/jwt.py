from jose import jwt, JWTError
from datetime import datetime, timedelta


SECRET_KEY = "SECRETKEY"

ALGORITHM = "HS256"


ACCESS_TOKEN_EXPIRE_MINUTES = 60



def create_token(data: dict):

    token_data = data.copy()


    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )


    token_data.update({

        "exp": expire

    })


    token = jwt.encode(

        token_data,

        SECRET_KEY,

        algorithm=ALGORITHM

    )


    return token




def verify_token(token: str):

    try:

        payload = jwt.decode(

            token,

            SECRET_KEY,

            algorithms=[ALGORITHM]

        )


        return payload


    except JWTError:

        return None