from selenium import webdriver
from selenium.webdriver.common.by import By

ROLLER_COASTER_XPATH = '//*[@id="rrc"]'


class RollerCoaster:
    def __init__(self):
        self.__driver = webdriver.Chrome()
        self.__driver.get('https://rcdb.com/')

    def __get_roller_coaster(self):
        roller_coaster = self.__driver.find_element(By.XPATH, ROLLER_COASTER_XPATH).text.replace(
            "Random Roller Coaster", "")
        roller_coaster_img = self.__driver.find_element(By.CSS_SELECTOR, "#rrc a#rrc_pic").get_attribute('href')
        return roller_coaster, roller_coaster_img

    def __write_data(
            self,
            filename,
            roller_coaster: str,
            roller_coaster_img: str
    ):
        try:
            file = open(f'{filename}.txt', 'r', encoding='utf-8')
            file_read = file.read()
            file.close()
        except FileNotFoundError:
            file = open(f'{filename}.txt', 'x', encoding='utf-8')
            file_read = file.read()
            file.close()
        if roller_coaster in file_read \
                and roller_coaster_img in file_read:
            print("roller coaster exists")
        else:
            with open(f"{filename}.txt", 'a', encoding='utf-8') as file:
                file.write(f"{roller_coaster}\n")
                file.write(f"See Image Here: {roller_coaster_img}\n\n")
                file.write("---------------------------------------\n")

    def __refresh_webpage(self):
        self.__driver.implicitly_wait(3)
        self.__driver.refresh()
        self.__driver.implicitly_wait(3)

    def get_many_roller_coasters(self, amount, filename):
        for i in range(amount):
            roller_coaster, roller_coaster_img = self.__get_roller_coaster()
            self.__write_data(
                filename,
                roller_coaster=roller_coaster,
                roller_coaster_img=roller_coaster_img
            )
            self.__refresh_webpage()


roller = RollerCoaster()
roller.get_many_roller_coasters(150, "roller_coaster")
