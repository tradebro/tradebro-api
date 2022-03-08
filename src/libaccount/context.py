from __future__ import annotations

from dataclasses import dataclass
from os import environ

import motor.motor_asyncio
from beanie import init_beanie
from fastapi import Request

from libaccount.errors import UnauthorizedError
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
    is_testing: bool = False

    access_token: str | None = None
    current_user: User | None = None

    def __init__(self, access_token: str | None = None):
        self.mongo_url = environ.get('MONGO_URL')
        self.env = environ.get('ENV')

        self.is_production = self.env == 'prod'
        self.is_staging = self.env == 'staging'
        self.is_dev = self.env == 'dev'
        self.is_testing = environ.get('TESTING') == 'pytest'

        self.access_token = access_token

    async def __aenter__(self) -> Context:
        self.mongo_client = motor.motor_asyncio.AsyncIOMotorClient(self.mongo_url)
        db_name = f'tradebro-{self.env}'
        await init_beanie(database=self.mongo_client[db_name], document_models=[User])

        # Authorize
        if self.access_token:
            await self.authorize_access_token(access_token=self.access_token)

        return self

    async def authorize_access_token(self, access_token: str):
        user = await User.get_user_by_access_token(access_token=access_token)
        if not user:
            raise UnauthorizedError('Unrecognized access token')

        self.current_user = user

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type or exc_val or exc_tb:
            ''' Exception happened '''
            return

    @classmethod
    def tokenless(cls) -> Context:
        return cls()

    @classmethod
    def protected(cls, authorization: str) -> Context:
        if authorization is None:
            raise UnauthorizedError('Empty access token')

        auth = authorization.split('Bearer ')
        if len(auth) != 2:
            raise UnauthorizedError('Unrecognized access token')

        access_token = auth[1]

        instance = cls(access_token=access_token)
        return instance


context = Context()
