from fastapi import FastAPI

app = FastAPI()


# @app.get('/persons/{name}')
# async def vecna_says_hi(name):
#     return {'Vecna says, Hi {}'.format(name)}
#
#
# @app.get('/persons/{name}')
# async def vecna_says_hi(name: str):
#     return {'Vecna says, Hi {}'.format(name)}


@app.get('/eggos/')
async def el_eats_eggos(num: int = 1, max_num: int = 10):
    return {'El likes {} eggos, but feed her {} max!'.format(num, max_num)}


from typing import Union


@app.get('/persons/{name}/eggos/')
async def strange_character_eats_eggos(
    name: str, num: int = 1, strange_character: Union[bool, None] = None
):
    msg = '{} likes {} eggos!'.format(name, num)
    res = {'message': msg}
    if strange_character:
        res.update({'is_strange_character': strange_character})
    return res


# # Data Validation

from enum import Enum


class StrangeCharacter(str, Enum):
    mike = 'mike'
    el = 'el'
    dustin = 'dustin'
    will = 'will'
    lucas = 'lucas'


# @app.get('/persons/{name}')
# async def vecna_says_hi(name: StrangeCharacter):
#     print(name, name in (StrangeCharacter.mike, StrangeCharacter.lucas, StrangeCharacter.dustin))
#     if name in (StrangeCharacter.mike, StrangeCharacter.lucas, StrangeCharacter.dustin):
#         return 'Vecna says, Hi {}'.format(name.capitalize())
#     else:
#         return 'Vecna says, Bye {}'.format(name.capitalize())


# pydantic class

from pydantic import BaseModel
from typing import List


class EggoEater(BaseModel):
    name: str
    hobbies: Union[List[str], None] = None
    num_eggos: int


eggo_eaters = {'mike': {'name': 'Mike', 'num_eggos': 1, 'hobbies': ['D&D', 'writing to El']},
               'el': {'name': 'Jane', 'num_eggos': 2, 'hobbies': ['controlling things with mind', 'writing to Mike']},
               'will': {'name': 'Will', 'num_eggos': 0},
               'dustin': {'name': 'Dustin', 'num_eggos': 1, 'hobbies': ['D&D', 'hacking into school computer systems']},
               'lucas': {'name': 'Lucas', 'num_eggos': 2}}


# @app.get('/persons/{name}', response_model=EggoEater)
# async def strange_character_eats_eggos(name: str):
#     return eggo_eaters[name]


# @app.get('/persons/{name}', response_model=EggoEater, response_model_exclude={'hobbies'})
# async def strange_character_eats_eggos(name: str):
#     return eggo_eaters[name]
#
#
# @app.get('/persons/{name}', response_model=EggoEater, response_model_include={'num_eggos'})
# async def strange_character_eats_eggos(name: str):
#     return eggo_eaters[name]

#
# logging

from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler
from fastapi.logger import logger as fastapi_logger
from fastapi import Request


formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(message)s', '%Y-%m-%d %H:%M:%S')
logging.getLogger().setLevel(logging.INFO)
handler = RotatingFileHandler('fastapi_access.log', backupCount=0)
fastapi_logger.addHandler(handler)
handler.setFormatter(formatter)
fastapi_logger.info('****************** Starting Server *****************')


@app.middleware('http')
async def log_middle(request: Request, call_next):
    response = await call_next(request)
    fastapi_logger.info(
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {request.method} {request.url} STATUS: {response.status_code}")
    return response


# # exception handling
from fastapi import HTTPException


@app.get('/persons/{name}', response_model=EggoEater)
async def strange_character_eats_eggos(name: str):
    if name not in eggo_eaters:
        raise HTTPException(status_code=404, detail="Strange Character not found!")
    return eggo_eaters[name]







