# -*- coding: UTF-8 -*-
from elements import elements
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

file_handler = logging.FileHandler('order.log')
file_handler.setFormatter(formatter1)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter2)
console_handler.setLevel(level=logging.INFO)
logger.addHandler(console_handler)


class Shopee(): 
    def __init__(self):
        self.driver = None
        self.timeout = None
        self.username = "test"
        self.password = "123456"
        self.elements = elements


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
        self.timeout = WebDriverWait(self.driver, 30)
        

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
                timeout.until(EC.element_to_be_clickable((By.XPATH,self.elements.get("popup_banner_button")))).click()
            
            #click the login link in the upper right corner
            timeout.until(EC.element_to_be_clickable((By.XPATH,self.elements.get("login_link")))).click()
 
            #enter username 
            timeout.until(EC.element_to_be_clickable((By.XPATH,self.elements.get("username_input")))).send_keys(self.username)
            logger.info("Enter username")

            #enter password
            timeout.until(EC.element_to_be_clickable((By.XPATH,self.elements.get("password_input")))).send_keys(self.password)
            logger.info("Enter password")
             
            #click login button
            timeout.until(EC.element_to_be_clickable((By.XPATH,self.elements.get("login_button")))).click()
            logger.info("Click login button")

            #check if there is a alert message
            alert = self.ElementExist(self.elements.get("alert_message"))
            #show error if there is a alert message
            if alert:
                error_message = timeout.until(EC.visibility_of_element_located((By.XPATH,self.elements.get("alert_message")))).text   
                logger.error(error_message)
                raise Exception("Incorrect account or password")
                        
            #close it if there is a popup banner 
            popup_banner = self.ElementExist(self.elements.get("popup_banner_button"))
            if popup_banner:
                timeout.until(EC.element_to_be_clickable((By.XPATH,self.elements.get("popup_banner_button")))).click()
            
            #verify login result
            login_result = self.VerifyLoginResult(self.username)
            if login_result:
                logger.info("Login successfully")  
            else:
                raise Exception("Login Failed")
                   
        except Exception as error:
            logger.exception(error)
            #take a screenshot when the error occurs
            driver.get_screenshot_as_file(current_time + ".png")

            # quit the driver and close all windows
            self.driver.quit()
            sys.exit()


    #Verify whether the account is logged in successfully    
    def VerifyLoginResult(self, username):
        logger.info("Verify whether the account is logged in successfully")  
        driver = self.driver
        timeout = self.timeout

        #check if the account in the upper right corner is equal to the login username
        account = timeout.until(EC.element_to_be_clickable((By.XPATH,self.elements.get("account")))).text
        login_result = bool(account == username)
        return login_result


    #place an order by searching an product
    def PlaceOrder(self):
        logger.info("Place an order by searching an product")
        driver = self.driver
        timeout = self.timeout
        current_time = time.strftime("%Y%m%d-%H.%M.%S")
        
        try:
            #Search products based on the keyword
            keyword = "apple"
            timeout.until(EC.element_to_be_clickable((By.XPATH,self.elements.get("search_input")))).send_keys(keyword)
            logger.info("Enter search keyword")

            #click search button
            timeout.until(EC.element_to_be_clickable((By.XPATH,self.elements.get("search_button")))).click()
            logger.info("Click search button")

            #click an item in the search result page
            timeout.until(EC.element_to_be_clickable((By.XPATH,self.elements.get("search_result_item")))).click()
            logger.info("Click search result item")

            #click if there are product options
            product_options = self.ElementExist(self.elements.get("product_options"))
            if product_options:
                timeout.until(EC.element_to_be_clickable((By.XPATH,self.elements.get("product_options")))).click()
                logger.info("Click product options")
                time.sleep(5)

            #Click buy directly button
            timeout.until(EC.element_to_be_clickable((By.XPATH,self.elements.get("buy_directly_button")))).click()
            logger.info("Click buy directly button")
            time.sleep(10)

            #Click go to checkout button
            timeout.until(EC.element_to_be_clickable((By.XPATH,self.elements.get("go_to_checkout_button")))).click()
            logger.info("Click go to checkout button")
            time.sleep(10)

            #Click bank transfer button
            bank_transfer_button = self.ElementExist(self.elements.get("bank_transfer_button"))
            if bank_transfer_button:
                timeout.until(EC.element_to_be_clickable((By.XPATH,self.elements.get("bank_transfer_button")))).click()
                logger.info("Click bank transfer button")
            time.sleep(10)
            
            #get order information in checkout page
            self.seller_checkoutpage = timeout.until(EC.visibility_of_element_located((By.XPATH,self.elements.get("seller_checkoutpage")))).text
            self.product_name_checkoutpage = timeout.until(EC.visibility_of_element_located((By.XPATH,self.elements.get("product_name_checkoutpage")))).text     
            self.order_amount_checkoutpage = timeout.until(EC.visibility_of_element_located((By.XPATH,self.elements.get("order_amount_checkoutpage")))).text   
            self.payment_method = timeout.until(EC.visibility_of_element_located((By.XPATH,self.elements.get("bank_transfer_button")))).text  
            logger.info("Place an order by " + self.payment_method)
            logger.info("Order information in checkout page - Seller: " + self.seller_checkoutpage + ", Product: " + self.product_name_checkoutpage + ", Order amount: " + self.order_amount_checkoutpage)

            #Click place order button
            timeout.until(EC.element_to_be_clickable((By.XPATH,self.elements.get("place_order_button")))).click()
            logger.info("Click place order button")
            time.sleep(10)

            #Click OK button when unexpected error occurs
            unexpected_error_OK_button = self.ElementExist(self.elements.get("unexpected_error_OK_button"))
            if unexpected_error_OK_button:
                timeout.until(EC.element_to_be_clickable((By.XPATH,self.elements.get("unexpected_error_OK_button")))).click()
                logger.info("Click OK button when unexpected error occurs")
                time.sleep(10)
            
            #Click OK button in bank transfer detail page
            bank_transfer_OK_button = self.ElementExist(self.elements.get("bank_transfer_OK_button"))
            if bank_transfer_OK_button:
                timeout.until(EC.element_to_be_clickable((By.XPATH,self.elements.get("bank_transfer_OK_button")))).click()
                logger.info("Click OK button in bank transfer detail page")
                time.sleep(10)
            
            #Check if the order is successfully created
            order_result = self.VerifyOrderResult()
            if order_result:
                logger.info("Successfully placed an order")
            else:
                raise Exception("Order Failed")   
        
        except Exception as error:
            logger.exception(error)
            #take a screenshot when the error occurs
            driver.get_screenshot_as_file(current_time + ".png")

        # quit the driver and close all windows
        self.driver.quit()
        sys.exit()
    

    #Verify that the order is successfully created
    def VerifyOrderResult(self):
        logger.info("Verify that the order status and order information is correct")
        driver = self.driver
        timeout = self.timeout
        
        order_status = timeout.until(EC.visibility_of_element_located((By.XPATH,self.elements.get("order_status")))).text 
        seller_orderlistpage = timeout.until(EC.visibility_of_element_located((By.XPATH,self.elements.get("seller_orderlistpage")))).text
        product_name_orderlistpage = timeout.until(EC.visibility_of_element_located((By.XPATH,self.elements.get("product_name_orderlistpage")))).text     
        order_amount_orderlistpage = timeout.until(EC.visibility_of_element_located((By.XPATH,self.elements.get("order_amount_orderlistpage")))).text   
        logger.info("Order status is : " + order_status)
        logger.info("Order information in order list page - Seller: " + seller_orderlistpage + ", Product: " + product_name_orderlistpage + ", Order amount: " + order_amount_orderlistpage)

        #If the order status and order information is correct, result = True
        if(order_status == u'待付款' and seller_orderlistpage == self.seller_checkoutpage and product_name_orderlistpage == self.product_name_checkoutpage and order_amount_orderlistpage == self.order_amount_checkoutpage):
            order_result = True
        else:
            order_result = False
        return order_result
    
    
    #Check if the element exist
    def ElementExist(self,element):
        exist_result = True
        driver = self.driver
        timeout = self.timeout
        #if the element exist, result = True
        try:
            timeout.until(EC.element_to_be_clickable((By.XPATH,element)))
        #if the element does not exist, result = False
        except:
            exist_result = False  
        return exist_result


if __name__ == "__main__":
    shopee = Shopee()
    shopee.InitialWebDriver()
    shopee.GoToShopeeWebsite()
    shopee.Login()
    shopee.PlaceOrder()
   
    