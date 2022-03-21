from fastapi import FastAPI

app = FastAPI()

# simplest example
@app.get('/')
async def greet():
    return {"message": "Hello World"}

# parameters (in URL + function)
@app.get('/param_str/{param}')
async def use_id(param: str):
    return {"message": f"Extracting params: {param}"}

# this will return an error is the param is not an int
# FastAPI does this automatically with the type declaration
@app.get('/param_int/{param}')
async def param_int(param: int):
    return {"message": f"Adding 2 to your input: {param + 2}"}

# static URLs should go before dynamic if the have the same path
# FastAPI evaluates path operations in order, so if they are not 
# ordered as specified, the static URL will be considered dynamic and
# pass the wrong parameter
@app.get('/users/me')
async def get_me():
    return {"message": "using id from token/cookie, etc"}

@app.get('/users/{user_id}')
async def get_user_id(user_id: str):
    return {"message": f"using id from URL: {user_id}"}

# validating parameters with Enum
from enum import Enum

class CropType(str, Enum):
    wheat = "wheat"
    corn = "corn"
    soy = "soy"

# if I pass a crop name not enumerated, it will raise a ValidationError
@app.get('/crops/{crop_name}')
async def get_crops(crop_name: CropType):
    return {"message": f"Selected crop: {getattr(CropType, crop_name)}"}

# when the parameter is a path, declare it as such
@app.get('/file/{file_path:path}')
async def get_path(file_path):
    return {"message": f"Returning {file_path}"}


# query parameters: declared in the inner function
# but not in the path
# type validations and defaults come in handy as well
@app.get('/query/{example}')
async def query(example: str, x: int = 0, y: int = 0):
    return {
        "example": example,
        "sum": x + y
    }

# you can include booleans (in URL they can be "True", "yes", "on")
# if parameter is not optional and no default declared, then FastAPI will
# enforce it for requests
# You may also use Enum in this case

# uvicorn.run(app, port=8000)
# from command line: uvicorn first:app --reload