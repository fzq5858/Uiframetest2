# coding=utf-8
from selenium import webdriver
import unittest
import os
import time
from public.login import Mylogin
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class youhuiquan(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://101.133.169.100/yuns/index.php/admin/index/login")
        self.driver.maximize_window()
        time.sleep(5)
        Mylogin(self.driver).login2()   #登陆后台
        self.driver.find_element_by_xpath('/html/body/div[1]/ul/a[4]').click()  #点击营销
        time.sleep(5)


    def tearDown(self):
        filedir = "E:/Pyc.path/screenshot/"
        if not os.path.exists(filedir):
            os.makedirs(os.path.join('E:/', 'Pyc.path', 'screenshot'))
        screen_name = filedir + time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time())) + ".png"
        self.driver.get_screenshot_as_file(screen_name)
        self.driver.quit()


    def testyouhuiquan01(self):
        '''点击添加优惠券是否进入编辑优惠券页面'''

        print(self.driver.window_handles)
        print(self.driver.current_window_handle)
        self.driver.switch_to.frame('content')       #切入iframe
        self.driver.find_element_by_link_text("添加优惠券").click()
        time.sleep(3)
        print(self.driver.window_handles)
        print(self.driver.current_window_handle)
        ele = WebDriverWait(self.driver, 10, 0.5).until(EC.presence_of_element_located((By.CLASS_NAME, "explain")))
        ele.click()

    def testyouhuiquan02(self):
        '''点击删除按钮是否弹出提示框'''
        self.driver.switch_to.frame('content')
        self.driver.find_elements_by_link_text('删除')[0].click()
        print(self.driver.switch_to.alert.text)
        self.driver.switch_to.alert.dismiss()


    def testyouhuiquan03(self):
        '''点击编辑按钮是否跳转到编辑优惠券页面'''
        self.driver.switch_to.frame('content')
        self.driver.find_elements_by_link_text('编辑')[0].click()
        WebDriverWait(self.driver, 10, 0.5).until(EC.presence_of_element_located((By.CLASS_NAME, "explain")))

    def testyouhuiquan04(self):
        '''添加优惠券不输入内容点击确认是否提示'''
        self.driver.switch_to.frame('content')  # 切入iframe
        self.driver.find_element_by_link_text("添加优惠券").click()
        self.driver.find_element_by_xpath('//*[@id="form"]/table/tbody/tr[11]/td[2]/input').click()
        self.driver.switch_to.default_content()
        self.driver.implicitly_wait(3)
        point_out = self.driver.find_element_by_xpath('/html/body/div[6]/span').text
        self.assertEqual(point_out, '名称不能为空')


    def testyouhuiquan05(self):
        '''添加优惠券只输入活动名称点击确认，提示内容是否正确'''
        self.driver.switch_to.frame('content')  # 切入iframe
        self.driver.find_element_by_link_text("添加优惠券").click()
        self.driver.find_element_by_xpath('//*[@id="form"]/table/tbody/tr[2]/td[2]/input').send_keys('国庆活动')
        self.driver.find_element_by_xpath('//*[@id="form"]/table/tbody/tr[11]/td[2]/input').click()
        self.driver.switch_to.parent_frame()
        self.driver.implicitly_wait(3)
        point_out=self.driver.find_element_by_xpath('/html/body/div[6]/span').text
        self.assertEqual(point_out,'优惠金额不能为空')

    def testyouhuiquan06(self):
        '''验证优惠金额不能为负数'''
        self.driver.switch_to.frame('content')  # 切入iframe
        self.driver.find_elements_by_link_text('编辑')[0].click()
        self.driver.find_element_by_xpath('//*[@id="form"]/table/tbody/tr[3]/td[2]/input').clear()
        self.driver.find_element_by_xpath('//*[@id="form"]/table/tbody/tr[3]/td[2]/input').send_keys('-123')
        self.driver.find_element_by_xpath('//*[@id="form"]/table/tbody/tr[11]/td[2]/input').click()
        self.driver.switch_to.parent_frame()
        self.driver.implicitly_wait(3)
        point_out = self.driver.find_element_by_xpath('/html/body/div[6]/span').text
        self.assertEqual(point_out, '优惠金额不能为负数')
        # time.sleep(2)
        # self.driver.find_element_by_xpath(' self.driver.find_element_by_xpath')

    def testyouhuiquan07(self):
        '''验证选择部分商品是否正常'''
        self.driver.switch_to.frame('content')  # 切入iframe
        self.driver.find_element_by_link_text("添加优惠券").click()
        self.driver.find_element_by_xpath('//*[@id="form"]/table/tbody/tr[8]/td[2]/label[2]/input').click()
        self.driver.find_element_by_xpath('//*[@id="form"]/table/tbody/tr[8]/td[2]/a').click()
        self.driver.switch_to.parent_frame()
        time.sleep(2)
        self.driver.find_element_by_xpath('/html/body/div[6]/div/div[2]/table/tbody/tr[1]/td[1]/input').click()
        time.sleep(1)
        self.driver.find_element_by_xpath('/html/body/div[6]/div/div[3]/a').click()
        self.driver.switch_to.frame('content')
        time.sleep(2)
        a=self.driver.find_element_by_xpath('//*[@id="form"]/table/tbody/tr[9]/td[2]/table/tbody/tr/td[5]/a').is_displayed()
        self.assertEqual(a,True)

    def testyouhuiquan08(self):
        '''验证添加开始时间是否正常'''
        self.driver.switch_to.frame('content')  # 切入iframe
        self.driver.find_element_by_link_text("添加优惠券").click()
        self.driver.find_element_by_xpath('//*[@id="start_time"]').send_keys('2020-09-30 00:00')
        time.sleep(2)
        self.driver.find_element_by_xpath('//*[@id="form"]/table/tbody/tr[5]/td[2]/input').click()
        a = self.driver.find_element_by_xpath('//*[@id="start_time"]').get_attribute('value')
        self.assertEqual(a, "2020-09-30 00:00")
        print("OKk")

    def testyouhuiquan09(self):
        '''验证添加开始时间不能是过去的日期'''
        self.driver.switch_to.frame('content')  # 切入iframe
        self.driver.find_element_by_link_text("添加优惠券").click()
        self.driver.find_element_by_xpath('//*[@id="start_time"]').click()
        self.driver.find_element_by_xpath('//*[@id="start_time"]').send_keys('2018-09-30 00:00')
        self.driver.find_element_by_xpath('//*[@id="form"]/table/tbody/tr[5]/td[2]/input').click()
        time.sleep(5)
        a=self.driver.find_element_by_xpath('//*[@id="laydate_time"]/p').text
        self.assertEqual(a, "日期不在有效期内，请重新选择。")



    def testyouhuiquan10(self):
        '''点击正常，验证商品列表的日期是否都是正常的，不应该包含过期的商品'''
        self.driver.switch_to.frame('content')
        self.driver.find_element_by_xpath('/html/body/div/div[2]/a[3]').click()
        time.sleep(4)
        #print(self.driver.window_handles)
        el=self.driver.find_elements_by_css_selector('tr td:nth-child(7)')
        # showtime=[]
        # for i in range(0,len(el)):
        #     showtime.append(el[i].text)
        #     print(showtime)
        #print(self.driver.find_element_by_xpath('/html/body/div/div[3]/table/tbody/tr[7]/td[7]').text)
        #print(el)
        #print(el[0].text)
        showtime=[el[i].text for i in range(0,len(el))]
        #print(showtime)
        import datetime
        nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        print(nowTime)
        for i in range(len(showtime)):
            if showtime[i] > nowTime:
                print('正常')
            else:
                print('过期')
                self.assertEqual('展示结束时间大于','本地时间')





if __name__ == "__main__":
    unittest.main()
