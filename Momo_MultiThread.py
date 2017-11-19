# 起手式
import requests
from bs4 import BeautifulSoup as bs
from queue import Queue
from threading import Thread
from datetime import datetime
import json
import re
import time
#需要設定的唷
#l,m,d,i
_step_ = True
URLsource = "https://www.momoshop.com.tw"
URL = "https://www.momoshop.com.tw/category/LgrpCategory.jsp?l_code=1400300000"
pageURL1 = "&lowestPrice=&highestPrice=&whcode=&cpyn=&p_pageNum=%s"
pageURL2 = "&p_orderType=4&lowestPrice=&highestPrice=&whcode=&cpyn=&p_pageNum=%s"
listmomo = [] # 存商品頁網址
listmomoall = [] # 存全部商品頁網址
listmomo_goods = [] # 存單品網址
items_data = [] #存單品資料
headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
}
queue = Queue()
def worker():
    while not queue.empty():
        items = queue.get()
        crawler(items)

def crawler(items):
    if _step_ == True:# 將商品頁的每一頁網址抓下來
        print("now is " + str(items))
        res = requests.get(listmomoall[items], headers=headers)
        s = bs(res.text, 'html5lib')
        eachgood = s.select("div.prdListArea > ul > li.eachGood > a")  # 單頁商品數
        for j in range(len(eachgood)):
            listmomo_goods.append(URLsource + eachgood[j].get("href", "no"))
            print("now is go  " + str(items) + ":" + str(j))
            time.sleep(0.001)
    else :# 抓所有品項資訊
        print("now are " + str(items))
        res = requests.get(listmomo_goods[items], headers=headers)
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
        print("now are go  " + str(items) + ":")
        item_data = {"title": title, "catalog": Catalog,
                     "price": [{"del_price": del_price, 'now_price': now_price}]}
        items_data.append(item_data)
    print("item " + str(items) + " crawler done")

if __name__ == "__main__":
    thStart = datetime.now()
    resp = requests.get(URL,headers = headers)
    s = bs(resp.text, 'html5lib')
    for ss in range(len(s.select("a"))): # 抓主頁
        # 有些內容點進去是該商家商品頁  bt_2_107
        r_category = re.findall('/category/DgrpCategory.jsp\?d_code=.*bt_2_107.*ctype=B',s.select("a")[ss].get("href","no"))
        # 有些則是點進去就是單品
        r_goods = re.findall('/goods/GoodsDetail.jsp\?i_code=.*bt_2_107.*ctype=B',s.select("a")[ss].get("href","no"))
        if len(r_category) > 0 :
            listmomo.append(URLsource+r_category[0])
        if len(r_goods) > 0 :
            listmomo_goods.append(URLsource+r_goods[0])
    print(listmomo)
    print(listmomo_goods)
    for i in range(len(listmomo)): # 將商品頁的每一頁網址抓下來
        res = requests.get(listmomo[i], headers=headers)
        s = bs(res.text, 'html5lib')
        pages = re.findall("/(\d*)", s.select_one("div.pageArea > dl > dt > span").text)[0]  # 商品頁數
        pages = int(pages) # 轉成數字
        rls = re.findall('https://www.momoshop.com.tw/category/DgrpCategory.jsp\?d_code=\d*',listmomo[i])
        if len(rls) < 1 :
            rls = re.findall('https://www.momoshop.com.tw/category/DgrpCategory.jsp\?d_code=\d*',listmomo[i])[0]
            r = rls[0] + pageURL2
        else :
            r = rls[0] + pageURL1
        for page in range(1,(pages+1)):
            r%page #商品頁每一頁的網址
            listmomoall.append(r)
    thEnd = datetime.now()
    timeSpent = str(thEnd - thStart).split('.')[0]
    print("first = " + timeSpent);
    pages = len(listmomoall)
    numThread = 4

    for i in range(1,5):  # 爬item動作
        queue.put(i)
    threads = []
    for j in range(numThread):  # 建立多執緒清單
        threads.append(Thread(target=worker))
    for i in range(len(threads)):  # 將所有執行緒啟動，worker()開始到queue拿取工作
        threads[i].start()
        print("run")
    for i in range(len(threads)):  # 等所有worker()工作完畢
        threads[i].join()

    thEnd = datetime.now()
    timeSpent = str(thEnd - thStart).split('.')[0]
    print("upper = " + timeSpent);
    _step_ = False #切換
    print("下半段")

    items = len(listmomo_goods)
    for i in range(1,5):  # 爬item動作
        queue.put(i)
    threads = []
    for j in range(numThread):  # 建立多執緒清單
        threads.append(Thread(target=worker))
    for i in range(len(threads)):  # 將所有執行緒啟動，worker()開始到queue拿取工作
        threads[i].start()
        print("run2")
    for i in range(len(threads)):  # 等所有worker()工作完畢
        threads[i].join()
    thEnd = datetime.now()
    timeSpent = str(thEnd - thStart).split('.')[0]

    with open('D:\專題\momo_Data_roadrun.json', 'w', encoding="utf-8") as f:  # 將resList存為json檔
        f.write(json.dumps(items_data, ensure_ascii=False, indent=4))

    print("執行緒:" + str(numThread))
    print("筆數:" + str(len(items_data)))
    print("耗時:" + timeSpent)
