# 起手式
import requests
from column_4 import BeautifulSoup
import json
URL = "https://docs.mongodb.com/manual/"
resp = requests.get(URL)
soup = BeautifulSoup(resp.text,"html5lib")

# 參考 ldic = {"l1":["l2":["l3":"l4":["l5":""]]]}
listMongo = []
ldisc = {}
column = soup.select("li.toctree-l1")
#讓title形成字典般的格式分布
for l1 in range(len(column)):
    column_1 = column[l1]
    ldisc[column_1.select_one("a").text] = []
    for l2 in range(len(column_1.select("ul > li.toctree-l2"))):
        column_2 = column_1.select("li.toctree-l2")[l2]
        ldisc[column_1.select_one("a").text].append({column_2.select_one("a").text:[]})
        for l3 in range(len(column_2.select("ul > li.toctree-l3"))):
            column_3 = column_2.select("li.toctree-l3")[l3]
            ldisc[column_1.select_one("a").text][l2][column_2.select_one("a").text].append({column_3.select_one("a").text:[]})
            for l4 in range(len(column_3.select("ul > li.toctree-l4"))):
                column_4 = column_3.select("li.toctree-l4")[l4]
                ldisc[column_1.select_one("a").text][l2][column_2.select_one("a").text][l3][column_3.select_one("a").text].append({column_4.select_one("a").text:[]})
                for l5 in range(len(column_4.select("ul > li.toctree-l5"))):
                    column_5 = column_4.select("li.toctree-l5")[l5]
                    ldisc[column_1.select_one("a").text][l2][column_2.select_one("a").text][l3][column_3.select_one("a").text][l4][column_4.select_one("a").text].append(column_5.select_one("a").text)
listMongo.append(ldisc)
# 存json檔
with open("D:/MongoBD/notebook/Mongo_Catalog.json","w",encoding="UTF-8") as f:
    f.write(json.dumps(listMongo, ensure_ascii=False, indent=4))