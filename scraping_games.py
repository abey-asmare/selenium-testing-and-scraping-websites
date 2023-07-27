from selenium import webdriver
from selenium.webdriver.common.by import By


CHROME_DRIVER_PATH = 'C:/Development/chromedriver.exe'
URL = 'https://steamdb.info/'
BASE_XPATH = '//*[@id="main"]/div[2]/div[1]/div'
BASE_XPATH2 = '//*[@id="main"]/div[2]/div[2]/div'


class Game:
    def __init__(self):
        self.__driver = webdriver.Chrome()
        self.__driver.get(url=URL)
        self.__get_all_data()

    def __get_all_data(self):
        most_played = self.__driver.find_element(By.XPATH, f"{BASE_XPATH}[1]").text
        trending = self.__driver.find_element(By.XPATH, f"{BASE_XPATH}[2]").text
        popular_release = self.__driver.find_element(By.XPATH, f"{BASE_XPATH2}[1]").text
        hot_release = self.__driver.find_element(By.XPATH, f"{BASE_XPATH2}[2]").text
        return most_played, trending, popular_release, hot_release

    def write_data(self, filename1, filename2, filename3, filename4):
        most_played, trending, popular_release, hot_release = self.__get_all_data()
        with open(filename1, 'w') as file:
            file.write(most_played)
        with open(filename2, 'w') as file:
            file.write(trending)
        with open(filename3, 'w',encoding='utf-16') as file:
            file.write(popular_release,)
        with open(filename4, 'w',encoding='utf-16') as file:
            file.write(hot_release)


game = Game()
game.write_data("most_played.txt", "trending.txt", "popular.txt", "hot.txt")
