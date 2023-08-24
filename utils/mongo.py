import pymongo
from bootstrap_config import app_config


def get_mongo():
    client = pymongo.MongoClient(app_config["MONGO_URL"])
    return client["df_pro"]
