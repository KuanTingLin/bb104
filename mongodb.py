from pymongo import MongoClient
import json
client = MongoClient('localhost',27017)

db = client['testDatabase'] # db_name = testDatabase
collection = db['testCollection'] # collection_name = testCollection
# collection.insert_one({"key":"value"})
with open('D:/woodnata_note/test_data') as file:
    str_cont = file.read()
    list_cont = json.loads(str_cont)
    collection.insert_many(list_cont) # insert a 'list' of data using method 'insert_many()'

#using for-loop to iterate through curser object
for doc in db.testCollection.find():
    print(doc)