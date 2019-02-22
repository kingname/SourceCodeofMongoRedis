import pymongo
import config
from bson import ObjectId
from pymongo.collection import Collection
from pymongo.cursor import Cursor
from pymongo.command_cursor import CommandCursor
from typing import Dict


class MongoUtil(object):
    def __init__(self):
        self.db = pymongo.MongoClient(config.MONGODB_URI)[config.QA_SYSTEM_DB]
        self.handler_dict: Dict[str, Collection] = {}

    def set_handler(self, collection: str):
        self.handler_dict[collection] = self.db[collection]

    def insert_one(self, collection: str, data: dict) -> ObjectId:
        object_id = self.handler_dict[collection].insert_one(data).inserted_id
        return object_id

    def find_one(self, collection: str, *args) -> dict:
        return self.handler_dict[collection].find_one(*args)

    def find(self, collection: str, *args) -> Cursor:
        cursor = self.handler_dict[collection].find(*args)
        return cursor

    def update_one(self, collection: str, *args) -> bool:
        self.handler_dict[collection].update_one(*args)
        return True

    def aggregate(self, collection: str, *args) -> CommandCursor:
        return self.handler_dict[collection].aggregate(*args)

mongo_util = MongoUtil()