# 起手式
import requests
from bs4 import BeautifulSoup
import re
URLsource = "https://www.momoshop.com.tw"
URL = "https://www.momoshop.com.tw/category/LgrpCategory.jsp?l_code=1400300000"
headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
}
resp = requests.get(URL,headers = headers)
s = BeautifulSoup(resp.text, 'html5lib')
URLsource = "https://www.momoshop.com.tw"
listmomo = []
listmomo_goo = []
for ss in range(len(s.select("a"))):
    # 有些內容點進去是該商家商品頁，有些則是點進去就是單品， bt_2_107
    r = re.findall('/category/DgrpCategory.jsp\?d_code=.*bt_2_107.*ctype=B',s.select("a")[ss].get("href","no"))
    r1 = re.findall('/goods/GoodsDetail.jsp\?i_code=.*bt_2_107.*ctype=B',s.select("a")[ss].get("href","no"))
    if len(r) > 0 :
        listmomo.append(URLsource+r[0])
    if len(r1) > 0 :
        listmomo_goo.append(URLsource+r1[0])


for i in range(len(listmomo)):
    res = requests.get(listmomo[i],headers = headers)
    s = BeautifulSoup(res.text, 'html5lib')
    eachgood = s.select("div.prdListArea > ul > li.eachGood > a")
    for j in range(len(eachgood)):
        listmomo_goo.append(URLsource+eachgood[j].get("href","no"))

items_data = []
item = 0
for item in range(len(listmomo_goo)):
    res = requests.get(listmomo_goo[item],headers = headers)
    s = BeautifulSoup(res.text, 'html5lib')
    title = s.select_one("h1").text
    Catalog = []
    sCatalog = s.select("#bt_2_layout_NAV > ul > li")
    for i in range(len(sCatalog)):
        Catalog.append(sCatalog[i].text)
    del_price = s.select("ul.prdPrice > li")[0].select("del")
    if len(del_price) > 0 :
        del_price = s.select("ul.prdPrice > li")[0].select("del")[0].text
        now_price = s.select("ul.prdPrice > li")[1].select("span")[0].text
    else :
        del_price = ""
        now_price = s.select("ul.prdPrice > li")[0].select("span")[0].text

    item_data = {"title":title,"catalog":Catalog,"price":[{"del_price":del_price,'now_price':now_price}]}
    items_data.append(item_data)