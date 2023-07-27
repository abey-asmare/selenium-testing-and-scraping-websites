from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd

CHROME_DRIVER_PATH = 'C:/Development/chromedriver.exe'
URL = 'https://www.audible.com/search?feature_six_browse-bin=18685580011&keywords=book' \
             '&node=18573211011&pageSize=50&ref=a_search_c4_pageSize_3&pf_rd_p=1d79b443-2f1d-' \
             '43a3-b1dc-31a2cd242566&pf_rd_r=931EGPJG0B97THRK6GQA&pageLoadId=VRkHF8I22aNIccp3' \
             '&creativeId=18cc2d83-2aa9-46ca-8a02-1d1cc7052e2a'


class Audible:
    def __init__(self, path: str, url: str):
        self.__base_xpath = '//*[@id="center-3"]/div/div/div/span[2]/ul/li'
        self.__url = url
        service = Service(executable_path=path)
        self.__driver = webdriver.Chrome(service=service)
        self.__driver.get(url=self.__url)
        self.__books = self.__get_data()

    def __get_data(self):
        return [self.__driver.find_element(By.XPATH, f"{self.__base_xpath}[{i}]/div").text.split("\n")[1:-1] for i in
                range(1, 51)]

    def __clean_data(self) -> list:
        clean_books = []
        for book in self.__books:
            new_book = []
            for data in book:
                if " rating" not in data.lower() \
                        and "plus membership" not in data.lower():
                    if ":" in data:
                        data = data.split(":")[1]
                    if "," in data:
                        data = data.replace(",", "")
                    new_book.append(data)
            clean_books.append(new_book)
        for book in clean_books:
            if len(book) < 9:
                book.insert(1, "No Description")
            elif len(book) > 9:
                clean_books.remove(book)
        return clean_books

    def write_on_file(self, file_name: str):
        all_books = self.__clean_data()
        for books in all_books:
            print(books)
            print(len(books))
        with open(file_name, 'w') as file:
            file.write("Book Title, Book Description, By, Narrated By, Duration, Release Date, Length, Language, Current Price\n")
            for book in all_books:
                for data in book:
                    if data in book[:-1]:
                        file.write(f"{data},")
                    else:
                        file.write(data)
                file.write('\n')


audible = Audible(CHROME_DRIVER_PATH, URL)
audible.write_on_file("audible.csv")
