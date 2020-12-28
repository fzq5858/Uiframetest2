import os
import unittest
import time
from public.loginApp import Mylogin
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.touch_action import TouchAction

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)



class AndroidTests(unittest.TestCase):
    def setUp(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'  #平台名称
        desired_caps['platformVersion'] = '5.1'   #填写虚拟机/手机的系统版本号
        desired_caps['deviceName'] = 'Android Emulator' #填写安卓虚拟机的设备名称
        desired_caps['noReset'] = 'True'
        desired_caps['app'] = PATH('E:/zhiyuan/zuiyou518.apk')
        desired_caps['appPackage'] = 'cn.xiaochuankeji.tieba'   #填写被测试app包名
        desired_caps['appActivity'] = '.ui.base.SplashActivity'  #填写被测试app入口，app打开首个界面 adb shell dumpsys activity top | findstr“ACTIVITY"
        desired_caps['unicodeKeyboard'] = 'True'  # 安装中文输入法
        desired_caps['resetKeyboard'] = 'True'    #重置虚拟机输入法
        desired_caps['newCommandTimeout'] = 200   #默认60秒
        desired_caps['automationName'] = 'Uiautomator2'  #toast

        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        time.sleep(60)
        self.driver.implicitly_wait(60)
        try:
            self.driver.find_element_by_id("cn.xiaochuankeji.tieba:id/tvConfirmWithBg").click()  # 点击我知道了（青少年模式）
            time.sleep(8)
        except:
            pass
        time.sleep(8)
        # dongtai=self.driver.find_elements_by_id("cn.xiaochuankeji.tieba:id/iconTabItem")
        # print(dongtai[1].text)


    def tearDown(self):
        self.driver.quit()
        pass

    def test01(self):
        '''验证底部导航栏文案显示是否正常'''
        self.driver.find_element_by_id('cn.xiaochuankeji.tieba:id/textTabItem')
        time.sleep(6)
        a= self.driver.find_elements_by_id('cn.xiaochuankeji.tieba:id/textTabItem')
        self.assertEqual(a[0].text,'最右')
        self.assertEqual(a[1].text,'动态')
        self.assertEqual(a[2].text,'消息')
        self.assertEqual(a[3].text,'我的')

    def test02(self):
        '''验证点击叉号屏蔽功能是否正常'''
        a=self.driver.find_element_by_id('cn.xiaochuankeji.tieba:id/simple_member_tv_name')
        bb=a.text
        print(bb)
        self.driver.find_element_by_id('cn.xiaochuankeji.tieba:id/simple_decorator_delete').click()
        time.sleep(6)
        self.assertTrue(self.driver.find_element_by_id('cn.xiaochuankeji.tieba:id/tv_tedium_title').is_displayed())
        self.driver.find_element_by_id('cn.xiaochuankeji.tieba:id/tv_tedium_other_reason').click()
        time.sleep(2)
        self.driver.find_element_by_class_name('android.widget.EditText').send_keys('不好8+4笑')
        #self.driver.find_element_by_id('cn.xiaochuankeji.tieba:id/dialog_edittext').send_keys('不好8+4笑')
        cc=self.driver.find_element_by_class_name('android.widget.EditText')
        print(cc.text)
        #print(cc.get_attribute('value'))
        time.sleep(4)
        self.driver.find_element_by_id('cn.xiaochuankeji.tieba:id/tvConfirm').click()
        time.sleep(20)
        #self.driver.refresh()
        #self.assertFalse(a.is_displayed())
        c=self.driver.find_element_by_id('cn.xiaochuankeji.tieba:id/simple_member_tv_name')
        print(c.text)
        self.assertNotEqual(bb,c.text)
        time.sleep(5)
        #self.assertTrue(self.driver.find_element_by_id(''))

    def test03(self):
        '''验证点击话题，进入话题页面正常'''
        self.driver.find_element_by_id('cn.xiaochuankeji.tieba:id/topic').click()
        time.sleep(2)
        self.assertTrue(self.driver.find_element_by_id('cn.xiaochuankeji.tieba:id/title').is_displayed())

    def test04(self):
        '''验证话题广场顶部文案是否正常'''
        self.driver.implicitly_wait(60)
        self.driver.find_element_by_id('cn.xiaochuankeji.tieba:id/topic').click()
        time.sleep(4)
        self.driver.find_element_by_id('cn.xiaochuankeji.tieba:id/tv_topic_square_inrecommend').click()
        time.sleep(5)
        a=self.driver.find_elements_by_id('cn.xiaochuankeji.tieba:id/tvPgcCategoryName')
        self.assertEqual(a[0].text,'推荐')
        self.assertEqual(a[1].text, '爆笑')
        self.assertEqual(a[2].text, '爱好')
        self.assertEqual(a[3].text, '生活圈')
        self.assertEqual(a[4].text, '游戏')
        self.assertEqual(a[5].text, '头像壁纸')
        self.assertEqual(a[6].text, '情感')
        self.assertEqual(a[7].text, '影音')

    def test05(self):
        '''验证关注页面有提示图片'''
        self.driver.find_element_by_id('cn.xiaochuankeji.tieba:id/title').click()
        time.sleep(8)
        self.assertTrue(self.driver.find_element_by_id('cn.xiaochuankeji.tieba:id/tips').is_displayed())

    def test06(self):
        '''验证未登陆时点击关注会提示先登陆'''
        self.driver.find_element_by_id('cn.xiaochuankeji.tieba:id/title').click()
        time.sleep(8)
        self.driver.find_element_by_id('cn.xiaochuankeji.tieba:id/tv_subscribe_name_unselected').click()
        self.driver.implicitly_wait(100)
        toast_loc = ("xpath", '//*[contains(@text,"请先登陆")]')
        e1 = WebDriverWait(self.driver, 20, 0.1).until(EC.presence_of_element_located(toast_loc))

    def test07(self):
        '''验证发帖正常'''
        Mylogin(self.driver).login()
        time.sleep(8)
        self.driver.find_element_by_id('cn.xiaochuankeji.tieba:id/iconTabItem').click()
        self.driver.implicitly_wait(100)
        self.driver.find_element_by_id('cn.xiaochuankeji.tieba:id/etContent').send_keys('fatian')
        time.sleep(5)
        self.driver.find_element_by_id('cn.xiaochuankeji.tieba:id/select_topic_top_container').click()
        time.sleep(5)
        self.driver.find_element_by_id('cn.xiaochuankeji.tieba:id/topic_title_tv').click()
        time.sleep(5)
        self.driver.find_element_by_id('cn.xiaochuankeji.tieba:id/try_publish').click()
        time.sleep(5)
        a=self.driver.find_element_by_id('cn.xiaochuankeji.tieba:id/simple_member_tv_name')
        self.assertTrue(a.text,'ad涅米')

    def test08(self):
        '''验证编辑个人信息选择城市'''
        Mylogin(self.driver).login()
        time.sleep(8)
        self.driver.find_elements_by_id('cn.xiaochuankeji.tieba:id/iconTabItem')[3].click()
        time.sleep(5)
        self.driver.find_element_by_class_name('android.widget.ImageView').click()
        self.driver.implicitly_wait(100)
        self.driver.find_element_by_id('cn.xiaochuankeji.tieba:id/btn_edit_info').click()
        time.sleep(5)
        city00=self.driver.find_element_by_id('cn.xiaochuankeji.tieba:id/tvCity')
        aa=city00.text
        city00.click()
        time.sleep(5)
        height = self.driver.get_window_size()['height']
        width = self.driver.get_window_size()['width']
        self.driver.swipe(width * 0.3, height * 0.8, width * 0.8, height * 0.8, 3000)
        self.driver.find_element_by_id('cn.xiaochuankeji.tieba:id/btnSubmit').click()
        time.sleep(5)
        city=self.driver.find_element_by_id('cn.xiaochuankeji.tieba:id/tvCity')
        bb=city.text
        city.click()
        time.sleep(5)
        self.assertFalse(aa.text,bb.text)

    def test09(self):
        '''验证长按弹出分享'''
        Mylogin(self.driver).login()
        time.sleep(5)
        self.driver.find_element_by_id("cn.xiaochuankeji.tieba:id/iconTabItem").click()
        time.sleep(5)
        el=self.driver.find_element_by_class_name('android.widget.ImageView')
        time.sleep(5)
        TouchAction(self.driver).long_press(el).perform()
        self.driver.implicitly_wait(80)
        self.driver.find_element_by_id('cn.xiaochuankeji.tieba:id/iconTabItem').click()

    def test10(self):
        '''验证评论发送是否正常'''
        Mylogin(self.driver).login()
        time.sleep(5)
        self.driver.find_element_by_id("cn.xiaochuankeji.tieba:id/iconTabItem").click()
        time.sleep(6)
        self.driver.implicitly_wait(60)
        el = self.driver.find_element_by_id("cn.xiaochuankeji.tieba:id/ic_search_b")
        time.sleep(6)
        self.driver.find_element_by_id("cn.xiaochuankeji.tieba:id/expand_content_view").click()
        time.sleep(6)
        self.driver.find_element_by_id("cn.xiaochuankeji.tieba:id/etInput").send_keys('t123')
        time.sleep(2)
        self.driver.find_element_by_id("cn.xiaochuankeji.tieba:id/send").click()
        toast_loc = ("xpath", '//*[contains(@text,"评论发送成功")]')
        e1 = WebDriverWait(self.driver, 20, 0.1).until(EC.presence_of_element_located(toast_loc))
        print(e1.text)
        time.sleep(2)
        self.driver.keyevent(4)

    def test11(self):
        '''验证下拉刷新是否正常'''
        # Mylogin(self.driver).login()
        # time.sleep(5)
        # self.driver.find_element_by_id("cn.xiaochuankeji.tieba:id/iconTabItem").click()
        # time.sleep(6)
        height = self.driver.get_window_size()['height']
        width = self.driver.get_window_size()['width']
        self.driver.swipe(width * 0.5, height * 0.3, width * 0.5, height * 0.8, 3000)
        self.driver.implicitly_wait(60)
        a=self.driver.find_element_by_xpath('//*[contains(@text,"为你选出")]')
        self.assertEqual('为你选出14条好帖',a.text)

    def test12(self):
        '''进入消息页面是否正常'''
        Mylogin(self.driver).login()
        time.sleep(5)
        self.driver.find_element_by_id("cn.xiaochuankeji.tieba:id/iconTabItem").click()
        time.sleep(6)
        self.driver.find_elements_by_id("cn.xiaochuankeji.tieba:id/iconTabItem")[2].click()
        time.sleep(6)
        self.driver.find_elements_by_id("cn.xiaochuankeji.tieba:id/title")[1].click()
        time.sleep(6)
        a=self.driver.find_elements_by_class_name("android.widget.RelativeLayout")
        for i in range(0,len(a)):
            a[i].click()
            time.sleep(3)
            self.driver.find_element_by_id("cn.xiaochuankeji.tieba:id/input").send_keys('cs哈喽哇')
            self.driver.find_element_by_id("cn.xiaochuankeji.tieba:id/text").click()
            self.driver.keyevent(4)
            time.sleep(4)
            continue
        time.sleep(6)

    def test13(self):
        '''验证搜索功能是否正常'''
        Mylogin(self.driver).login()
        time.sleep(5)
        self.driver.find_element_by_id("cn.xiaochuankeji.tieba:id/iconTabItem").click()
        time.sleep(6)
        self.driver.find_element_by_id("cn.xiaochuankeji.tieba:id/ic_search_b").click()
        time.sleep(3)
        self.driver.find_element_by_id("cn.xiaochuankeji.tieba:id/search_input").send_keys('电影')
        self.driver.find_element_by_id("cn.xiaochuankeji.tieba:id/ic_search_b").click()
        time.sleep(5)
        self.assertTrue(self.driver.find_element_by_xpath('//*[contains(text,"电影")]'))

    def test14(self):
        '''验证关注别人是否正常'''
        Mylogin(self.driver).login()
        time.sleep(5)
        self.driver.find_element_by_id("cn.xiaochuankeji.tieba:id/iconTabItem").click()
        time.sleep(6)
        self.driver.find_element_by_id("cn.xiaochuankeji.tieba:id/simple_member_tv_name").click()
        time.sleep(3)
        a=self.driver.find_element_by_id("cn.xiaochuankeji.tieba:id/btn_follow")
        bb=a.text
        a.click()
        time.sleep(3)
        self.assertnNotEqual(a.text,bb)

    def test15(self):
        '''验证视频刷新按键是否正常'''
        self.driver.find_elements_by_id("cn.xiaochuankeji.tieba:id/title")[2].click()
        time.sleep(3)
        self.driver.find_element_by_id("cn.xiaochuankeji.tieba:id/home_refresh_view").click()
        self.driver.implicitly_wait(60)
        a = self.driver.find_element_by_xpath('//*[contains(@text,"为你选出")]')
        self.assertEqual('为你选出12条好帖', a.text)

    def test16(self):
        '''验证顶帖键功能是否正常'''
        Mylogin(self.driver).login()
        time.sleep(5)
        self.driver.find_element_by_id("cn.xiaochuankeji.tieba:id/iconTabItem").click()
        time.sleep(6)
        a=self.driver.find_element_by_id("cn.xiaochuankeji.tieba:id/tvUpCount")
        bb=a.text
        self.driver.find_element_by_id("cn.xiaochuankeji.tieba:id/ivUpArrow").click()
        self.assertNotEqual(bb, a.text)

    def test17(self):
        '''验证取消顶帖键功能是否正常'''
        Mylogin(self.driver).login()
        time.sleep(5)
        self.driver.find_element_by_id("cn.xiaochuankeji.tieba:id/iconTabItem").click()
        time.sleep(2)
        # a=self.driver.find_element_by_id("cn.xiaochuankeji.tieba:id/tvUpCount")
        # bb=a.text
        self.driver.find_element_by_id("cn.xiaochuankeji.tieba:id/ivUpArrow").click()
        self.driver.find_element_by_id("cn.xiaochuankeji.tieba:id/ivDownArrow").click()
        time.sleep(2)
        self.driver.find_element_by_id("cn.xiaochuankeji.tieba:id/tv_func_click").click()

    def test18(self):
        '''验证进入话题是否正常'''
        Mylogin(self.driver).login()
        time.sleep(5)
        self.driver.find_element_by_id("cn.xiaochuankeji.tieba:id/iconTabItem").click()
        time.sleep(2)
        a=self.driver.find_element_by_id("cn.xiaochuankeji.tieba:id/topic_tv")
        bb=a.text
        a.click()
        time.sleep(2)
        cc=self.driver.find_element_by_id("cn.xiaochuankeji.tieba:id/tvTopicName").text
        self.assertEqual(bb,cc)

    def test19(self):
        '''验证进入视频是否正常'''
        Mylogin(self.driver).login()
        time.sleep(5)
        self.driver.find_element_by_id("cn.xiaochuankeji.tieba:id/iconTabItem").click()
        time.sleep(2)
        self.driver.find_elements_by_id("cn.xiaochuankeji.tieba:id/title")[2].click()
        time.sleep(2)
        self.driver.find_element_by_id("cn.xiaochuankeji.tieba:id/holder_flow_rmdv").click()
        time.sleep(5)
        self.driver.find_element_by_id("cn.xiaochuankeji.tieba:id/iv_danmu_switch").click()

    def test20(self):
        '''验证发弹幕是否正常'''
        Mylogin(self.driver).login()
        time.sleep(5)
        self.driver.find_element_by_id("cn.xiaochuankeji.tieba:id/iconTabItem").click()
        time.sleep(2)
        self.driver.find_elements_by_id("cn.xiaochuankeji.tieba:id/title")[2].click()
        time.sleep(2)
        self.driver.find_element_by_id("cn.xiaochuankeji.tieba:id/holder_flow_rmdv").click()
        time.sleep(5)
        self.driver.find_element_by_id("cn.xiaochuankeji.tieba:id/text_danmu").send_keys('发弹幕测试测试测试')
        time.sleep(5)







if __name__ == "__main__":
    unittest.main()

