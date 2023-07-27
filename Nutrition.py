from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

BASE_URL = 'https://www.nutritionvalue.org/'


class Nutrition:
    def __init__(self):
        self.__driver = webdriver.Edge()
        self.__driver.get(BASE_URL)
        self.__action = ActionChains(self.__driver)
        self.__get_data()

    def __search_food(self):
        food_query = input("Enter the food to know nutrition facts.")
        self.__driver.find_element(By.CSS_SELECTOR, 'input#food_query').send_keys(food_query, Keys.RETURN)
        return self.__driver.find_elements(By.CSS_SELECTOR, "table td a.table_item_name")

    def __write(self, element_name):
        with open(f"{element_name}.txt", 'w') as file:
            details = self.__driver.find_element(By.ID, 'nutrition-label').text
            file.write(details)

    def food_menu(self, foods: webdriver):
        i = 1
        for food in foods:
            print(f'{i}) {food.text}')
            i += 1
        user_choice = int(input("choose from the menu: "))
        if user_choice not in range(len(foods)):
            user_choice = 1
        return foods[user_choice - 1]

    def __get_data(self):
        food_results = self.__search_food()
        element = self.food_menu(food_results)
        element_name = element.text
        element_link = element.get_attribute('href')
        self.__action.scroll_to_element(element).perform()
        sleep(3)
        # bypassing ElementClickInterceptedException
        self.__driver.execute_script('arguments[0].click();', element)
        # clicking somewhere to bypass the Ad
        self.__action.click().perform()
        self.__driver.implicitly_wait(5)
        self.__write(element_name)


nutrition = Nutrition()

