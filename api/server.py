import uvicorn
from fastapi import FastAPI
from routes.test import router as test_router

def start():
    api = _init_api()
    uvicorn.run(api, host="127.0.0.1", port=8000)

def _init_api():
    api = FastAPI(
        title="Vector Database API",
        description="API for managing document embeddings and vector search",
        version="1.0.0",
    )
    api.include_router(test_router)
    return api