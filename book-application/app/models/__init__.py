from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine
from app.config import MONGO_DB_URL, MONGO_DB_NAME


class MongoDB:
    def __init__(self):
        self.client = None
        self.engine = None

    def connect(self):
        self.client = AsyncIOMotorClient(MONGO_DB_URL)
        self.engine = AIOEngine(self.client, MONGO_DB_NAME)
        print("db connected")

    def disconnect(self):
        self.client.close()


mongodb = MongoDB()
