# FastAPI has many classes to handle data from the request
# Body, Query, Path, Cookie, Header, Form
# here go some examples

# -------------------File Example --------------------

# File works for small files, as all bytes will be stores in memory
# UploadFile can handler larger sizes: it has a file-like async interface,
# and exposes a SpooledTemporaryFile object to pass directly to other libraries
# you can also upload multiples files, metadata, etc

# This example also shows the use of Form data (if the request hast a 
# file, it cannot have a body, as the Headers would differ)

import os
from typing import Optional, Dict, Union

from fastapi import FastAPI, File, UploadFile, Form

app = FastAPI()

@app.post('/file/')
def receive_file(file: bytes = File(...), form_data: Optional[str] = Form(None)):
    
    dirs = ['/', 'home', 'lucas-mateo', 'Desktop']
    filename = ['new_file.jpeg']
    path = os.path.join(*dirs+filename)
    # this will copy the file to Desktop
    with open(path, 'wb') as new_file:
        # i think this is the wrong method
        new_file.write(file)
    
    result: Dict[str, Union[int, str]] = { 'file_size': len(file) }
    # in Postman, DO NOT put Headers (let Postman do it for you)
    if form_data:
        result.update({'form_data': form_data.capitalize()}) 
    
    return result