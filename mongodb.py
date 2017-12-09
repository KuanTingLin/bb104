from pymongo import MongoClient
import json
client = MongoClient('localhost',27017)
db = client['bb104-3']

with open('D:\專題\momo_Data_healthy.json', 'r', encoding="utf-8") as f:
    input = json.load(f)
    # insert datas using method 'insert_many()'
    db.momoHealthyThings.insert_many(input)