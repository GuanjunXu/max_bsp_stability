#coding=utf-8

from uiautomator import device as d
import unittest
import os
import time
import random
import sys

reload(sys) 
sys.setdefaultencoding('utf-8')

TEST_CYCLE = 500
WIFI_NAME = 'zhangmeiniu'
WIFI_PWD = '011706122'

resource_empty = 'android:id/empty'
resource_widget = 'com.android.settings:id/switch_widget'

class MaxBSPTest(unittest.TestCase):
    CYCLE_NOW = 0
    start_time = 0
    CASE_NOW = ''

    def setUp(self):
        super(MaxBSPTest, self).setUp()
        self.backToDesktop()
        if d(text = u'确定').wait.exists(timeout = 2000):
            self.firstLaunch()
        self.start_time = time.time()
        print "start: \t%s"%(time.strftime('%Y%m%d_%H%M%S',time.localtime(self.start_time)))
        print "case name: ",

    def tearDown(self):
        super(MaxBSPTest, self).tearDown()
        end_time = time.time()
        print "\nend: \t%s"%(time.strftime('%Y%m%d_%H%M%S',time.localtime(end_time)))
        print "duration: \t%s"%(end_time-self.start_time)
        print "\t ... end at %s time(s)"%(self.CYCLE_NOW),
        if self.CYCLE_NOW < TEST_CYCLE:
            print ": Fail..."
            whatnow = time.time()
            fmtime  = time.strftime('%Y%m%d_%H%M%S',time.localtime(whatnow))
            os.popen('adb shell /system/bin/screencap -p /sdcard/%s.png'%(fmtime))
            strpath = 'max_android_result/%s_end_at_%s_%s'%(self.CASE_NOW,self.CYCLE_NOW,fmtime)
            os.makedirs(strpath)
            os.popen('adb shell logcat -d > %s/logcat_%s.txt'%(strpath,fmtime))
            os.popen('adb bugrepot > %s/0_bugreport.log'%strpath)
            os.popen('adb pull /sdcard/%s.png %s\\%s\\%s.png'%(fmtime,os.getcwd(),strpath,fmtime))
            # print 'adb pull /sdcard/%s.png %s\\%s\\%s.png'%(fmtime,os.getcwd(),strpath,fmtime)
        else:
            print ": - Pass -"
        print " - * - * - * - * - * - * - * - * - * -"
        self.CASE_NOW = ''
        self.CYCLE_NOW = 0
        self.backToDesktop()

    # def testPrint(self):
    #     self.CASE_NOW = "testPrint"
    #     print self.CASE_NOW
    #     for i in range(TEST_CYCLE):
    #         self.CYCLE_NOW = i+1
    #     time.sleep(5)

    def firstLaunch(self):
        # for escape the devices' beginner's guide when first power up
        # need long-pressing back key before running
        # if d(text = u'确定').wait.exists(timeout = 2000):
        d(text = u'确定').click.wait()
            # To set up never sleep
        d(resourceId='com.android.launcher:id/hotseat').click.wait()
        if d(resourceId='com.android.launcher:id/cling_dismiss').wait.exists(timeout = 2000):
            d(resourceId='com.android.launcher:id/cling_dismiss').click.wait()
        d(text = u'设置').click.wait()
        while d(text = u'关于手机').wait.gone(timeout = 2000):
            # Slide up
            d.swipe(700,2550,700,1)
        d(text = u'关于手机').click.wait()
        for i in range(10):
            d(text = u'版本号').click()
        d.press('back')
        d(text = u'开发者选项').click.wait()
        d(text = u'不锁定屏幕').right(resourceId = 'android:id/switchWidget').click.wait()
        self.backToDesktop()

    def pressBack(self,times=1):
        for i in range(times):
            d.press('back')

    def backToDesktop(self):
        while d(resourceId='com.android.launcher:id/hotseat').wait.gone(timeout = 2000):
            self.pressBack()

    def switchWLANBT(self,wireless,cycle):
        self.launchSettings()
        d(text = wireless).click.wait()
        assert d(resourceId = resource_widget).wait.exists(timeout = 2000)
        for i in range(cycle):
            self.CYCLE_NOW = i+1
            if d(resourceId = resource_empty).wait.exists(timeout = 2000):
                d(resourceId = resource_widget).click.wait()
                assert d(resourceId = resource_empty).wait.gone(timeout = 2000)
            else:
                d(resourceId = resource_widget).click.wait()
                assert d(resourceId = resource_empty).wait.exists(timeout = 2000)

    def launchSettings(self):
        os.popen("adb shell am start -n com.android.settings/.Settings") # Launch Settings

    def testWifiEnDis(self):
        '''
            Steps:
                1. Launch Settings
                2. Enable Wifi
                3. Disable Wifi
                4. Re-run 2~3 multiple times
        '''
        self.CASE_NOW = "testWifiEnDis"
        print self.CASE_NOW
        self.switchWLANBT('WLAN',TEST_CYCLE)

    def testBTEnDis(self):
        '''
            Steps:
                1. Launch Settings
                2. Enable BT
                3. Disable BT
                4. Re-run 2~3 mutiple times
        '''
        self.CASE_NOW = "testBTEnDis"
        print self.CASE_NOW
        self.switchWLANBT(u'蓝牙',TEST_CYCLE)

    def testDisConnectWiFi(self):
        '''
            Steps:
                1. Launch Settings
                2. Enable WiFi
                3. Connect an AP
                4. Forgot the AP step 3rd connected
                5. Re-run 3~4 multiple times
        '''
        self.CASE_NOW = "testDisConnectWiFi"
        print self.CASE_NOW
        self.launchSettings()
        d(text = 'WLAN').click.wait()
        if d(resourceId = resource_empty).wait.exists(timeout = 2000):
            d(resourceId = resource_widget).click.wait()
            assert d(resourceId = resource_empty).wait.gone(timeout = 2000)
        for i in range(TEST_CYCLE):
            self.CYCLE_NOW = i+1
            d(text = WIFI_NAME).click.wait()
            if d(text = u'取消保存').wait.exists(timeout = 2000): # To disconnect ap if the current status was connected
                d(text = u'取消保存').click.wait()
                d(text = WIFI_NAME).click.wait()
            # d(resourceId = 'com.android.settings:id/password').click.wait()
            d(resourceId = 'com.android.settings:id/password').set_text(WIFI_PWD)
            d(text = u'显示密码').click.wait()
            assert d(text = WIFI_PWD).wait.exists(timeout = 2000), "input wrong password"
            d(text = u'连接').click.wait()
            time.sleep(5)
            assert d(textContains = u'已连接').wait.exists(timeout = 5000) or d(textContains = u'已保存').wait.exists(timeout = 10000), "wifi does not connect successfully in 10s"
            d(textContains = u'已连接').click.wait() # Sometimes it pop up a dialog which contains text wifiname
            time.sleep(1)
            d(text = u'取消保存').click.wait()
            assert d(textContains = u'已连接').wait.gone(timeout = 2000)

    # def testDisConnectBT(self):
    #     '''
    #         Steps:
    #             1. Launch Settings
    #             2. Enable BT
    #             3. Connect another BT device
    #             4. Forgot the device step 3rd connected
    #             5. Re-run 3~4 multiple times
    #     '''
    #     pass