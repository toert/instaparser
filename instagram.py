# Built-In libs
import inspect
import pprint
import datetime
from time import sleep
# Third-party libs
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class InstagramParser():

    INSTAGRAM_URL = 'https://www.instagram.com/'
    IS_LOGGINED = False

    def __init__(self):
        #self.chrome = webdriver.Chrome()
        #self.safari = webdriver.Safari()
        # TODO support new drivers
        self.profile = webdriver.FirefoxProfile()
        self.firefox = webdriver.Firefox(firefox_profile=self.profile)

    def login(self, driver, login, password):
        driver.get(self.INSTAGRAM_URL)
        sleep(3)
        driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[2]/p/a').click()
        driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[1]/'
                                          'div/form/div[1]/div/input').send_keys(login)
        driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[1]/'
                                          'div/form/div[2]/div/input').send_keys(password)
        driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[1]/'
                                     'div/form/div[2]/div/input').send_keys(Keys.RETURN)
        self._log()
        self.take_screenshot(driver)
        sleep(3)

    def expore_tag(self, driver, tag):
        posts = {
            'popular': [],
            'new': []
        }
        driver.get('https://www.instagram.com/explore/tags/{}/'.format(tag))
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/section/main/article/div[1]/div')))
        best_photos_block = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[1]/div')
        for a in best_photos_block.find_elements_by_tag_name('a'):
            posts['popular'].append(a.get_attribute('href'))
        new_photos_block = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]')
        for a in new_photos_block.find_elements_by_tag_name('a'):
            posts['new'].append(a.get_attribute('href'))
        posts['new'] = posts['new'][:-1]
        self._log()
        self.take_screenshot(driver)
        return posts

    def like_post(self, driver, url):
        driver.get(url)
        like_button_section_xpath = '//*[@id="react-root"]/section/main/div/div/article/div[2]/section[1]'
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, like_button_section_xpath)))
        like_button_section = driver\
            .find_element_by_xpath(like_button_section_xpath)
        try:
            like_button_section.find_element_by_class_name('coreSpriteHeartOpen').click()
            self._log()
            self.take_screenshot(driver)
            return True
        except selenium.common.exceptions.NoSuchElementException:
            print('Even liked')
            self._log()
            self.take_screenshot(driver)
            return False

    def write_comment(self, driver, url, text):
        try:
            driver.get(url)
            comment_area_xpath = '//*[@id="react-root"]/section/main/div/div/article/div[2]/section[9]/form/textarea'
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, comment_area_xpath)))
            driver.find_element_by_xpath(comment_area_xpath).send_keys(text)
            driver.find_element_by_xpath(comment_area_xpath).send_keys(Keys.RETURN)
            self.take_screenshot(driver)
            self._log()
            return True
        except Exception as e:
            print(repr(e))
            self._log(repr(e))

    def close(self):
        self.firefox.quit()
        #self.chrome.quit()
        #self.safari.quit()

    @staticmethod
    def take_screenshot(driver):
        mask = '%d.%m.%y, %H:%M:%S'
        driver.save_screenshot('screenshots/{}.png'.format(datetime.datetime.now().strftime(mask)))
        print(datetime.datetime.now().strftime(mask))

    @staticmethod
    def _log(error=None):
        with open('log.txt', 'a', encoding='UTF-8') as file_handler:
            caller_name = inspect.stack()[1][3]
            error = 'Success' if error is None else error
            datetime_string = datetime.datetime.now().strftime('%d.%m-%H:%M:%S')
            file_handler.write('\n{}-{}-{}'.format(datetime_string, caller_name, error))


if __name__=='__main__':
    client = InstagramParser()
    driver = client.firefox
    client.login(driver, 'toert_', 'psswrd_here')
    pprint.pprint(client.expore_tag(driver, 'find'))
    client.like_post(driver, 'https://www.instagram.com/p/BY17uuSHAdC/')
    client.write_comment(driver, 'https://www.instagram.com/p/BY17uuSHAdC/', 'Amazing video')
    client.close()