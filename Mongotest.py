# 起手式
import requests
from bs4 import BeautifulSoup
import json
URL = "https://docs.mongodb.com/manual/"
res = requests.get(URL)
bs = BeautifulSoup(res.text,"html5lib")

# 參考 ldic = {"l1":["l2":["l3":"l4":["l5":""]]]}
listMongo = []
ldisc = {}
#讓title形成字典般的格式分布
for l1 in range(len(bs.select("li.toctree-l1"))):
    bs1 = bs.select("li.toctree-l1")[l1]
    ldisc[bs1.select_one("a").text] = []
    for l2 in range(len(bs.select("li.toctree-l1")[l1].select("ul > li.toctree-l2"))):
        bs2 = bs1.select("li.toctree-l2")[l2]
        ldisc[bs1.select_one("a").text].append({bs2.select_one("a").text:[]})
        for l3 in range(len(bs.select("li.toctree-l1")[l1].select("ul > li.toctree-l2")[l2].select("ul > li.toctree-l3"))):
            bs3 = bs2.select("li.toctree-l3")[l3]
            ldisc[bs1.select_one("a").text][l2][bs2.select_one("a").text].append({bs3.select_one("a").text:[]})
            for l4 in range(len(bs.select("li.toctree-l1")[l1].select("ul > li.toctree-l2")[l2].select("ul > li.toctree-l3")[l3].select("ul > li.toctree-l4"))):
                bs4 = bs3.select("li.toctree-l4")[l4]
                ldisc[bs1.select_one("a").text][l2][bs2.select_one("a").text][l3][bs3.select_one("a").text].append({bs4.select_one("a").text:[]})
                for l5 in range(len(bs.select("li.toctree-l1")[l1].select("ul > li.toctree-l2")[l2].select("ul > li.toctree-l3")[l3].select("ul > li.toctree-l4")[l4].select("ul > li.toctree-l5"))):
                    bs5 = bs4.select("li.toctree-l5")[l5]
                    ldisc[bs1.select_one("a").text][l2][bs2.select_one("a").text][l3][bs3.select_one("a").text][l4][bs4.select_one("a").text].append(bs5.select_one("a").text)
listMongo.append(ldisc)
# 存json檔
with open("D:/MongoBD/notebook/Mongo_Catalog.json","w",encoding="UTF-8") as f:
    f.write(json.dumps(listMongo, ensure_ascii=False, indent=4))