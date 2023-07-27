from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import *
from time import sleep

# 4-63

CHROME_DRIVER_PATH = 'C:/Development/chromedriver.exe'
URL = 'https://www.allrecipes.com/recipes/201/meat-and-poultry/chicken/'
BASE_XPATH = '//*[@id="mntl-card-list-items_2-0-'


class Recipe:
    def __init__(self):
        self.__driver = webdriver.Edge()
        self.__action = ActionChains(self.__driver)
        self.__driver.get(URL)
        self.__get_all_data()

    def __get_all_data(self):
        for i in range(4, 64):
            try:
                element = self.__driver.find_element(By.XPATH, f'{BASE_XPATH}{i}"]')
            except NoSuchElementException:
                continue
            except StaleElementReferenceException:
                continue
            # move to that specific element
            self.__driver.implicitly_wait(5)
            self.__action.move_to_element(element).perform()
            # click and open that element in new window
            element.send_keys(Keys.CONTROL, Keys.RETURN)
            # get window handles(st from the first window gets 0)
            window_handles = self.__driver.window_handles
            # switch to the second window (the second index: 1)
            self.__driver.switch_to.window(window_handles[1])
            self.__get_recipe_info()
            sleep(10)
            # close the current window
            self.__driver.close()
            # switch back to first window(index: 0)
            self.__driver.switch_to.window(window_handles[0])
            sleep(5)

    def __get_recipe_info(self):
        try:
            name_xpath = '//*[@id="article-heading_1-0"]'
            name_element = self.__driver.find_element(By.XPATH, name_xpath)
            name = name_element.text
        except:
            name = "No name provided"
        try:
            discription = '//*[@id="article-subheading_1-0"]'
            description_element = self.__driver.find_element(By.XPATH, discription)
            description = description_element.text
        except:
            description = "no description Provided"

        try:
            img_xpath = '//*[@id="mntl-sc-block-image_1-0-1"]'
            img_element = self.__driver.find_element(By.XPATH, img_xpath)
            self.__action.move_to_element(img_element).perform()
            self.__driver.implicitly_wait(5)
            img = img_element.get_attribute('src')
        except NoSuchElementException:
            img = "No Image Provided."

        try:
            ingredients_xpath = '//*[@id="mntl-structured-ingredients_1-0"]'
            ingredients_element = self.__driver.find_element(By.XPATH, ingredients_xpath)
            ingredients = ingredients_element.text
        except NoSuchElementException:
            ingredients = "No ingredients provided"

        try:
            directions_xpath = '//*[@id="recipe__steps_1-0"]'
            directions_element = self.__driver.find_element(By.XPATH, directions_xpath)
            directions = directions_element.text
        except:
            directions = "No directions provided"

        def write_data():
            with open(f'{name.replace(" ", "_")}.txt', 'w', encoding='utf-8') as file:
                file.write(f"{name}\n\n")
                file.write(f"{description}\n\n")
                file.write(f"see image here: {img}\n\n")
                file.write(f"\n{ingredients}\n\n")
                file.write(f"\n{directions}\n\n")

        write_data()


recipe = Recipe()
