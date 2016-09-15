import os
import unittest
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class GalaxyScaleContainers(unittest.TestCase):

  def __init__(self, testname, new_num_containers):
    super(GalaxyScaleContainers, self).__init__(testname)
    self.new_num_containers = new_num_containers

  def setUp(self):
    self.driver = webdriver.Chrome()
    self.GALAXY_USER = os.environ['GALAXY_USER']
    self.GALAXY_PASS = os.environ['GALAXY_PASS']
    self.GALAXY_URL = os.environ['GALAXY_URL']
    self.GALAXY_APP_DOMAIN = os.environ['GALAXY_APP_DOMAIN']

  def set_continers(self):
    driver = self.driver
    wait = WebDriverWait(driver, 20)

    driver.get(self.GALAXY_URL)
    wait.until(EC.visibility_of_element_located((By.NAME, "username")))
    email_elem = driver.find_element_by_name("username")
    email_elem.send_keys(self.GALAXY_USER)

    password_elem = driver.find_element_by_name("password")
    password_elem.send_keys(self.GALAXY_PASS)

    login_submit_elem = driver.find_element_by_css_selector("#render-target > span > div > div > div > form > button > span.rest")
    login_submit_elem.click()


    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#render-target > span > div > div.content-wrapper > span > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td.lower-column.primary > div > div:nth-child(2) > div > div:nth-child(1) > a")))

    driver.get(self.GALAXY_URL + "app/" + self.GALAXY_APP_DOMAIN)

    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.cardinal-number.editable > div > input[type=number]")))
    num_containers = driver.find_element_by_css_selector("div.cardinal-number.editable > div > input[type=number]")
    num_containers.send_keys(Keys.BACK_SPACE)
    num_containers.send_keys(Keys.BACK_SPACE)
    num_containers.send_keys(Keys.BACK_SPACE)
    num_containers.send_keys(Keys.BACK_SPACE)
    num_containers.send_keys(self.new_num_containers)
    num_containers.send_keys(Keys.RETURN)
    wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#render-target > span > div > div.content-wrapper > span > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td.lower-column.secondary > div > div.activity-list > div > span > div:nth-child(1) > div > div.description > span > span > em"), self.new_num_containers))

  def tearDown(self):
    self.driver.close()

if __name__ == "__main__":
  new_num_containers = sys.argv[1] #not the best way to do this, but for a quick and dirty script it works...
  suite = unittest.TestSuite()
  suite.addTest(GalaxyScaleContainers("set_continers", new_num_containers))

  unittest.TextTestRunner().run(suite)
