from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

CHROME_DRIVER_PATH = 'C:/Development/chromedriver.exe'

class Nba:
    def __init__(self, path: str):
        self.__base_xpath = '//*[@id="__next"]/div[2]/div[2]/div[3]/div/div[1]/section[1]/div/div[4]/div'
        self.__element = None
        self.__result = ""
        service = Service(executable_path=path)
        self.__driver = webdriver.Chrome(service=service)
        self.__driver.get(url='https://www.nba.com/stats')

    def get_seasonal_data(self):
        for i in range(1, 10):
            self.__element = self.__driver.find_element(By.XPATH, f'{self.__base_xpath}[{i}]')
            self.__result += f"{self.__element.text}\n\n"
        with open("nba_stat_records.txt", 'w') as file:
            file.write(self.__result)


nba = Nba(CHROME_DRIVER_PATH)
nba.get_seasonal_data()