from fastapi import FastAPI
from .routers import brand, product
from .repository.database import DEVELOPMENT_MODE
from . import helpers

app = FastAPI(
    docs_url='/'
)


@app.on_event('startup')
def on_startup():
    helpers.create_tables_if_not_exists()
    if DEVELOPMENT_MODE:
        if not helpers.is_pre_populated():
            helpers.pre_populate_database()


@app.on_event('shutdown')
def on_shutdown():
    if DEVELOPMENT_MODE:
        helpers.drop_tables()


app.include_router(router=brand.router, prefix='/brands')
app.include_router(router=product.router, prefix='/products')

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('app.main:app', reload=True)
