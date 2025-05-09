import time
import os
from datetime import date

from selenium import webdriver 
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests 
from dotenv import load_dotenv
import pandas as pd

from resources.utils import autoSendMail

dict_select_option_data = {
    "province" : {"Tất cả": "0", "Hà Nội": "1", "Hồ Chí Minh": "2", "Đà Nẵng": "3", "Hải Phòng": "4", "Cần Thơ": "5", "An Giang": "6", "Bà Rịa Vũng Tàu": "7", "Bạc Liêu": "8", "Bắc Kạn": "9", "Bắc Giang": "10", "Bắc Ninh": "12", "Bến Tre": "13", "Bình Dương": "14", "Bình Định": "15", "Bình Phước": "16", "Bình Thuận": "17", "Cà Mau": "18", "Cao Bằng": "19", "Đắk Lắk": "20", "Đăk Nông": "21", "Điện Biên": "22", "Đồng Nai": "23", "Đồng Tháp": "24", "Gia Lai": "25", "Hà Giang": "26", "Hà Nam": "27", "Hà Tĩnh": "28", "Hải Dương": "11", "Hậu Giang": "29", "Hòa Bình": "30", "Hưng Yên": "31", "Khánh Hòa": "32", "Kiên Giang": "33", "Kon Tum": "34", "Lai Châu": "35", "Lâm Đồng": "36", "Lạng Sơn": "37", "Lào Cai": "38", "Long An": "39", "Nam Định": "40", "Nghệ An": "41", "Ninh Bình": "42", "Ninh Thuận": "43", "Phú Thọ": "44", "Phú Yên": "45", "Quảng Bình": "46", "Quảng Nam": "47", "Quảng Ngãi": "48", "Quảng Ninh": "49", "Quảng Trị": "50", "Sóc Trăng": "51", "Sơn La": "52", "Tây Ninh": "53", "Thái Bình": "54", "Thái Nguyên": "55", "Thanh Hóa": "56", "Thừa Thiên-Huế": "57", "Tiền Giang": "58", "Trà Vinh": "59", "Tuyên Quang": "60", "Vĩnh Long": "61", "Vĩnh Phúc": "62", "Yên Bái": "63"}
    ,"post-type" : {'Cần bán': 'can-ban', 'Cho thuê': 'cho-thue', 'Cần mua': 'can-mua', 'Cần thuê': 'can-thue'}
    ,"square": {' Tất cả ': '0', 'Dưới 30 m2': '1', '30-50 m2': '2', '50-70 m2': '3', '70-100 m2': '4', '100-150 m2': '5', '150-200 m2': '6', '200-250 m2': '7', '250-300 m2': '8', '300-350 m2': '9', '350-400 m2': '10', '400-600 m2': '11', '600-800 m2': '12', '800-1000 m2': '13', 'Trên 1000 m2': '14'}
    ,"direction" : {' Tất cả ': '0', 'Đông': '1', 'Tây': '2', 'Nam': '3', 'Bắc': '4', 'Đông Nam': '5', 'Đông Bắc': '6', 'Tây Nam': '7', 'Tây Bắc': '8'}
    ,"price":{' Tất cả ': '0', 'Dưới 1 triệu': '1', '1 - 3 triệu': '2', '3 - 5 triệu': '3', '5 - 10 triệu': '4', '10 - 15 triệu': '5', '15 - 20 triệu': '6', '20 - 30 triệu': '7', '30 - 40 triệu': '8', '40 - 60 triệu': '9', '60 - 80 triệu': '10', '80 - 100 triệu': '11', '100 - 300 triệu': '12', '300 - 500 triệu': '13', '500 - 800 triệu': '14', '800 - 1 tỷ': '15', '1 - 2 tỷ': '16', '2 - 3 tỷ': '17', '3 - 4 tỷ': '18', '4 - 6 tỷ': '19', '6 - 8 tỷ': '20', '8 - 10 tỷ': '21', '10 - 15 tỷ': '22', '15 - 20 tỷ': '23', '20 - 30 tỷ': '24', '30 - 60 tỷ': '25', 'Trên 60 tỷ': '26'}
    ,"property-type" : {"Chọn loại BĐS": "nha-dat", "Nhà": "nha", "Nhà mặt tiền": "nha-mat-tien", " Nhà trong hẻm": "nha-trong-hem", "Biệt thự, nhà liền kề": "biet-thu-nha-lien-ke", "Căn hộ chung cư": "can-ho-chung-cu", "Phòng trọ, nhà trọ": "phong-tro-nha-tro", "Văn phòng": "van-phong", "Kho, xưởng": "kho-xuong", "Nhà hàng, khách sạn": "nha-hang-khach-san", "Shop, kiot, quán": "shop-kiot-quan", "Trang trại": "trang-trai", "Mặt bằng": "mat-bang", "Đất thổ cư, đất ở": "dat-tho-cu-dat-o", "Đất nền, liền kề, đất dự án": "dat-nen-lien-ke-dat-du-an", "Đất nông, lâm nghiệp": "dat-nong-lam-nghiep", "Các loại khác": "cac-loai-khac"}
}

