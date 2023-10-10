from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from settings import settings
client = MongoClient(
    "mongodb+srv://anand:root@cluster0.2swsj.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))["df_pro"]


def get_mongo():
    return client
