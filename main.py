import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from api.tours import get_tours
from api.router import router


app = FastAPI(title='TOUR API',
              docs_url='/docs',
              redoc_url='/redoc')
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
    allow_credentials=True,
)
# обавить при запуске приложеньки загружаем в оперативу справочник
app.include_router(router)

if __name__ == '__main__':
    uvicorn.run(app=app, host='127.0.0.1', port=8000)
