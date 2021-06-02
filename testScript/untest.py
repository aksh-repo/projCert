import unittest
from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import subprocess
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

class TestPhpWebsite(unittest.TestCase):
    def test_php(self):
        dockerstop = "docker stop phpcontainer"
        dockerremove = "docker rm phpcontainer"
        actual_text = self.seltest()
        print("Actual text is:")
        print(actual_text)
        print('\n')
        readFile = open("phpapp.txt", 'r')
        expected_text = readFile.read()
        readFile.close()
        print("Expected text is:")
        print(expected_text)
        if (expected_text != actual_text):
            subprocess.call(dockerstop, shell=True)
            subprocess.call(dockerremove, shell=True)
        assert True
        self.assertEqual(actual_text,expected_text,msg="Actual and expected text does not match, hence stopping and removing container from Test Server")
        print("\n")
        print("Actual and Expected text is Matching. Testing is success. Hence deploying the container to Prod Server...")

    def seltest(self):
        driver = webdriver.Chrome(executable_path='/usr/lib64/chromium-browser/chromedriver',chrome_options=chrome_options)
        url = "http://34.122.73.52:8080/"
        try:
            driver.get(url)
            driver.maximize_window()
            about_text1 = ''
            about_text2 = ''
            about_text = ''
            try:
                # Navigating to About Us
                driver.find_element_by_xpath("//a[@id = 'About Us']").click()
                time.sleep(5)
                # Fetching the text
                about_text1 = driver.find_element_by_xpath("//p[@id = 'PID-ab2-pg']").text
                about_text2 = driver.find_element_by_xpath("//p[@id = 'PID-ab2-pg']//following::p").text
            except NoSuchElementException:
                print("Element not found")
            about_text = about_text1 + "\n" + "\n"  + about_text2
        except Exception as e:
            print("Exception occured <> {}".format(str(e)))
        driver.close()
        return about_text

if __name__ == '__main__':
    unittest.main()