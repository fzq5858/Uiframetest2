import time
class Mylogin(object):
    def __init__(self, driver):
        self.driver = driver

    def login(self):
        self.driver.find_element_by_link_text("登录").click()
        time.sleep(2)
        self.driver.find_element_by_name("username").send_keys("17731990979")
        self.driver.find_element_by_id("password").send_keys("123456")
        self.driver.find_element_by_class_name("submit_login").click()
        time.sleep(5)

    def login2(self):
        self.driver.find_element_by_xpath('//input[@placeholder="请输入用户名"]').send_keys('admin')
        self.driver.find_element_by_xpath('//input[@placeholder="请输入密码"]').send_keys('admin')
        self.driver.find_element_by_name('submit').click()
        time.sleep(5)
            
            


            
    