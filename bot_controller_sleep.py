from threading import Thread
from selenium import webdriver
from time import sleep
from datetime import datetime


class bot_on_thread(Thread):

    def __init__(self, url, browser, login, password, middle_name, cardNumber, cardExpiry, cardCvc, drop_time,
                 window_count):
        Thread.__init__(self)
        self.url = url
        self.login = login
        self.password = password
        self.middle_name = middle_name
        self.cardNumber = cardNumber
        self.cardExpiry = cardExpiry
        self.cardCvc = cardCvc
        self.browser = browser
        self.drop_time = drop_time
        self.window_count = window_count

    def run(self):

        if self.browser == "firefox":
            self.driver = webdriver.Firefox()
        elif self.browser == "chrome":
            self.driver = webdriver.Chrome()
        elif self.browser == "opera":
            self.driver = webdriver.Opera()
        else:
            return "Wrong type of browser"

        self.driver.get(self.url)
        for i in range(self.window_count):
            self.driver.execute_script(
                "window.open('" + self.url + "','Nike" + str(i) + "', 'resizable=yes');")

        sleep(self.window_count * 5)
        for i in range(self.window_count):
            self.driver.switch_to.window(self.driver.window_handles[i])
            element = self.driver.find_elements_by_name("emailAddress")
            element[0].send_keys(self.login[i])
            self.driver.find_element_by_name("password").send_keys(self.password[i])
            self.driver.find_element_by_class_name("nike-unite-component.nike-unite-submit-button").click()
            el_test = self.driver.find_elements_by_id("middleName")
            while len(el_test) != 1:
                sleep(4)
                element = self.driver.find_elements_by_class_name("nike-unite-error-close")
                if len(element) != 0:
                    element[0].click()
                    self.driver.find_element_by_name("password").send_keys(self.password[i])
                    self.driver.find_element_by_class_name("nike-unite-component.nike-unite-submit-button").click()

                el_test = self.driver.find_elements_by_id("middleName")

            sleep(10)
            element = self.driver.find_elements_by_id("middleName")
            element[0].send_keys(self.middle_name[i])
            element = self.driver.find_elements_by_xpath(
                "//button[@class='button-continue'][.='Сохранить и продолжить']")
            while len(element) != 0:
                element[0].click()
                element = self.driver.find_elements_by_xpath(
                    "//button[@class='button-continue'][.='Сохранить и продолжить']")
            sleep(1)
            element = self.driver.find_elements_by_class_name("stored-card-text")
            if len(element) != 0:
                iframeSwitch = self.driver.find_element_by_class_name("cvv")
                self.driver.switch_to.frame(iframeSwitch)
                self.driver.find_element_by_id("cardCvc-input").send_keys(self.cardCvc[i])
            else:
                iframeSwitch = self.driver.find_element_by_class_name("newCard")
                self.driver.switch_to.frame(iframeSwitch)
                self.driver.find_element_by_id("cardNumber-input").send_keys(self.cardNumber[i])
                self.driver.find_element_by_id("cardExpiry-input").send_keys(self.cardExpiry[i])
                self.driver.find_element_by_id("cardCvc-input").send_keys(self.cardCvc[i])
            self.driver.switch_to.parent_frame()

            element = self.driver.find_elements_by_xpath("//button[@class='button-continue'][.=' Продолжить ']")
            sleep(5)
            element[0].click()

        element = self.driver.find_elements_by_xpath("//button[@class='button-submit'][.=' Отправить заказ ']")
        wait_time = self.drop_time - int(datetime.now().timestamp())
        if wait_time < 0:
            wait_time = 0
        sleep(wait_time)
        for i in range(self.window_count):
            self.driver.switch_to.window(self.driver.window_handles[i])
            while len(element) != 0:
                try:
                    element[0].click()
                except:
                    break
                element = self.driver.find_elements_by_xpath("//button[@class='button-submit'][.=' Отправить заказ ']")

    def close_browser(self):
        self.driver.close()

    def __del__(self):
        print('Destructor called, thread deleted.')
