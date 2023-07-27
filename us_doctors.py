from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import *
import csv
import os

BASE_URL = 'https://health.usnews.com/doctors/idaho'
BASE_XPATH = '//*[@id="app"]/article/div/div[4]/div[2]/div[1]/ol/li'
NAME_XPATH = '/div[1]/div[2]/div/a[1]/h2'
SPECIALIZATION_XPATH = '/div[1]/div[2]/p[1]'
SUB_SPECIALIZATION_XPATH = '/div[1]/div[2]/p[2]'
LOCATION_XPATH = '/div[1]/div[2]/p[3]'
WORKS_IN_XPATH = '/div[1]/div[2]/p[4]'
IMG_XPATH = '/div[1]/div[1]/picture/img'
HEADER = ['Name', 'Specialization', 'Specialization', 'img', 'works in', 'location']


class Doctor:
    def __init__(self):
        self.__driver = webdriver.Edge()
        self.__driver.get(BASE_URL)
        self.__action = ActionChains(self.__driver)

    def __write(self, filename: str, doctor: list):
        if os.path.exists(f"{filename}.csv"):
            with open(f"{filename}.csv", 'a', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(doctor)
        else:
            with open(f"{filename}.csv", 'w', newline="") as f:
                writer = csv.writer(f)
                writer.writerow(HEADER)

    def __find_doctor(self, element_xpath) -> list:
        doctor = self.__driver.find_element(By.XPATH, element_xpath)
        self.__action.scroll_to_element(doctor).perform()
        self.__driver.implicitly_wait(5)
        name = doctor.find_element(By.XPATH, f'{element_xpath}{NAME_XPATH}').text
        specialization = doctor.find_element(By.XPATH, f"{element_xpath}{SPECIALIZATION_XPATH}").text
        sub_specialization = doctor.find_element(By.XPATH,
                                                 f"{element_xpath}{SUB_SPECIALIZATION_XPATH}").text.replace(",", "")
        try:
            location = doctor.find_element(By.XPATH,
                                           f"{element_xpath}{LOCATION_XPATH}").text.replace(",", "")
        except NoSuchElementException:
            location = "no location provided"

        try:
            works_in = doctor.find_element(By.XPATH,
                                           f"{element_xpath}{WORKS_IN_XPATH}").text.replace(",", "")
        except NoSuchElementException:
            works_in = "No work history provided"

        try:
            img = doctor.find_element(By.XPATH,
                                      f"{element_xpath}{IMG_XPATH}").get_attribute('src').replace(",", "")
        except:
            img = "No img provided"

        return [
            name,
            specialization,
            sub_specialization,
            img,
            works_in,
            location,
        ]

    def get_data(self, filename: str):
        for i in range(1, 20):
            try:
                element_xpath = f"{BASE_XPATH}[{i}]/div/div/div[1]"
                new_dict = self.__find_doctor(element_xpath=element_xpath)
                self.__write(filename, new_dict)
            except NoSuchElementException:
                print("error occured")


doctor = Doctor()
doctor.get_data('doctors')
