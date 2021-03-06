__author__ = 'cloverchio'

"""
Simple selenium regression suite for the UI.
To keep things simple for now, this suite uses a local instance of the FireFox
driver and is not ran on the grid.

https://github.com/cloverchio

"""

from decouple import config
from selenium import webdriver
from unittest import TestCase

url = config('LOCAL_URL', default='http://localhost:5000/')


class TestValidInput(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox()
        cls.driver.get(url)

    def test_valid_input(self):
        search_bar = self.driver.find_element_by_id('s')
        search_bar.clear()
        search_bar.send_keys("Aberlour")
        search_bar.submit()
        self.driver.implicitly_wait(20)
        xpath = "/html/body/div[1]/div[2]/div[2]"
        search_result = self.driver.find_element_by_xpath(xpath)
        self.assertTrue(search_result.size > 0)
        self.assertFalse(search_result.size <= 0)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


class TestInvalidInput(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox()
        cls.driver.get(url)

    def test_invalid_input(self):
        search_bar = self.driver.find_element_by_id('s')
        search_bar.clear()
        search_bar.send_keys(" ")
        search_bar.submit()
        self.driver.implicitly_wait(20)
        page_content = self.driver.page_source
        no_results_text = "Sorry, no whisky found"
        self.assertTrue(no_results_text in page_content)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


class TestRecommendSearch(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox()
        cls.driver.get(url)

    def test_option_list(self):
        search_bar = self.driver.find_element_by_id('s')
        search_bar.clear()
        search_bar.send_keys(" ")
        self.driver.implicitly_wait(20)
        xpath_1 = "/html/body/div[2]/div[5]"
        list_option = self.driver.find_element_by_xpath(xpath_1)
        list_option.click()
        search_bar.submit()
        self.driver.implicitly_wait(20)
        xpath_2 = "/html/body/div[1]/div[2]/div[2]"
        search_result = self.driver.find_element_by_xpath(xpath_2)
        self.assertTrue(search_result.size > 0)
        self.assertFalse(search_result.size <= 0)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
