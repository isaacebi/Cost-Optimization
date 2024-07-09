from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np


class SeleniumGoogleMap:
    def __init__(self, coordinates) -> None:
        self.coordinates = coordinates
        self.browser = webdriver.Firefox()

        #######################
        ### Hardcoded XPATH ###
        #######################

        # Direction button
        self.DXPATH = "//html/body/div[1]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[4]/div[1]/button"

        # Start location input
        self.SXPATH = "//html/body/div[1]/div[3]/div[8]/div[3]/div[1]/div[2]/div/div[3]/div[1]/div[1]/div[2]/div[1]/div/input"

        # End location input
        self.EXPATH = "//html/body/div[1]/div[3]/div[8]/div[3]/div[1]/div[2]/div/div[3]/div[1]/div[2]/div[2]/div[1]/div/input"

        # Driving button
        self.DRIVING = "//html/body/div[1]/div[3]/div[8]/div[3]/div[1]/div[2]/div/div[2]/div/div/div/div[2]/button"

        # Distance class name
        self.DISTANCE = "//*[@class='ivN21e tUEI8e fontBodyMedium']"


    def open_map(self, url='https://www.google.com/maps'):
        self.browser.get(url)
        assert 'Google Maps' in self.browser.title

    def wait_selector(self, selector):
        for retry in range(5):
            element = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.XPATH, selector))
            )
        return True
    

    def initial_location(self, location="Tanjung Aru"):
        # Find the search box
        element = self.browser.find_element(By.NAME, 'q')
        element.send_keys(location + Keys.RETURN)

    def initiate_direction(self):
        print("Locating 'Direction' button ...")
        if self.wait_selector(self.DXPATH):
            print("'Direction' button located and proceed with clicking")
            direction = self.browser.find_element(By.XPATH, self.DXPATH)
            direction.click()

        else:
            print("'Direction' button not located, please recheck the hardcoded XPATH selector")

    
    def get_direction(self, start="Tanjung Aru", end="Kundasang"):
        if self.wait_selector(self.SXPATH) and self.wait_selector(self.EXPATH):
            slocation = self.browser.find_element(By.XPATH, self.SXPATH)
            slocation.send_keys(start)

            elocation = self.browser.find_element(By.XPATH, self.EXPATH)
            elocation.send_keys(end + Keys.RETURN)

            # filter only driving route
            if self.wait_selector(self.DRIVING):
                driving = self.browser.find_element(By.XPATH, self.DRIVING)
                driving.click()

        else:
            print("Please check the start and end location XPATH selector")

    def get_distance(self):
        results = []
        if self.wait_selector(self.DISTANCE):
            distances = self.browser.find_elements(By.XPATH, self.DISTANCE)

            for distance in distances:
                results.append(distance.text)

            return np.array(results)

        else:
            print("There are no valid distance, please check the distance XPATH/class_name")

    
    


if __name__ == "__main__":
    browser = SeleniumGoogleMap(coordinates='1234')
    browser.open_map()
    browser.initial_location()
    browser.initiate_direction()
    browser.get_direction()
    browser.get_distance()