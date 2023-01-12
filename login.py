# -*- coding: UTF-8 -*-
import logging
import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, SessionNotCreatedException


#logger setting
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)
formatter1 = logging.Formatter('%(asctime)s - %(lineno)s - %(levelname)s : %(message)s')
formatter2 = logging.Formatter('%(asctime)s - %(levelname)s : %(message)s')

file_handler = logging.FileHandler('login.log')
file_handler.setFormatter(formatter1)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter2)
console_handler.setLevel(level=logging.INFO)
logger.addHandler(console_handler)


class Login: 
    def __init__(self):
        self.driver = None
        self.timeout = None
        self.username = "test"
        self.password = "1256"
        self.elements={'popup_banner_button':'div.shopee-popup__close-btn',
                        'login_link':'登入',
                        'username_input':'loginKey',
                        'password_input':'password',
                        'login_button':'/html/body/div[1]/div/div[2]/div/div/form/div/div[2]/button',
                        'alert_message':'div._-packages-user-common-ui-alert-pc-src-components-BaseAlert-style__primaryText',
                        'account':'div.navbar__username'
                        }


    #set up driver
    def InitialWebDriver(self):
        logger.info("Set up driver")
        
        options = webdriver.ChromeOptions()
        #turn off Chrome notifications
        prefs = {
            'profile.default_content_setting_values':
                {
                    'notifications': 2
                },
            "profile.password_manager_enabled": False, 
            "credentials_enable_service": False
        }
        options.add_experimental_option('prefs', prefs) 
        options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])

        try:
            self.driver = webdriver.Chrome(options = options)
        #log error when the version does not match
        except SessionNotCreatedException:
            logger.exception("ChromeDriver does not support the current browser version")
            sys.exit()
            
        #set the waiting time limit
        self.timeout = WebDriverWait(self.driver, 10)
        

    #go to Shopee website
    def GoToShopeeWebsite(self):
        logger.info("Go to Shopee website")
        driver = self.driver
        driver.get("https://shopee.tw")
        
        #expand the window to maximum
        driver.maximize_window()


    #login Shopee with username and password
    def Login(self):   
        logger.info("Login with username: " + self.username + " and password: " + self.password)
        driver = self.driver
        timeout = self.timeout
        current_time = time.strftime("%Y%m%d-%H.%M.%S")

        try:
            #close it if there is a popup banner 
            popup_banner = self.ElementExist(self.elements.get("popup_banner_button"))
            if popup_banner:
                timeout.until(EC.element_to_be_clickable((By.CSS_SELECTOR,self.elements.get("popup_banner_button")))).click()
            
            #click the login link in the upper right corner
            timeout.until(EC.element_to_be_clickable((By.LINK_TEXT,self.elements.get("login_link")))).click()
 
            #enter username 
            timeout.until(EC.element_to_be_clickable((By.NAME,self.elements.get("username_input")))).send_keys(self.username)
            logger.info("Enter username")

            #enter password
            timeout.until(EC.element_to_be_clickable((By.NAME,self.elements.get("password_input")))).send_keys(self.password)
            logger.info("Enter password")
             
            #click login button
            timeout.until(EC.element_to_be_clickable((By.XPATH,self.elements.get("login_button")))).click()
            logger.info("Click login button")

            #check if there is a alert message
            alert = self.ElementExist(self.elements.get("alert_message"))
            #show error if there is a alert message
            if alert:
                error_message = timeout.until(EC.visibility_of_element_located((By.CSS_SELECTOR,self.elements.get("alert_message")))).text   
                logger.error(error_message)
                raise Exception("Incorrect account or password")
                        
            #close it if there is a popup banner 
            popup_banner = self.ElementExist(self.elements.get("popup_banner_button"))
            if popup_banner:
                timeout.until(EC.element_to_be_clickable((By.CSS_SELECTOR,self.elements.get("popup_banner_button")))).click()
                
            #verify login result
            result = self.VerifyResult(self.username)
            if result:
                logger.info("Login successfully")  
            else:
                raise Exception("Login Failed")
        
        except Exception as error:
            logger.exception(error)
            #take a screenshot when the error occurs
            driver.get_screenshot_as_file(current_time + ".png")
            

    #Verify whether the account is logged in successfully    
    def VerifyResult(self, username):
        logger.info("Verify whether the account is logged in successfully")  
        driver = self.driver
        timeout = self.timeout

        #check if the account in the upper right corner is equal to the login username
        account = timeout.until(EC.element_to_be_clickable((By.CSS_SELECTOR,self.elements.get("account")))).text
        result = bool(account == username)
        return result


    #Check if the element exist
    def ElementExist(self,element):
        result = True
        driver = self.driver
        timeout = self.timeout
        #if the element exist, result = True
        try:
            timeout.until(EC.element_to_be_clickable((By.CSS_SELECTOR,element)))
        #if the element does not exist, result = False
        except:
            result = False
        return result
    

if __name__ == "__main__":
    try:
        login = Login()
        login.InitialWebDriver()
        login.GoToShopeeWebsite()
        login.Login()

    except:
        logger.exception()

    finally:
        #quit the driver and close all windows
        login.driver.quit()
        