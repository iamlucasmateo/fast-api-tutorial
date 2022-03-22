# - Declare request example data (with pydantic, using Config and schema_extra)
# 
# - Body, Path, Query, Cookie, Header, Form, etc, can also have examples (as args); 
# they are similar, and inherit from Param. Header admits multiple values from request
# 
# - Other data types: datetime (.datetime, .date, .time; converted to ISO time str), 
# uuid (id, to str)
# 
# - Response model (declared on path operation decorator): it will filter, validate and 
# format the data before returning a response. 
# You can exclude_unset to filter nulls (good for many-columns models). 
# You can have multiple models (e.g., user; use inheritance to keep it DRY). 
# You can also use Union, List (of models), or any arbitrary dict
# 
# - Status codes: declared on decorator, on raise HttpError
# 
# - Forms have their own headers and are handled with Form by FastAPI
# 
# - Parameters for decorator (path operation): status_code, tags, summary, 
# response_description, description (can come from the docstrings), deprecated flag
# 
# - jsonable_encoder from fastapi.encoders returns a “json version” of the object, 
# for example to pass to a NoSQL database (useful, e.g., for datetime objects). 
# This is used internally by FastAPI, but can be used for other purposes. 