from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from router import router
import uvicorn

openapi_url = '/api/openapi.json'
redoc_url = '/api/redoc'

app = FastAPI(
    title='Youtube data API',
    openapi_url=openapi_url,
    redoc_url=redoc_url,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(
    router,
    prefix='/api',
    tags=['search'],
)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
