from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

app = FastAPI()
oauth2 = OAuth2PasswordBearer(tokenUrl='token')


class User(BaseModel):
    email: str
    full_name: str
    username: str

class UserInDB(User):
    hashed_password: str


def fake_hash_password(password: str):
    return f'fake_hash_{password}'

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": 'fake_hash_secret',
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": 'fake_hash_pass123',
        "disabled": True,
    },
}


def fake_decode_token(token: str):
    return get_user(fake_users_db, token)

async def get_user(db, username: str):
    if username in db:
        user_dict = db['username']
        return UserInDB(**user_dict)


async def get_current_user(token: str = Depends(oauth2)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid authentication credentials',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    return user





# FastAPI will know to pass the token from the header
# to the get_current_user function
@app.get('/users/me')
async def authenticated(current_user: User = Depends(get_current_user)):
    print(current_user)
    # return {'user': current_user}

@app.get('/users/me')
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@app.post('/token/')
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Incorrect username or password'
        )
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Incorrect username or password'
        )
    
    return { 'access-token': user.username, 'token_type': 'bearer' } 




# @app.get('/user/me')
# async def read_items(current_user: User = Depends(get_current_user)):
#     return current_user
