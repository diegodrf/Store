import os
from sqlmodel import create_engine
import sys

DATABASE_URL = os.environ.get('DATABASE_URL')
ECHO_MODE = os.environ.get('ECHO_MODE')
DEVELOPMENT_MODE = os.environ.get('DEVELOPMENT_MODE', None)

echo = True
connect_args = {}

if not ECHO_MODE:
    connect_args['sslmode'] = 'require'
    echo = False

if not DEVELOPMENT_MODE:
    """
        This is necessary because the default connection string from Heroku is not recognized by 
        SQLAlchemy create_engine()  
    """
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql+psycopg2://')

engine = create_engine(
    url=DATABASE_URL,
    echo=echo,
    connect_args=connect_args
)

