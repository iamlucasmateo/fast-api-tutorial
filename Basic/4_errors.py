from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get('/error/{raise_error}')
def get_error(raise_error: bool):
    if raise_error:
        raise HTTPException(
            status_code=400,
            detail="An error was raised",
            # this can be done, it's rather rare
            headers={"X-Error": "There goes my error"}
        )
    return {"message": "No error was raised"}


# You can also make custom exceptions extending exception
# and using the decorator app.expection_handler(CustomException)
# You can overriede the default ValidationException