from typing import Optional

from fastapi import FastAPI, Depends
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str


# function dependencies
async def common_deps1(q1: Optional[str], q2: int = 0):
    return {'q1': q1, 'q2': q2}

# class dependencies
class CommonDeps2:
    def __init__(self, path_var: str, item: Item):
        self.path_var = path_var
        self.item = item

# class dependencies using pydantic (easy to mix with other dependencies)
class CommonDeps3(BaseModel):
    path_var: str
    item: Item


@app.get('/dep1/')
async def example_dep1(dependencies: dict = Depends(common_deps1)):
    return dependencies


@app.post('/dep2/{path_var}')
async def example_dep2(dependencies: CommonDeps2 = Depends(CommonDeps2)):
    return dependencies

# you can omit the argument of Depends if it is the same
# as the declared type
@app.post('/dep3/{path_var}')
async def example_dep3(deps1: dict = Depends(common_deps1),
                       deps3: CommonDeps3 = Depends()):
    
    deps1.update(deps3.dict())
    return deps1

# dependencies can depend on other dependencies
# they are cached in that case (only called once),
# unless you need otherwise, using use_cache=False

# if you don't need to use the values of dependencies (for example, only for security)
# then you can declare them as a list in the path operation decorator
# For app-wise dependencies, you can declare them as parameters,
# when calling: FastAPI([dependencies])

# You can use yield instead of return for dependencies
# This is useful for executing code after the response has been sent 
# (e.g., closing database connections)

