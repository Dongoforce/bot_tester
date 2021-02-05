from threading import Thread
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from time import sleep
from datetime import datetime
from webdriver_manager import chrome, firefox


class bot_on_thread(Thread):

    def __init__(self, url, browser, login, password, middle_name, cardNumber, cardExpiry, cardCvc, drop_time):
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
        # self.proxy = proxy

    def run(self):

        if self.browser == "firefox":
            # webdriver.DesiredCapabilities.FIREFOX['proxy'] = {
            #     "httpProxy": self.proxy,
            #     "ftpProxy": self.proxy,
            #     "sslProxy": self.proxy,
            #
            #     "proxyType": "MANUAL",
            #
            # }
            options = Options()
            options.headless = True
            self.driver = webdriver.Firefox(options=options)
        elif self.browser == "chrome":
            self.driver = webdriver.Chrome(chrome.ChromeDriverManager().install())
        elif self.browser == "opera":
            self.driver = webdriver.Opera()
        else:
            return "Wrong type of browser"
        # self.driver.get('https://www.expressvpn.com/what-is-my-ip')
        self.driver.get(self.url)
        sleep(14)
        element = self.driver.find_elements_by_name("emailAddress")
        while len(element) == 0:
            element = self.driver.find_elements_by_name("emailAddress")
        element[0].send_keys(self.login)
        self.driver.find_element_by_name("password").send_keys(self.password)
        self.driver.find_element_by_class_name("nike-unite-component.nike-unite-submit-button").click()
        el_test = self.driver.find_elements_by_id("middleName")
        while len(el_test) != 1:
            sleep(2)
            element = self.driver.find_elements_by_class_name("nike-unite-error-close")
            if len(element) != 0:
                element[0].click()
                self.driver.find_element_by_name("password").send_keys(self.password)
                self.driver.find_element_by_class_name("nike-unite-component.nike-unite-submit-button").click()

            el_test = self.driver.find_elements_by_id("middleName")

        element = self.driver.find_elements_by_id("middleName")
        while len(element) != 1:
            element = self.driver.find_elements_by_id("middleName")
        element[0].send_keys(self.middle_name)
        element = self.driver.find_elements_by_xpath("//button[@class='button-continue'][.='Сохранить и продолжить']")
        while len(element) != 0:
            element[0].click()
            element = self.driver.find_elements_by_xpath("//button[@class='button-continue'][.='Сохранить и продолжить']")
        sleep(1)
        element = self.driver.find_elements_by_class_name("stored-card-text")
        if len(element) != 0:
            iframeSwitch = self.driver.find_element_by_class_name("cvv")
            self.driver.switch_to.frame(iframeSwitch)
            self.driver.find_element_by_id("cardCvc-input").send_keys(self.cardCvc)
        else:
            iframeSwitch = self.driver.find_element_by_class_name("newCard")
            self.driver.switch_to.frame(iframeSwitch)
            self.driver.find_element_by_id("cardNumber-input").send_keys(self.cardNumber)
            self.driver.find_element_by_id("cardExpiry-input").send_keys(self.cardExpiry)
            self.driver.find_element_by_id("cardCvc-input").send_keys(self.cardCvc)
        self.driver.switch_to.parent_frame()

        element = self.driver.find_elements_by_xpath("//button[@class='button-continue'][.=' Продолжить ']")
        while len(element) != 0:
            try:
                element[0].click()
            except:
                break
            element = self.driver.find_elements_by_xpath("//button[@class='button-continue'][.=' Продолжить ']")

        element = self.driver.find_elements_by_xpath("//button[@class='button-submit'][.=' Отправить заказ ']")
        wait_time = self.drop_time - int(datetime.now().timestamp())
        if wait_time < 0:
            wait_time = 0
        sleep(wait_time)
        while len(element) != 0:
            try:
                element[0].click()
            except:
                break
            element = self.driver.find_elements_by_xpath("//button[@class='button-submit'][.=' Отправить заказ ']")
        print("Каеф")


    def close_browser(self):
        self.driver.close()

    def __del__(self):
        print('Destructor called, thread deleted.')
