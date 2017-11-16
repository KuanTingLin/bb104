# 起手式
import requests
from bs4 import BeautifulSoup as bs
from queue import Queue
from threading import Thread
from datetime import datetime
import json
import re
#需要設定的唷
_step_ = True
URLsource = "https://www.momoshop.com.tw"
URL = "https://www.momoshop.com.tw/category/LgrpCategory.jsp?l_code=1400300000"
pageURL = "&lowestPrice=&highestPrice=&whcode=&cpyn=&p_pageNum=%s"
listmomo = [] # 存商品頁網址
listmomoall = [] # 存全部商品頁網址
listmomo_goods = [] # 存單品網址
items_data = [] #存單品資料
headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
}

def worker():
    while not queue.empty():
        page = queue.get()
        crawler(page)



def crawler(items):
    if _step_ == True:# 將商品頁的每一頁網址抓下來
        for i in range(len(listmomo)):
            res = requests.get(listmomo[i], headers=headers)
            s = bs(res.text, 'html5lib')
            eachgood = s.select("div.prdListArea > ul > li.eachGood > a")  # 單頁商品數
            for j in range(len(eachgood)):
                listmomo_goods.append(URLsource + eachgood[j].get("href", "no"))
    else :# 抓所有品項資訊
        for item in range(items):
            res = requests.get(listmomo_goods[item], headers=headers)
            s = bs(res.text, 'html5lib')
            title = s.select_one("h1").text
            Catalog = []
            sCatalog = s.select("#bt_2_layout_NAV > ul > li")
            for i in range(len(sCatalog)):
                Catalog.append(sCatalog[i].text)
            del_price = s.select("ul.prdPrice > li")[0].select("del")
            if len(del_price) > 0:
                del_price = s.select("ul.prdPrice > li")[0].select("del")[0].text
                now_price = s.select("ul.prdPrice > li")[1].select("span")[0].text
            else:
                del_price = ""
                now_price = s.select("ul.prdPrice > li")[0].select("span")[0].text

            item_data = {"title": title, "catalog": Catalog,
                         "price": [{"del_price": del_price, 'now_price': now_price}]}
            items_data.append(item_data)
    print("item " + str(page) + " crawler done")

if __name__ == "__main__":
    resp = requests.get(URL,headers = headers)
    s = bs(resp.text, 'html5lib')
    for ss in range(len(s.select("a"))): # 抓主頁
        # 有些內容點進去是該商家商品頁  bt_2_107
        r_category = re.findall('/category/DgrpCategory.jsp\?d_code=.*bt_2_107.*ctype=B',s.select("a")[ss].get("href","no"))
        # 有些則是點進去就是單品
        r_goods = re.findall('/goods/GoodsDetail.jsp\?i_code=.*bt_2_107.*ctype=B',s.select("a")[ss].get("href","no"))
        if len(r) > 0 :
            listmomo.append(URLsource+r_category[0])
        if len(r1) > 0 :
            listmomo_goods.append(URLsource+r_goods[0])

    for i in range(len(listmomo)): # 將商品頁的每一頁網址抓下來
        res = requests.get(listmomo[i], headers=headers)
        s = bs(res.text, 'html5lib')
        pages = re.findall("/(\d*)", s.select_one("div.pageArea > dl > dt > span").text)  # 商品頁數
        int(pages[0]) # 轉成數字
        r = re.findall('https://www.momoshop.com.tw/category/DgrpCategory.jsp\?d_code=\d*&p_orderType=1',listmomo[i])
        for page in range(1,pages+1) :
            r = r + pageURL%page #商品頁每一頁的網址
            listmomoall.append(r)



    for i in range(items, items - 10, -1):  # 爬item動作
        queue.put(i)
    threads = []
    for j in range(numThread):  # 建立多執緒清單
        threads.append(Thread(target=worker()))
    for i in range(len(threads)):  # 將所有執行緒啟動，worker()開始到queue拿取工作
        threads[i].start()
    for i in range(len(threads)):  # 等所有worker()工作完畢
        threads[i].join()

    items = len(listmomo_goods)
    for i in range(items, items-10, -1):  # 爬item動作
        queue.put(i)
    threads = []
    for j in range(numThread):  # 建立多執緒清單
        threads.append(Thread(target=worker()))
    for i in range(len(threads)):  # 將所有執行緒啟動，worker()開始到queue拿取工作
        threads[i].start()
    for i in range(len(threads)):  # 等所有worker()工作完畢
        threads[i].join()
    thEnd = datetime.now()
    timeSpent = str(thEnd - thStart).split('.')[0]

    with open('D:\Python\momo_Data_bikini.json', 'w', encoding="utf-8") as f:  # 將resList存為json檔
        f.write(json.dumps(items_data, ensure_ascii=False, indent=4))

    print("執行緒:" + str(numThread))
    print("文章數:" + str(len(CF_Data)))
    print("耗時:" + timeSpent)
