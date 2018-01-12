# 起手式
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, wait
from datetime import datetime
import json
import re
import time


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


class Crawler():
    # 取得商品網址
    @staticmethod
    def craw_goods_url(items):
        resp = requests.get(items, headers=headers)
        soup = BeautifulSoup(resp.text, 'html5lib')
        goods_urls = soup.select("li.eachGood > a")
        for url in goods_urls:
            r = re.findall('/goods/GoodsDetail.jsp\?i_code=\d*.*', url.get("href"))
            product_urls.append(DOMAIN + r[0])
        print(len(product_urls))

    # 取得所有商品資訊
    @staticmethod
    def crawler_item_data(item):
        # item_data = {
        #     "id": "",
        #     "title": "",
        #     "url": "",
        #     "discount_price": 0,
        #     "original_price": 0,
        #     "tags": []
        # }
        item_data = {}
        resp = requests.get(item, headers=headers)
        soup = BeautifulSoup(resp.text, 'html5lib')
        item_data["title"] = soup.select_one("h1").text  # 標題塞入標題
        item_data["url"] = item  # url塞入url
        itemid_tag = soup.select("ul#categoryActivityInfo > li")
        for it_des in itemid_tag:
            try:
                item_data['id'] = re.findall("\d{4}\d+", it_des.text)[0]  # id塞入id
            except:
                item_data["tags"].append(it_des.text)  # 描述塞入Tag
        item_tag = soup.select("div.related_category > dl > * > a")
        for tag in item_tag:
            item_data["tags"].append(tag.text)  # 類別塞入Tag
        # 舊價格、新價格
        li_prices = soup.select("ul.prdPrice > li")
        del_price = li_prices[0].select("del")
        if len(del_price) > 0:
            del_price = re.match("(\d*)[,]{0,1}(\d*)", del_price[0].text)
            price = del_price.group(1) + del_price.group(2)
            temp_discount = re.match("(\d*)[,]{0,1}(\d*)", li_prices[1].select("span")[0].text)
            discount_price = temp_discount.group(1) + temp_discount.group(2)
        else:
            price = "0"
            temp_discount = re.match("(\d*)[,]{0,1}(\d*)", li_prices[0].select("span")[0].text)
            discount_price = temp_discount.group(1) + temp_discount.group(2)
        item_data["discount_price"] = int(discount_price)  # 新價格塞入折扣價
        item_data["original_price"] = int(price)  # 原價格塞入原價格
        count.append("success")
        item_num = len(count)
        item_datas.append(item_data)  # 存取全部資料囉
        print(item_num)
        if 0 == item_num % 1000:
            with open('D:\woodnata_note\data_run_{}'.format(item_num), 'a',
                      encoding="utf-8") as f:  # 將item_datas存為json檔
                f.write(json.dumps(item_datas[:1000], ensure_ascii=False, indent=4))
            del item_datas[:1000]
            print(str(item_num) + "  存檔")


def main():
    Stopwatch.stop_start("work")
    resp = requests.get(HOME_PAGE_URL, headers=headers)
    soup = BeautifulSoup(resp.text, 'html5lib')
    # 所有分類網址
    for s in soup.select("ul#bt_cate_top > li > a"):  # 左側目錄欄位的每個欄位連結
        r = re.findall('/category/DgrpCategory.jsp\?d_code=\d*.*', s.get('href'))  # 找d_code分類的網址
        category_urls.append(DOMAIN + r[0]) if len(r) > 0 else r
    # 取得所有頁數資訊
    print(len(category_urls))
    for url in category_urls:
        # 頁數
        try:
            r = re.findall("/\s*(\d*)", BeautifulSoup(requests.get(url, headers=headers).text, 'html5lib') \
                           .select_one("div.pageArea > dl > dt > span").text)  # 總頁數
            for page in range(1, int(r[0]) + 1):
                item_urls.append(url + PAGE_NUM.format(page))
        except:
            # 直接存原網址
            item_urls.append(url)
    Stopwatch.stop_start("work")
    print(len(item_urls))
    threads = ThreadPoolExecutor(Thread_num)  # 設定多執行緒
    futures = [threads.submit(Crawler.craw_goods_url, items) for items in item_urls]  # 將工作事項交給futures管理
    wait(futures)
    Stopwatch.stop_start("craw_goods_url ")
    print(len(product_urls))
    threads = ThreadPoolExecutor(Thread_num)  # 設定多執行緒
    futures = [threads.submit(Crawler.crawler_item_data, item) for item in product_urls]  # 將工作事項交給futures管理
    wait(futures)


if __name__ == "__main__":
    HOME_PAGE_URL = "https://www.momoshop.com.tw/category/LgrpCategory.jsp?l_code=1306000000"  # 首頁
    DOMAIN = "https://www.momoshop.com.tw"
    PAGE_NUM = "&p_pageNum={}"  # to match the page of items' url
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
    }  # headers for requests get
    category_urls = []  # 商品首頁url
    product_urls = []  # 商品url
    item_urls = []  # 總商品頁url
    item_datas = []  # 全部資料
    Thread_num = 10
    count = []
    main()
    Stopwatch.stop_start("craw all datas  ")
    with open('D:\woodnata_note\data_run_{}'.format(len(item_urls)), 'a', encoding="utf-8") as f:  # 將item_datas存為json檔
        f.write(json.dumps(item_datas, ensure_ascii=False, indent=4))

    print("耗時:" + timeSpent)
