import logging
from fastapi import FastAPI


logger = logging.getLogger(__name__)

app = FastAPI(
    version='1.0.0',
    title='Anonymous Chat API',
    contact={'name': 'Michael', 'email': 'mdev4work@gmail.com'}
)

