from decimal import Decimal
from enum import Enum
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

