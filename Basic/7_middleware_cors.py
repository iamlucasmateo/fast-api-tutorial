import time

from fastapi import FastAPI, Request

app = FastAPI()

# This middleware takes the request (which it can process before sending to the endpoint),
# awaits the response using call_next, processes the response and finally returns the 
# processed response

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers['X-Process-Time'] = str(process_time)
    return response


@app.get('/greet/{name}/')
async def greeting(name: str, query1: int):
    time.sleep(query1)
    return { "hello": f"{name}", "query1": query1 }