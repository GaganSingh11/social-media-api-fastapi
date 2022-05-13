from jose import JWSError, jwt
from datetime import datetime, timedelta

# SECREAT_KEY
# Algoritham
# Expiration date or time

SECRET_KEY = "JHKGEHVKHKGTFHKWR4656B343KFNFRKLVBNLKVNLBEJBNKLBJ33453567676EGVBVLEBNE"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt