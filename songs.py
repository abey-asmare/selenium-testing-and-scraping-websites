import os
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import *
from time import sleep
BASE_URL = 'https://soundcloud.com/discover/sets/charts-trending:all-music'
BASE_XPATH = '//*[@id="content"]/div/div/div[2]/div[1]/div/div[2]/ul/li'
RANK_XPATH = '/div[2]/span'
ARTIST_XPATH = '/div[3]/a[1]'
SONG_XPATH = '/div[3]/a[2]'

HEADER = ['rank', 'artist', 'song']


def write_data(filename: str, song: list):
    if not os.path.exists(f"{filename}.csv"):
        with open(f"{filename}.csv", 'w', newline='', encoding='UTF') as file:
            writer = csv.writer(file)
            writer.writerow(HEADER)

    with open(f"{filename}.csv", 'a', newline='', encoding='UTF8') as file:
            writer = csv.writer(file)
            writer.writerow(song)


class Music:
    def __init__(self, filename: str):
        self.__driver = webdriver.Edge()
        self.__driver.implicitly_wait(10)
        self.__driver.get(BASE_URL)
        self.__action = ActionChains(driver=self.__driver)
        self.__get_music(filename)

    def __get_music(self, filename: str):
        for i in range(1, 41):
            try:
                music = self.__driver.find_element(By.XPATH, f'{BASE_XPATH}[{i}]/div')
            except NoSuchElementException:
                print('error occured')
                continue

            self.__action.scroll_to_element(music).perform()
            details: list = self.get_details(music, i)
            write_data(filename, details)

    def get_details(self, element: WebElement, i: int):
        rank = element.find_element(By.XPATH, f'{BASE_XPATH}[{i}]/div{RANK_XPATH}').text.replace(",", "")
        artist = element.find_element(By.XPATH, f'{BASE_XPATH}[{i}]/div{ARTIST_XPATH}').text.replace(",", "")
        try:
            song_title = element.find_element(By.XPATH, f'{BASE_XPATH}[{i}]/div{SONG_XPATH}').text.replace(",", "")
        except NoSuchElementException:
            song_title = 'NaN'
        return [rank, artist, song_title]


music_data = Music("music")
