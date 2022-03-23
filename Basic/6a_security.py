# Used libraries:
# - python-jose (for JWT, other option us PyJWT)
# - depends on pyca/criptography
# - passlib (password hashing)

from datetime import datetime, timedelta
from re import L
from typing import Optional

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

app = FastAPI()

SECRET_KEY = '0f8a4aa2ac283412eb83b07cbe61e9113449246514db5a364556f8f1daca8b7b'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

fake_users_db = {
    'johndoe': {
        'username': 'johndoe',
        'full_name': 'John Doe',
        'email': 'john@doe.com',
        # this was hashed with pwd.hash('secret')
        'hashed_pass': '$2b$12$EOyGp7/Qp75NMuWoAmANFOfyinPZ2IQ3RwKgBoo6GvaIR.hjqOTg6'
    }
}


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None


class UserInDB(User):
    hashed_pass: str


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


async def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


async def get_password_hash(password: str):
    return pwd_context.hash(password)


async def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

async def authenticate_user(fake_db, username: str, password: str):
    user = await get_user(fake_db, username)
    if not user:
        return False
    if not await verify_password(password, user.hashed_pass):
        return False
    return user

async def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

@app.post('/token/', response_model=Token)
async def get_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(
        data={'sub': user.username}, expires_delta=access_token_expires
    )
    return {'access_token': access_token, 'token_type': 'Bearer'}

@app.get('/users/me', response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@app.get('/items')
async def read_own_items(current_user: User = Depends(get_current_user)):
    return [{'item_id': 'Foo', 'owner': current_user.username}]
