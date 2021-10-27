from fastapi import FastAPI
from . import helpers

app = FastAPI()


@app.on_event('startup')
def on_startup():
    helpers.create_tables_if_not_exists()


@app.get('/')
def index():
    return {'message': 'Hello world!!'}
