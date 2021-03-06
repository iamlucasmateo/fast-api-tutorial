from decimal import Decimal
from enum import Enum
from re import M
from typing import Optional, List, Dict

from fastapi import FastAPI
from pydantic import BaseModel

# ----------------Request Bodies----------------

app = FastAPI()


class Country(Enum):
    Argentina = "Argentina"
    Australia = "Australia"
    Ukraine = "Ukraine"

# this will use Pydantic and validate data accordingly
class Crop(BaseModel):
    seed_size: Decimal
    origin: Country
    description: Optional[str] = None

@app.post('/crops/')
def create_item(crop: Crop):
    crop_dict = crop.dict()
    crop_dict.update({'origin_country': crop.origin})
    crop_dict.pop('origin')
    return crop_dict


# using path and query params as well
# FastAPI will check: 
# 1. If parameter is declared in URL, then function arg is taken from here 
# 2. If type hint is singular (int, str, float, bool), it is a query param
# 3. If type hint is a Pydantic model, it will be interpreted as a request body 
@app.post('/crops/{path_var}/')
def create_item2(path_var: str, crop: Crop, query: Optional[str] = None):
    crop_dict = crop.dict()
    crop_dict.update({'path_var': path_var, 'query': query})
    return crop_dict


# ------- Query parameters validations------------
# ------------------------------------------------
from fastapi import Query

# this type can have other type of validations, e.g. regex
crop_indicator = Query("default_value", max_length=20, min_length=2)

# for the query to be required (with no default):
# Query(..., [kw parameters])
# this uses Ellipsis (from Python)

# this endpoint will return an Error if the Query type
# specification is not fulfilled
@app.get('/crops_q/')
async def query_validation(indicator: Optional[str] = crop_indicator):
    if indicator:
        # some logic here
        pass
    return {
        "indicator": indicator
    }

# You can also generate metadata, alias, deprecated indicator, etc, for the docs


# ------------- Path parameters validation and metadata ---------------
# ---------------------------------------------------------------------

from fastapi import Path

# using title (metadata) and number validations here
path_type = Path(..., title="The item id", lt=100, gt=50)

@app.get('/path_example/{item_id}/', )
async def path_example(item_id: int = path_type):
    return {
        "data": item_id
    }

# ------------- Functionalities -------------------

# You can have multiple body parameters: that is, 
# multiple Pydantic models mapping to multiple keys in request body (JSON)

class FieldSize(Enum):
    big = "big"
    medium = "medium"
    small = "small"


class Field(BaseModel):
    main_crop: str
    size: FieldSize
    owner: Optional[str]


@app.post('/double_body/{some_data}')
def double_body(*, some_data: str, 
                q1: int,
                q2: Optional[str] = None, 
                field: Field,
                crop: Crop):
    result = {
        'from_URL': some_data,
        'from_query': q1,
        'field (from_body)': field,
        'crop (also from_body)': crop
    }
    if q2:
        result.update({'other_query': q2})
    return result

    # there is another class in FastAPI, Body. You use it when you will not
    # use a Base Model, like this: def function([...], data: int = Body(...[,validations, metadata]))
    # this will be expected in the request body
    # also, to add a key in the body with the model name:
    # { "item" : { "id": 23542435, "description": "something"  } }
    # you would do def func([...], item: Item = Body(..., embed=True))

    # You can use pydantic's Field class to add validation and metadata
    # to a BaseModel attributes

    # You can use nested models (i.e., a Field of one Model is another Field)