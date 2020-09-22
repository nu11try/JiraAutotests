from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from utils import Config
import time


class Jira:

    def __init__(self):
        self.config = Config.Config()
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--no-sandbox')
        # chrome_options.add_argument('--window-size=1420,1080')
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)

    def __wait_el(self, element, type):
        if type == "xpath":
            WebDriverWait(self.driver, 500).until(
                lambda driver: driver.find_element_by_xpath(element))
        elif type == "css":
            WebDriverWait(self.driver, 500).until(
                lambda driver: driver.find_element_by_css_selector(element))

    def __wait_time(self, time):
        self.driver.implicitly_wait(time)

    '''
        АВТОРИЗАЦИЯ ПОЛЬЗОВАТЕЛЯ
    '''

    def __auth(self):
        self.driver.get("https://job-jira.otr.ru/login.jsp")

        while True:
            try:
                self.driver.find_element_by_id("login-form-username")
                break
            except:
                time.sleep(1)

        self.driver.find_element_by_id("login-form-username").send_keys(self.config.get_config("auth", "login"))
        self.driver.find_element_by_id("login-form-password").send_keys(self.config.get_config("auth", "password"))

        self.driver.find_element_by_id("login-form-submit").click()

    '''
        ПОЛУЧЕНИЕ ССЫЛКИ АКТИВНОГО ПРОГОНА
    '''

    def __get_link_active_packs(self, id):
        # выбор необходимого модулу
        self.__select_needed_module("packs")
        # выбор студии в дереве
        self.__select_studio()
        # открытие фильтра
        self.__open_filter()

        self.__search_needed_pack(id)
        time.sleep(2)

        # установка значения в фильтре
        # self.select_field_filter("Assigned to", "Зуев Владислав Борисович")
        # получение ссылки активного прогона
        buf_key = self.driver.find_element_by_xpath(
            '//*[@id="content"]/div/div/div/div/div/div[2]/div[3]/refresher/grid/span/table/tbody/tr/td[2]/a')
        buf_name = self.driver.find_element_by_xpath(
            '//*[@id="content"]/div/div/div/div/div/div[2]/div[3]/refresher/grid/span/table/tbody/tr/td[3]/a/span')
        return self.config.get_config("url", "link_pack") + buf_key.text

    '''
        ФУНКЦИЯ ОТКРЫТИЯ ФИЛЬТРА
    '''

    def __open_filter(self):
        self.__wait_el(
            '//*[@id="ktm-toggle-filters"]',
            "xpath")
        self.driver.find_element_by_xpath('//*[@id="ktm-toggle-filters"]').click()

    '''
        ФУНКЦИЯ ОТКРЫТИЯ НАБОРА
    '''

    def __open_pack(self, link):
        self.driver.get(link)

    '''
        ВЫБОР ФИЛЬТРА И УСТАНОВКА В НЕГО ЗНАЧЕНИЯ
    '''

    def __select_field_filter(self, field, text):
        if field == "Все":
            self.driver.find_elements_by_xpath(
                '//*[@id="content"]/div/div/div/div/div/div[2]/div[1]/div/div[2]/div/filter-button[1]/button').click()
            self.driver.find_elements_by_xpath('//*[@id="ktm-uid-1"]/div/div[1]/div/input').send_keys(text)
            self.driver.find_elements_by_xpath('//*[@id="ktm-uid-1"]/div/div[2]/ul/li/a').click()
        elif field == "Итерации":
            self.driver.find_elements_by_xpath(
                '//*[@id="content"]/div/div/div/div/div/div[2]/div[1]/div/div[2]/div/filter-button[2]/button').click()
            self.driver.find_elements_by_xpath('//*[@id="ktm-uid-4"]/div/div[1]/div/input').send_keys(text)
            self.driver.find_elements_by_xpath('//*[@id="ktm-uid-4"]/div/div[2]/ul/li/a').click()
        elif field == "План тестирования":
            self.driver.find_elements_by_xpath(
                '//*[@id="content"]/div/div/div/div/div/div[2]/div[1]/div/div[2]/div/filter-button[3]/button').click()
            self.driver.find_elements_by_xpath('//*[@id="ktm-uid-2"]/div/div[1]/div/input').send_keys(text)
            self.driver.find_elements_by_xpath('//*[@id="ktm-uid-2"]/div/div[2]/ul/li/a').click()
        elif field == "Assigned to":
            self.driver.find_elements_by_xpath(
                '//*[@id="content"]/div/div/div/div/div/div[2]/div[1]/div/div[2]/div/user-filter-button/button').click()
            self.driver.find_elements_by_xpath('//*[@id="ktm-uid-5"]/div[1]/div/input').send_keys(text)
            self.driver.find_elements_by_xpath('//*[@id="ktm-uid-5"]/div/div[2]/ul/li/a').click()
        elif field == "Статусы":
            self.driver.find_element_by_xpath(
                '//*[@id="content"]/div/div/div/div/div/div[2]/div[1]/div/div[2]/div/filter-button[4]/button').click()
            self.driver.find_element_by_xpath('//*[@id="ktm-uid-3"]/div/div[1]/div/input').send_keys(text)
            self.driver.find_element_by_xpath('//*[@id="ktm-uid-3"]/div/div[2]/ul/li/a').click()
        time.sleep(3)

    '''
        ВЫБОР СТУДИИ В ЛЕВОМ ДЕРЕВЕ
    '''

    def __select_studio(self):
        self.__wait_el(
            '//*[@id="content"]/div/div/div/div/div/div[2]/div[3]/refresher/grid/span/table/thead/tr/th[4]/span',
            "xpath")
        self.__wait_el(
            '//*[@id="ktm-library-folder-tree"]/folder-tree/div/div/ol/li[2]/div/div/span[3]',
            "xpath")
        self.driver.find_element_by_xpath(
            '//*[@id="ktm-library-folder-tree"]/folder-tree/div/div/ol/li[2]/div/div/span[3]').click()

    '''
        ВЫБОР НЕОБХОДИМОГО МОДУЛЯ
        @ТЕСТЫ ПРОГОНЫ ОТЧЕТЫ ПЛАНЫ@    
    '''

    def __select_needed_module(self, module):
        self.driver.get(self.config.get_config("url", module))

    '''
        УСТАНОВКА НЕОБХОДИМОГО СТАТУСА ТЕСТА
        @В РАБОТЕ ПРОЙДЕН ПРОВАЛЕН БЛОКИРОВАН@
    '''

    def __select_status_test_in_pack(self, status, test_id):
        self.__wait_el(
            '//*[@id="content"]/div/div/div/div[1]/div[1]/div[2]/div/div[1]/div/div[1]/div/div[2]/span/span[1]',
            "xpath"
        )
        while True:
            if self.driver.find_element_by_xpath('//*[@id="content"]/div/div/div/div[1]/div[1]/div[2]/div/div[1]/div/div[1]/div/div[1]/h2/a').text.split(" ")[0] == test_id:
                self.driver.find_element_by_xpath(
                    '//*[@id="content"]/div/div/div/div[1]/div[1]/div[2]/div/div[1]/div/div[1]/div/div[2]/span/span[1]').click()
                status_id = self.config.get_config("status", status)
                self.driver.find_element_by_css_selector(
                    'aui-dropdown2-section > ul > aui-dropdown2-item:nth-child(' + status_id + ') > li > a').click()
                break
            else:
                self.__wait_time(3)
        self.__wait_time(5)

    '''
        УСТАНОВКА ВРЕМЯ ПРОГОНА ТЕСТА
    '''

    def __set_time_test_in_pack(self, time):
        self.__wait_el(
            '//*[@id="content"]/div/div/div/div[1]/div[1]/div[2]/div/div[1]/div/div[1]/div/div[2]/div/button[2]',
            "xpath"
        )
        self.driver.find_element_by_xpath(
            '//*[@id="content"]/div/div/div/div[1]/div[1]/div[2]/div/div[1]/div/div[1]/div/div[2]/div/button[2]').click()
        self.driver.find_element_by_css_selector('form[name="testPlayerTimeForm"] > div > input').send_keys(time)
        self.driver.find_element_by_css_selector('form[name="testPlayerTimeForm"] > div > button').click()
        self.__wait_time(5)

    '''
        ПОИСК НЕОБХОДИМОГО НАБОРА
    '''

    def __search_needed_pack(self, id):
        self.__wait_el(
            '//*[@id="content"]/div/div/div/div/div/div[2]/div[1]/div/div[1]/div/div[2]/div[1]/input',
            "xpath")
        self.driver.find_element_by_xpath(
            '//*[@id="content"]/div/div/div/div/div/div[2]/div[1]/div/div[1]/div/div[2]/div[1]/input').send_keys(id)

    '''
        ПОИСК НЕОБХОДИМОГО ТЕСТА В НАБОРЕ
    '''

    def __search_needed_test_in_pack(self, id):
        self.__wait_el(
            '//*[@id="ktm-test-player-scope"]/div[1]/div[1]/div/div',
            "xpath")
        self.driver.find_element_by_xpath('//*[@id="ktm-test-player-scope"]/div[1]/div[1]/div/div').click()
        self.driver.find_element_by_xpath('//*[@id="ktm-test-player-scope"]/div[1]/div[1]/div/div/input').send_keys(id)
        self.__wait_el(
            '//*[@id="ktm-test-player-scope"]/div[1]/div[2]/ol/li/ol/li/div/div[2]',
            "xpath")
        self.driver.find_element_by_xpath(
            '//*[@id="ktm-test-player-scope"]/div[1]/div[2]/ol/li/ol/li/div/div[2]').click()
        self.__wait_time(5)

    '''
        ГЛАВНЫЙ МЕТОД ВЫПОЛНЕНИЯ
    '''

    def exec(self, data):
        self.__auth()
        link = self.__get_link_active_packs(self.config.get_config("pack", "pack"))
        self.__open_pack(link)

        tests_ar = data["tests"]
        results_ar = data["results"]
        times_ar = data["times"]

        if len(tests_ar) != len(results_ar) or len(tests_ar) != len(times_ar):
            return "ERROR_LEN"
        else:
            buf = 0
            while True:
                if buf != len(tests_ar):
                    self.__search_needed_test_in_pack(tests_ar[buf])
                    self.__select_status_test_in_pack(results_ar[buf], tests_ar[buf])
                    self.__set_time_test_in_pack(times_ar[buf])
                    self.driver.refresh()
                    buf += 1
                else:
                    break