class CrawlAloNhaDat:
    def __init__(self):
        self.driver = None
        self.dict_select_option_data = dict_select_option_data
        load_dotenv()

        #Main task config
        self.PAGE_URL = os.getenv("PAGE_URL")
        self.SLEEP_BEFOR_GO_NEXT_PAGE = os.getenv("SLEEP_BEFOR_GO_NEXT_PAGE")
        self.TIME_WAIT_PAGE_LOAD = os.getenv("TIME_WAIT_PAGE_LOAD")
        self.TIME_WAIT_GET_SUMMARY = os.getenv("TIME_WAIT_GET_SUMMARY")
        self.IS_GET_SUMMARY_DETAIL = os.getenv("IS_GET_SUMMARY_DETAIL").lower() == "true"
        self.TOTAL_PAGE_CRAWL = os.getenv("TOTAL_PAGE_CRAWL")

        #Email cònig
        self.message = ""
        self.SENDER_EMAIL = os.getenv("SENDER_EMAIL")
        self.APP_PASSWORD = os.getenv("APP_PASSWORD")
        self.RECEIVER_EMAIL = os.getenv("RECIEVER") 

        # File dir
        self.SAVE_DATA_DIR = os.getenv("SAVE_DATA_DIR")
        self.FILE_NAME  = os.getenv("FILE_NAME")

        self.data = []

    # Mo trinh duyet
    def start_crawl(self):
        self.driver = webdriver.Chrome()
        self.driver.get(self.PAGE_URL)
        time.sleep(int(self.TIME_WAIT_PAGE_LOAD))

    # Lay value cua option the select bang ten
    def get_value_by_key_name(self, selected_site, key_name):
        current_site_option = dict_select_option_data[selected_site]
        return current_site_option[key_name]

    # Chon option trong select tag bang gia tri
    def chose_option_by_element_value(self, options, value):
        for option in options:
            if option.get_attribute("value") == value:
                option.click()
                break
    
    # Chon option trong select tag bang gia tri text
    def chose_option_by_element_text(self, options, text):
        for option in options:
            if option.text == text:
                option.click()
                break
    
    # Chon select tag
    def click_selected_tag(self, xpath, chose_value, type_select):
        selected_tag = self.driver.find_element(By.XPATH, xpath)
        selected_tag.click()
        options_selected_tag = selected_tag.find_elements(By.TAG_NAME, 'option')
        if type_select == "value":
            self.chose_option_by_element_value(options=options_selected_tag, value=chose_value) 
        else:
            self.chose_option_by_element_text(options=options_selected_tag, text=chose_value)
        
    # Chon cac option de tim kiem
    def chose_type_data_to_find(self, province , property_type , 
                            type_post , direction , square , price, district ):
        # Chon tinh 
        if province != "":
            self.click_selected_tag('//*[@id="ctl00_content_pc_content"]/div[1]/div[1]/table/tbody/tr[3]/td[2]/select', 
                        self.get_value_by_key_name("province", province), type_select="value")

        # Loai nha
        if property_type != "":
            self.click_selected_tag('//*[@id="ctl00_content_pc_content"]/div[1]/div[1]/table/tbody/tr[2]/td[4]/select', 
                        self.get_value_by_key_name("property-type", property_type), type_select="value")

        # Loai bai dang
        if type_post != "":
            self.click_selected_tag('//*[@id="ctl00_content_pc_content"]/div[1]/div[1]/table/tbody/tr[2]/td[2]/select', 
                        self.get_value_by_key_name("post-type", type_post), type_select="value")

        #Phuong huong nha
        if direction != "":
            self.click_selected_tag('//*[@id="ctl00_content_pc_content"]/div[1]/div[1]/table/tbody/tr[4]/td[2]/select', 
                        self.get_value_by_key_name("direction", direction), type_select="value")

        #Dien tich
        if square != "":
            self.click_selected_tag('//*[@id="ctl00_content_pc_content"]/div[1]/div[1]/table/tbody/tr[5]/td[2]/select', 
                        self.get_value_by_key_name("square", square), type_select="value")

        #Muc gia 
        if price != "":
            self.click_selected_tag('//*[@id="ctl00_content_pc_content"]/div[1]/div[1]/table/tbody/tr[5]/td[4]/select', 
                        self.get_value_by_key_name("price", price), type_select="value")

        time.sleep(int(self.TIME_WAIT_PAGE_LOAD))
        #Chon Quan Huyen 
        if district != "":
            self.click_selected_tag('//*[@id="ctl00_content_pc_content"]/div[1]/div[1]/table/tbody/tr[3]/td[4]/select', 
                        district, type_select="text")
        
        button_seearch = self.driver.find_element(By.XPATH, '//*[@id="ctl00_content_pc_content"]/div[1]/div[1]/table/tbody/tr[6]/td/div/div[1]')
        button_seearch.click()
        time.sleep(int(self.TIME_WAIT_PAGE_LOAD))
    
    # Kiem tra mot phan tu co ton tai trong item khong
    def check_element_exist_in_item(self, item, find_method, elementClass):
        try:
            item.find_element(find_method, elementClass)
            return True
        except:
            return False

    # Lay mo ta cua bai dang bang BS4 
    def lay_mot_ta_chi_tiet(self, href_page , default_sum ):
        response = requests.get(href_page)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            content = soup.find('div', class_="detail text-content")
            try:
                return content.text
            except:
                return default_sum

    # Lay thong tin cac nha trong danh sach bai viet 
    def get_list_house_infor(self, list_post):
        if list_post == None:
            return
        for item in list_post:
            self.get_house_infor(item=item)

    # Lay thong tin bai viet cua cac nha trong trang  
    def get_house_infor_posts( self ):
        try:
            element_content_items = self.driver.find_elements(By.XPATH, '//*[@id="left"]/div[1]/div[*]')
            return element_content_items
        except:
            print("A Page have no post")
            return None
        
    #Lay thong tin nha cua bai dang
    def get_house_infor(self, item):
        try:
            element_title = item.find_element(By.CLASS_NAME, 'ct_title').text
            if self.IS_GET_SUMMARY_DETAIL:
                element_sum = self.lay_mot_ta_chi_tiet(item.find_element(By.TAG_NAME, 'a').get_attribute("href"),  item.find_element(By.CLASS_NAME, 'ct_brief').text)
                time.sleep(int(self.TIME_WAIT_GET_SUMMARY))
            else:
                element_sum = item.find_element(By.CLASS_NAME, 'ct_brief').text

            element_road = item.find_element(By.CLASS_NAME, 'road-width').text if self.check_element_exist_in_item(item, By.CLASS_NAME, 'road-width') else "Null"
            element_floor = item.find_element(By.CLASS_NAME, 'floors').text if self.check_element_exist_in_item(item, By.CLASS_NAME, 'floors') else "Null"
            element_bedroom = item.find_element(By.CLASS_NAME, 'bedroom').text if self.check_element_exist_in_item(item, By.CLASS_NAME, 'bedroom') else "Null"
            element_dientich = item.find_element(By.CLASS_NAME, 'ct_dt').text 
            element_gia = item.find_element(By.CLASS_NAME, 'ct_price').text
            element_vitri = item.find_element(By.CLASS_NAME, 'ct_dis').text

            nha_infor = [element_title, 
                        element_sum,
                        element_road, 
                        element_floor, 
                        element_bedroom,
                        element_dientich, 
                        element_gia, 
                        element_vitri]
            self.data.append(nha_infor)
        except:
            print("A item "+item+" invalid ")

    # Tien hanh cao du lieu 
    def crawl_data(self):
        try:
            i = 1
            isActive = True
            while isActive:
                self.get_list_house_infor(self.get_house_infor_posts())
                i = i + 1
                isActive = self.click_next_page(next_page=i)
                isActive = True if i != int(self.TOTAL_PAGE_CRAWL) else False
                time.sleep(int(self.SLEEP_BEFOR_GO_NEXT_PAGE))
            
        except:
            print("Crawl break by error")
            self.message += "\n Some error while crawl !!!"
        finally:
            self.message += "Carwl successfully which "+str(i)+" page \n"
            print("Crawl successfull")

    #Click next page function 
    def click_next_page(self, next_page):
        elements_page_btn = self.driver.find_elements(By.XPATH, f'//*[@id="left"]/div[2]/a')
        if len(elements_page_btn) == 0:
            return False
        else:
            for element in elements_page_btn:
                if element.text == str(next_page):
                    element.click()
                    return True
            return False
                
    # Luu thong tin crawl vao Excel         
    def save_data_to_excel(self):
        try:
            df = pd.DataFrame(self.data, columns=["title", "mo ta", "road", "floor", "bedroom", "dientich", "gia", "vitri"])
            today = date.today()
            df.to_excel(self.SAVE_DATA_DIR+self.FILE_NAME+"-"+str(today)+".xlsx")
            self.message = "Save data to excel successfull" + self.message
            return True   
        except:
            print("Error while save data")
            self.message = "Failed when save data to excel, please check file name config, file directory config !!!"
            return False

    # Auto send mail
    def send_mail_crawl_state(self):
            if self.SENDER_EMAIL != "" and self.APP_PASSWORD != "" and self.RECEIVER_EMAIL !="": 
                autoSendMail.send_email( sender=self.SENDER_EMAIL,
                                        subject= "Crawl_data AloNhaDat",
                                        body=self.message,
                                        password=self.APP_PASSWORD,
                                        receiver=self.RECEIVER_EMAIL)
    
    # Ket thuc crawl
    def end_task(self):
        self.driver.close()



