import time
import os

import schedule
from dotenv import load_dotenv

from resources.crawler.BTL_WebBatDongSan import CrawlAloNhaDat 

def start_crawl_data():
    #Select option choose
    try:
        load_dotenv()
        PROVINCE = os.getenv("PROVINCE")
        PROPERTY_TYPE = os.getenv("PROPERTY_TYPE")
        TYPE_POST = os.getenv("TYPE_POST")
        DIRECTION = os.getenv("DIRECTION")
        SQUARE = os.getenv("SQUARE")
        PRICE = os.getenv("PRICE")
        DISTRICT = os.getenv("DISTRICT")
        crawl_data = CrawlAloNhaDat()
        crawl_data.start_crawl()
        crawl_data.chose_type_data_to_find(province=PROVINCE, property_type=PROPERTY_TYPE,direction=DIRECTION,
                            district=DISTRICT, price=PRICE, square=SQUARE, type_post=TYPE_POST )
        crawl_data.end_task()
    finally:
        print("Run task complete ")

schedule.every().day.at("06:00").do(start_crawl_data)
while True:
    schedule.run_pending()
    time.sleep(25)
