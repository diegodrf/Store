import os
from sqlmodel import create_engine
import sys

DATABASE_URL = os.environ.get('DATABASE_URL')
sys.stdout.write(f'>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> {DATABASE_URL}')
ECHO_MODE = os.environ.get('ECHO_MODE')
DEVELOPMENT_MODE = os.environ.get('DEVELOPMENT_MODE', None)

echo = True
connect_args = {}

if not ECHO_MODE:
    connect_args['sslmode'] = 'require'
    echo = False


engine = create_engine(
    url=DATABASE_URL,
    echo=echo,
    connect_args=connect_args
)

