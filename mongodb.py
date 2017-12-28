from pymongo import MongoClient
import json
client = MongoClient('localhost',27017)
#db name
db = client['bb104-3']

with open('D:\專題\momo_Data_healthy.json', 'r', encoding="utf-8") as f:
    input = json.load(f)
    # insert datas using method 'insert_many()'
    #[dbname].[collection].mrthod
    # db.momoHealthyThings.insert_many(input)

output = db.momoHealthyThings.find()
print(output)