# 起手式
import requests
from bs4 import BeautifulSoup
# from queue import Queue
# from threading import Thread
from concurrent.futures import ThreadPoolExecutor, wait
from datetime import datetime
import json
import re

_step_ = True

from datetime import datetime


class Stopwatch():
    start = None

    @staticmethod
    def stop_start(event):
        stop = datetime.now()
        if Stopwatch.start == None:
            Stopwatch.start = datetime.now()
            print(event)
        else:
            time_elapsed = str(stop - Stopwatch.start)
            Stopwatch.start = stop
            print("break point " + event + " time elapsed : " + time_elapsed)


# queue = Queue()
# def worker():
#     while not queue.empty():
#         items = queue.get()
#         crawler(items)
class Crawler():
    # def __init__(self): #當想要在呼叫時就做某些事的時候才使用
    #     pass

    @staticmethod
    def craw_item_data(items, datas, headers):
        resp = requests.get(items, headers=headers)
        soup = BeautifulSoup(resp.text, 'html5lib')

        li_prices = soup.select("ul.prdPrice > li")
        title = soup.select_one("h1").text
        li_categories = soup.select("#bt_2_layout_NAV > ul > li")
        categories = []
        for li_category in li_categories:
            categories.append(li_category.text)

        del_price = li_prices[0].select("del")
        if len(del_price):
            price = del_price[0].text
            discount_price = li_prices[1].select("span")[0].text
        else:
            price = ""
            discount_price = li_prices[0].select("span")[0].text
        item_data = {"title": title, "categories": categories,
                     "price": [{"price": price, 'discount price': discount_price}]}
        datas.append(item_data)
        count.append("success")
        item_num = len(count)
        if 0 == item_num%1000 :
            with open('D:\woodnata_note\data_{}.json'.format(item_num), 'a', encoding="utf-8") as f:  # 將all_data存為json檔
                f.write(json.dumps(datas[:1000], ensure_ascii=False, indent=4))
                del datas[:1000]
            print(str(item_num) + "  存檔")
        print("Done crawling item: " + str(item_num))

    @staticmethod
    def craw_goods_url(items, goods, headers, url_source):
        resp = requests.get(items, headers=headers)
        soup = BeautifulSoup(resp.text, 'html5lib')
        eachgood = soup.select("div.prdListArea > ul > li.eachGood > a")  # 單頁商品數
        for good in eachgood:
            goods.append(url_source + good.get("href", "no"))
        print("itemspage :  " + str(items) + " crawler done")


def main():
    DOMAIN = "https://www.momoshop.com.tw"
    URL = "https://www.momoshop.com.tw/category/LgrpCategory.jsp?l_code=1400300000"
    URL_PATTERN_1 = "&lowestPrice=&highestPrice=&whcode=&cpyn=&p_pageNum=%s"
    URL_PATTERN_2 = "&p_orderType=4&lowestPrice=&highestPrice=&whcode=&cpyn=&p_pageNum=%s"
    category_urls = []  # 存各類別商品第一頁網址
    product_urls = []  # 存全部商品頁網址
    item_urls = []  # 存單品網址
    item_datas = []  # 存單品資料
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
    }
    Stopwatch.stop_start("work")
    resp = requests.get(URL, headers=headers)
    soup = BeautifulSoup(resp.text, 'html5lib')
    for a in soup.select("a"):  # 抓主頁
        # 有些內容點進去是該商家商品頁  bt_2_107
        r_category = re.findall('/category/DgrpCategory.jsp\?d_code=.*bt_2_107.*ctype=B',
                                a.get("href", "no"))
        # 有些則是點進去就是單品
        r_goods = re.findall('/goods/GoodsDetail.jsp\?i_code=.*bt_2_107.*ctype=B', a.get("href", "no"))
        if len(r_category) > 0:
            category_urls.append(DOMAIN + r_category[0])
        if len(r_goods) > 0:
            item_urls.append(DOMAIN + r_goods[0])
    print(len(category_urls))
    print(len(item_urls))
    for i in range(len(category_urls)):  # 將每個商品頁的每一頁網址抓下來
        resp = requests.get(category_urls[i], headers=headers)
        soup = BeautifulSoup(resp.text, 'html5lib')
        pages = re.findall("/(\d*)", soup.select_one("div.pageArea > dl > dt > span").text)[0]  # 商品頁數
        pages = int(pages)  # 轉成數字
        r_urls = re.findall('https://www.momoshop.com.tw/category/DgrpCategory.jsp\?d_code=\d*', category_urls[i])
        if len(r_urls) < 1:
            r_urls = re.findall('https://www.momoshop.com.tw/category/DgrpCategory.jsp\?d_code=\d*', category_urls[i])[0]
            r = r_urls[0] + URL_PATTERN_2
        else:
            r = r_urls[0] + URL_PATTERN_1
        for page in range(1, (pages + 1)):
            # r%page #商品頁每一頁的網址
            product_urls.append(r % page)

    ###計時
    Stopwatch.stop_start("all the page")
    ###
    pages = len(product_urls)
    Thread_num = 4  # 多執行緒數目
    print(pages)

    threads = ThreadPoolExecutor(Thread_num)  # 設定多執行緒
    crawler = Crawler()
    futures = [threads.submit(crawler.craw_goods_url, product_urls[page], item_urls, headers, DOMAIN)
               for page in range(pages)]  # 將工作事項交給futures管理
    wait(futures) # 等待工作完成，此程序才會繼續動作
    # for i in range(1,pages):  # 爬page動作
    #     queue.put(i)
    # threads = []
    # for j in range(numThread):  # 建立多執緒清單
    #     threads.append(Thread(target=worker))
    # for i in range(len(threads)):  # 將所有執行緒啟動，worker()開始到queue拿取工作
    #     threads[i].start()
    #     print("run")
    # for i in range(len(threads)):  # 等所有worker()工作完畢
    #     threads[i].join()

    ### 計時
    Stopwatch.stop_start("craw all items")
    ###
    items = len(item_urls)
    print(items)
    threads = ThreadPoolExecutor(Thread_num)  # 設定多執行緒
    futures = [threads.submit(crawler.craw_item_data, item_urls[item], item_datas, headers)
               for item in range(items)]  # 將工作事項交給futures管理
    wait(futures)  # 等待工作完成，此程序才會繼續動作

    # for i in range(1,items+1):  # 爬item動作
    #     queue.put(i)
    # threads = []
    # for j in range(numThread):  # 建立多執緒清單
    #     threads.append(Thread(target=worker))
    # for i in range(len(threads)):  # 將所有執行緒啟動，worker()開始到queue拿取工作
    #     threads[i].start()
    #     print("run2")
    # for i in range(len(threads)):  # 等所有worker()工作完畢
    #     threads[i].join()

    ### 計時結束
    Stopwatch.stop_start("all items datas done ")
    ###
    with open('D:\專題\momo_Data_roadrun.json', 'a', encoding="utf-8") as f:  # 將resList存為json檔
        f.write(json.dumps(item_datas, ensure_ascii=False, indent=4))

    print("執行緒:" + str(Thread_num))


if __name__ == "__main__":
    count = []
    main()
