from fastapi import FastAPI
from .routers import brand
from . import helpers

app = FastAPI(
    docs_url='/'
)


@app.on_event('startup')
def on_startup():
    helpers.create_tables_if_not_exists()


app.include_router(router=brand.router, prefix='/brands')

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('app.main:app', reload=True)
