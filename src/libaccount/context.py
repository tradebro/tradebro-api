from dataclasses import dataclass
from os import environ

import motor.motor_asyncio
from beanie import init_beanie

from libaccount.models.mongo import User
from libshared.logging import logger


@dataclass
class Context:
    mongo_url: str
    mongo_client: motor.motor_asyncio.AsyncIOMotorClient

    env: str
    is_production: bool = False
    is_staging: bool = False
    is_dev: bool = True

    def __init__(self):
        self.mongo_url = environ.get('MONGO_URL')
        self.env = environ.get('ENV')

        self.is_production = self.env == 'prod'
        self.is_staging = self.env == 'staging'
        self.is_dev = self.env == 'dev'

    async def __aenter__(self):
        self.mongo_client = motor.motor_asyncio.AsyncIOMotorClient(self.mongo_url)
        await init_beanie(database=self.mongo_client.db_name, document_models=[User])

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type or exc_val or exc_tb:
            ''' Exception happened '''
            logger.error(msg=exc_tb)
            return

    @staticmethod
    async def tokenless():
        return Context()


context = Context()
