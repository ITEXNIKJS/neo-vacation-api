import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.router import router

app = FastAPI(title='EAS API',
              docs_url='/docs',
              redoc_url='/redoc')
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
    allow_credentials=True,
)

app.include_router(router.router)

if __name__ == '__main__':
    uvicorn.run(app=app, host='127.0.0.1', port=8000)
