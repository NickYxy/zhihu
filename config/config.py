from pymongo import *


config_dict = dict(
    USER_AVATAR_DIR='static/user_avatar',
    CATEGORY_PIC_DIR='static/category_pic',
)

#mongodb config
db_name = 'mongo_love'
client = MongoClient("mongodb://localhost:27017")
db = client[db_name]