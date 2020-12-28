# coding=utf-8
from selenium import webdriver
from public.login import Mylogin
import unittest
import os
import time
from selenium.webdriver.common.action_chains import ActionChains

class TestShouye(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://101.133.169.100/yuns/index.php")
        self.driver.maximize_window()
        time.sleep(5)
        print("starttime:" + time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time())))

    def tearDown(self):
        filedir = "E:/Pyc.path/screenshot/"
        if not os.path.exists(filedir):
            os.makedirs(os.path.join('E:/', 'Pyc.path', 'screenshot'))
        print("endTime:" + time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time())))
        screen_name = filedir + time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time())) + ".png"
        self.driver.get_screenshot_as_file(screen_name)
        self.driver.quit()


    def testShouye01_01(self):
        '''测试首页导航文案显示是否正常'''
        Mylogin(self.driver).login()
        firstPageNavi = self.driver.find_element_by_xpath("//div[@class='top']/span")
        loginText = self.driver.find_element_by_css_selector("div.login>a:nth-child(1)")
        regisText = self.driver.find_element_by_css_selector("div.login>a:nth-child(3)")

        self.assertEqual("亲，欢迎您来到云商系统商城！",firstPageNavi.text)
        self.assertEqual("17731990979", loginText.text)
        self.assertEqual("退出", regisText.text)
        self.assertNotEqual("dd", regisText.text)

        self.assertIn("云商系统商城",firstPageNavi.text)

        self.assertTrue(self.driver.find_element_by_xpath("//div[@class='top']/span").is_displayed())
        self.assertFalse(firstPageNavi.is_displayed())

        if loginText.text == "177****0979":
            print("等于")
        else:
            print("不等于")
            self.driver.find_element_by_xpath("王麻子")



    def testShouye01_02(self):
        '''验证搜索内容无时，提示语是否正常'''
        Mylogin(self.driver).login()
        self.driver.find_element_by_xpath("/html/body/div/div/div/div/form/input[1]").send_keys("王麻子")
        self.driver.find_element_by_xpath("/html/body/div/div/div/div/form/input[2]").click()
        time.sleep(2)
        searchText = self.driver.find_element_by_xpath("//div[@class='nomsg']")
        self.assertEqual(searchText.text, "抱歉，没有找到相关的商品")


    def testyhq01_03(self):
        '''验证未登陆时点击领取优惠券弹出登陆页面'''
        self.driver.find_element_by_xpath("/html/body/div[3]/div/div[2]/a[3]").click()
        time.sleep(5)
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.find_element_by_xpath("/html/body/div[4]/div/div/div[1]/div[3]").click()
        time.sleep(2)
        self.assertTrue(self.driver.find_element_by_xpath('//*[@id="ajax_login"]').is_displayed())
        time.sleep(5)


    def testyhq01_04(self):
        '''验证优惠券点击部分商品可用跳转到产品列表页面'''
        self.driver.find_element_by_xpath("/html/body/div[3]/div/div[2]/a[3]").click()
        time.sleep(2)
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.find_element_by_xpath("/html/body/div[4]/div/div/div[6]/div[2]/div[2]/span/a").click()
        time.sleep(4)
        self.driver.switch_to.window(self.driver.window_handles[2])
        self.assertTrue(self.driver.find_element_by_xpath('/html/body/div[4]/div/div[4]/div[1]/span').is_displayed())

    def testyhq01_05(self):
        '''验证点击页面下方帮助中心正常跳转'''
        js = "var q=document.documentElement.scrollTop=10000"  # 移动到页面底部，设置一个很大的值
        self.driver.execute_script(js)
        self.driver.find_element_by_xpath('/html/body/div[9]/div/div/div[2]/dl[2]/dd[1]/a').click()
        self.driver.switch_to.window(self.driver.window_handles[1])
        a=self.driver.find_element_by_xpath('/html/body/div[4]/div/div/div[2]/div[2]')
        self.assertIn('这个是帮助中心',a.text)

    def testyhq01_06(self):
        '''验证品牌街翻页正常'''
        self.driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/a[6]').click()
        time.sleep(2)
        self.driver.switch_to.window(self.driver.window_handles[1])
        time.sleep(2)
        a = self.driver.find_element_by_xpath('/html/body/div[4]/div/div[2]/div[2]/a/div/div[2]').text
        self.driver.find_element_by_xpath('/html/body/div[4]/div/div[3]/a[6]').click()
        print(self.driver.window_handles)
        print(self.driver.current_window_handle)
        time.sleep(2)
        b=self.driver.find_element_by_xpath('/html/body/div[4]/div/div[2]/div[2]/a/div/div[2]').text
        self.assertNotEqual(a,b)


    def testyhq01_07(self):
        '''验证点击母婴玩具弹出二级菜单'''
        my=self.driver.find_element_by_xpath('/html/body/div[3]/div/div[1]/div/dl[4]/dt/div/span/a')
        ActionChains(self.driver).move_to_element(my).perform()
        time.sleep(2)
        a=self.driver.find_element_by_xpath('/html/body/div[3]/div/div[1]/div/dl[4]/div/div[2]/div/a').is_displayed()
        self.assertEqual(a,True)

    def testyhq01_08(self):
        '''验证点击注册跳转到注册页面'''
        self.driver.find_element_by_xpath('/html/body/div[4]/div/div[2]/div[1]/div[2]/p/a[2]').click()
        a=self.driver.find_element_by_xpath('/html/body/div[2]/div/div[1]/form/div[2]/div[7]/input').is_displayed()
        self.assertTrue(a)

    def testyhq01_09(self):
        '''验证点击商城动态下的标题'''
        self.driver.find_element_by_xpath('/html/body/div[4]/div/div[2]/div[2]/div[2]/div/a[3]').click()
        self.driver.switch_to.window(self.driver.window_handles[1])
        time.sleep(2)
        a = self.driver.find_element_by_xpath('/html/body/div[4]/div/div[1]/div[1]/h1').is_displayed()
        self.assertTrue(a)


if __name__ == "__main__":
    unittest.main()


