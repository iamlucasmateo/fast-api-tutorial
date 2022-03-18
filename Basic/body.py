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


# additional validations

