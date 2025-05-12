import time
import os

import schedule
from dotenv import load_dotenv

from resources.crawler.BTL_WebBatDongSan import CrawlAloNhaDat 

def start_crawl_data():
    try:
        load_dotenv()
        PROVINCE = os.getenv("PROVINCE")
        PROPERTY_TYPE = os.getenv("PROPERTY_TYPE")
        TYPE_POST = os.getenv("TYPE_POST")
        DIRECTION = os.getenv("DIRECTION")
        SQUARE = os.getenv("SQUARE")
        PRICE = os.getenv("PRICE")
        DISTRICT = os.getenv("DISTRICT")

        # B 0: Khoi tao cac gia tri, hang so can thiet
        crawl_data = CrawlAloNhaDat()

        # B1 : Mo Trinh duyet voi URL co san
        crawl_data.start_crawl()

        # B2 : Chon thong tin can thiet de tim
        crawl_data.chose_type_data_to_find(province=PROVINCE, property_type=PROPERTY_TYPE,direction=DIRECTION,
                            district=DISTRICT, price=PRICE, square=SQUARE, type_post=TYPE_POST )
        # B3 : Nhan nut tim kiem de tim thong tin
        crawl_data.click_search_button()

        # B4, B5: Lay tat ca du lieu cua bai viet o cac trang
        crawl_data.crawl_data()

        # B6 : Luu du lieu vao Excel
        crawl_data.save_data_to_excel()

        # Ket thuc crawl
        crawl_data.end_task()
        # Gui mail thong bao ket qua
        crawl_data.send_mail_crawl_state()

    finally:
        print("Run task complete ")

# B7: Set lich chay luc 6h sang
schedule.every().day.at("06:00").do(start_crawl_data)
while True:
    schedule.run_pending()
    time.sleep(25)
