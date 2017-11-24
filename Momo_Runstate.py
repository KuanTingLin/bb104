# 起手式
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, wait
from datetime import datetime
import json
import re
import time

URL = "https://www.momoshop.com.tw/category/LgrpCategory.jsp?l_code=1306000000"  # 首頁
domain = "https://www.momoshop.com.tw"
Match_page = "&p_pageNum={}"  # to match the page of items' url
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
}  # headers for requests get
Cat_url_list = [] # 商品首頁url
Goods_urls = [] # 商品url
Cat_page_urls = [] # 總商品頁url
all_data = [] # 全部資料


# 取得商品網址
def crawler_item_url(page) :
    rep_itemurl = requests.get(Cat_page_urls[page], headers=headers)
    ss = BeautifulSoup(rep_itemurl.text, 'html5lib')
    goods_urls = ss.select("li.eachGood > a")
    for j in range(len(goods_urls)):
        r = re.findall('/goods/GoodsDetail.jsp\?i_code=\d*.*', goods_urls[j].get("href"))
        Goods_urls.append(domain + r[0])
    print(page)


# 取得所有商品資訊
def crawler_item_data(item) :
    item_data = {
        "id": "",
        "title": "",
        "url": "",
        "discount_price": 0,
        "original_price": 0,
        "tags": []
    }
    resp = requests.get(Goods_urls[item], headers=headers)
    s = BeautifulSoup(resp.text, 'html5lib')
    item_data["title"] = s.select_one("h1").text  # 標題塞入標題
    item_data["url"] = Goods_urls[item]
    itemid_tag = s.select("ul#categoryActivityInfo > li")
    for it_des in range(0, len(itemid_tag)):
        try:
            item_data['id'] = re.findall("\d{4}\d+", itemid_tag[it_des].text)[0]  # id塞入id
        except:
            item_data["tags"].append(itemid_tag[it_des].text)  # 描述塞入Tag
    item_tag = s.select("div.related_category > dl > * > a")
    for tag in range(1,len(item_tag)):
        item_data["tags"].append(item_tag[tag].text)  # 類別塞入Tag
    # 舊價格、新價格
    ol_price = s.select("ul.prdPrice > li")[0].select("del")
    if len(ol_price) > 0:
        ol_price = re.match("(\d*)[,]{0,1}(\d*)",ol_price[0].text)
        ol_price = ol_price.group(1) + ol_price.group(2)
        dc_price = re.match("(\d*)[,]{0,1}(\d*)",s.select("ul.prdPrice > li")[1].select("span")[0].text)
        dc_price = dc_price.group(1) + dc_price.group(2)
    else:
        ol_price = "0"
        dc_price = re.match("(\d*)[,]{0,1}(\d*)",s.select("ul.prdPrice > li")[0].select("span")[0].text)
        dc_price = dc_price.group(1) + dc_price.group(2)
    item_data["discount_price"] = int(dc_price)  # 新價格塞入折扣價
    item_data["original_price"] = int(ol_price)  # 原價格塞入原價格
    all_data.append(item_data) # 存取全部資料囉
    print(item)
    if 0 == item%1000 :
        with open('D:\專題\momo_Data_roadrun.json', 'a', encoding="utf-8") as f:  # 將all_data存為json檔
            f.write(json.dumps(all_data, ensure_ascii=False, indent=4))
        all_data[:] = []
        print(str(item) + "  存檔")



if __name__ == "__main__":
    Thread_num = 10
    thStart = datetime.now()
    resp = requests.get(URL, headers=headers)
    s = BeautifulSoup(resp.text, 'html5lib')
    # 所有分類網址
    for i in range(len(s.select("ul#bt_cate_top > li > a"))):  # 左側目錄欄位的每個欄位連結
        r = re.findall('/category/DgrpCategory.jsp\?d_code=\d*.*', s.select("ul#bt_cate_top > li > a")[i].get('href'))  # 找d_code分類的網址
        Cat_url_list.append(domain + r[0]) if len(r) > 0 else r
    # 取得所有頁數資訊
    print(len(Cat_url_list))
    for i in range(len(Cat_url_list)):
        # 頁數
        try:
            r = re.findall("/\s*(\d*)",BeautifulSoup(requests.get(Cat_url_list[i], headers=headers).text, 'html5lib') \
                           .select_one("div.pageArea > dl > dt > span").text)  # 總頁數
            for page in range(1, int(r[0]) + 1):
                Cat_page_urls.append(Cat_url_list[i] + Match_page.format(page))
        except:
            # 直接存原網址
            Cat_page_urls.append(Cat_url_list[i])
    thEnd = datetime.now()
    timeSpent = str(thEnd - thStart).split('.')[0]
    print(timeSpent)
    print(len(Cat_page_urls))
    threads = ThreadPoolExecutor(Thread_num)  # 設定多執行緒
    futures = [threads.submit(crawler_item_url, page) for page in range(len(Cat_page_urls)+1)]  # 將工作事項交給futures管理
    wait(futures)
    thEnd = datetime.now()
    timeSpent = str(thEnd - thStart).split('.')[0]
    print(timeSpent)
    print(len(Goods_urls))
    threads = ThreadPoolExecutor(Thread_num)  # 設定多執行緒
    futures = [threads.submit(crawler_item_data, item) for item in range(len(Goods_urls))]  # 將工作事項交給futures管理
    wait(futures)

    thEnd = datetime.now()
    timeSpent = str(thEnd - thStart).split('.')[0]
    print(all_data)
    with open('D:\專題\momo_Data_roadrun.json', 'a', encoding="utf-8") as f:  # 將all_data存為json檔
        f.write(json.dumps(all_data, ensure_ascii=False, indent=4))

    print("執行緒:" + str(Thread_num))
    print("筆數:" + str(len(all_data)))
    print("耗時:" + timeSpent)