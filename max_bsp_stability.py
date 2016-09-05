#coding=utf-8

from uiautomator import device as d
import unittest
import os
import time
import random
import sys

reload(sys) 
sys.setdefaultencoding('utf-8')

WIFI_NAME, WIFI_PWD = '360Wi-Fi', '123456789'
D_WIDTH = 1440
D_HEIGHT = 2392
D_C_X = D_WIDTH / 2
D_C_Y = D_HEIGHT / 2

resource_empty = 'android:id/empty'
resource_widget = 'com.android.settings:id/switch_widget'

class MaxBSPST(unittest.TestCase):
    CYCLE_NOW = 0
    start_time = 0
    CASE_NOW = ''

    def setUp(self):
        super(MaxBSPST, self).setUp()
        self.unlockScreen()
        if d(text = 'OK').wait.exists(timeout = 2000):
            self.firstBoot()
        self.backToDesktop()
        self.connectWiFi()

    def tearDown(self):
        super(MaxBSPST, self).tearDown()
        end_time = int(time.time())
        os.popen('adb shell /system/bin/screencap -p /sdcard/%s.png'%(end_time))
        duration = end_time - self.start_time
        # print "Start at %s"%self.start_time
        print "End at %s"%end_time
        print "Duration %ss"%(duration)
        str_path = 'max_bst_st_test_from_%s_to_%s'%(self.start_time,end_time)
        os.makedirs(str_path)
        os.popen('adb shell logcat -v time -d > %s/0_logcat_%s.txt'%(str_path,str(int(end_time))))
        os.popen('adb bugrepot > %s/0_bugreport.log'%str_path)
        os.popen('adb pull /sdcard/%s.png %s/%s'%(end_time,os.getcwd(),str_path))
        self.backToDesktop()
        
    def unlockScreen(self):
        d.wakeup()
        if d(resourceId = 'com.android.systemui:id/clock_view').wait.exists(timeout = 2000):
            d.swipe(D_C_X, D_HEIGHT-1, D_C_X, 0, 5)

    def firstBoot(self):
        d(text = 'OK').click.wait()
        d(resourceId='com.android.launcher:id/hotseat').click.wait()
        if d(resourceId='com.android.launcher:id/cling_dismiss').wait.exists(timeout = 2000):
            d(resourceId='com.android.launcher:id/cling_dismiss').click.wait()
        self.launchSettings()
        t = 0
        while d(text = 'About phone').wait.gone(timeout = 2000):
            d.swipe(D_C_X, D_HEIGHT-1, D_C_X, 0)
            time.sleep(1)
            t = t + 1
            if t > 10:
                print "No such an option..."
                break
        d(text = 'About phone').click.wait()
        for i in range(10):
            d(text = 'Build number').click()
        d.press('back')
        d(text = 'Developer options').click.wait()
        d(text = 'Stay awake').right(resourceId = 'android:id/switchWidget').click.wait()
        self.backToDesktop()

    def pressBack(self,times=1):
        for i in range(times):
            d.press('back')

    def backToDesktop(self):
        t = 0
        while d(resourceId='com.android.launcher:id/hotseat').wait.gone(timeout = 2000):
            self.pressBack()
            t = t + 1
            if t > 10:
                print "what happened..."
                break

    def launchSettings(self):
        os.popen("adb shell am start -n com.android.settings/.Settings")

    def refreshMedia(self):
        os.popen('adb shell am broadcast -a android.intent.action.MEDIA_MOUNTED -d file:///sdcard')

    def switchWLANBT(self,wireless,cycle):
        self.launchSettings()
        d(text = wireless).click.wait()
        assert d(resourceId = resource_widget).wait.exists(timeout = 2000)
        for i in range(cycle):
            print "%s, "%(i+1)
            self.CYCLE_NOW = i+1
            if d(resourceId = resource_empty).wait.exists(timeout = 2000):
                d(resourceId = resource_widget).click.wait()
                assert d(resourceId = resource_empty).wait.gone(timeout = 2000)
            else:
                d(resourceId = resource_widget).click.wait()
                assert d(resourceId = resource_empty).wait.exists(timeout = 2000)

    ######################################################################################

    def playVideo(self, cycle=1):
        os.popen('adb push IMG_0853.MP4 /sdcard/Movies/IMG_TEST.MP4')
        self.refreshMedia()
        for i in range(cycle):
            print "%s, "%(i+1),
            os.popen('adb shell am start -n com.android.gallery3d/.app.GalleryActivity')
            time.sleep(3)
            d.click(D_C_X, D_C_Y) # Enter the album
            time.sleep(3)
            d.click(D_C_X, D_C_Y) # Click on thumbnail
            if d(text = 'Open with').wait.exists(timeout = 2000):
                d(text = 'Video player').click.wait()
                time.sleep(1)
                d(text = 'Always').click.wait()
            # time.sleep(3)
            # d.click(D_C_X, D_C_Y) # Tap to start playing
            if d(text = 'Resume video').wait.exists(timeout = 2000):
                d(text = 'Start over').click.wait()
            time.sleep(180)
            self.backToDesktop() # Back to desktop
        print "\n"

    def playAudio(self, cycle=1):
        os.popen('adb push 96cat.mp3 /sdcard/Music/96cat.mp3')
        self.refreshMedia()
        for i in range(cycle):
            print "%s, "%(i+1),
            os.popen('adb shell am start -n com.android.music/.MusicBrowserActivity')
            time.sleep(3)
            d(text = 'Songs').click.wait() # Switch to songs tab
            d(resourceId = 'com.android.music:id/line1').click.wait() # Select one audio to play
            time.sleep(180)
            self.backToDesktop() # Back to desktop
        print "\n"

    def addDelFile(self, cycle=1):
        for i in range(cycle):
            print "%s, "%(i+1),
            os.popen('adb push IMG_0853.MP4 /sdcard/Movies/IMG_TEST.MP4')
            # print ">>> push mp4 file completely"
            os.popen('adb shell rm /sdcard/Movies/IMG_TEST.MP4')
            # print "<<< rm mp4 file completely"
            os.popen('adb push 96cat.mp3 /sdcard/Music/96cat.mp3')
            # print ">>> push mp3 file completely"
            os.popen('adb shell rm /sdcard/Music/96cat.mp3')
            # print "<<< rm mp3 file completely\n**********"
        print "\n"

    def gamePlay(self, cycle=1):
        for i in range(cycle):
            print "%s, "%(i+1),
            os.popen('adb shell am start -n com.imangi.templerun2.bd/com.templerun2.SuperIdsSingleSplashActivity')
            time.sleep(5)
            d.click(D_C_X, 1800) # Tap to start
            time.sleep(2)
            for i in range(10):
                d.swipe(D_C_X, D_HEIGHT-1, D_C_X, 0, 5)
            d.press('home')
            d.press('recent')
            while d(resourceId='com.android.systemui:id/dismiss_task').wait.exists(timeout = 2000):
                d(resourceId='com.android.systemui:id/dismiss_task').click.wait()
        print "\n"

    def turnOnWiFi(self):
        self.launchSettings()
        d(textContains = 'Fi').click.wait()
        assert d(resourceId = resource_widget).wait.exists(timeout = 2000)
        if d(resourceId = resource_empty).wait.exists(timeout = 2000):
            d(resourceId = resource_widget).click.wait()
            assert d(resourceId = resource_empty).wait.gone(timeout = 5000), "What's wrong..."

    def connectWiFi(self):
        self.turnOnWiFi()
        if d(textContains = 'Connected').wait.gone(timeout = 5000):
            t = 0
            while d(text = WIFI_NAME).wait.gone(timeout = 2000):
                time.sleep(1)
                t = t + 1
                if t > 10:
                    print "No such a WLAN..."
                    break
            d(text = WIFI_NAME).click.wait()
            d(resourceId = 'com.android.settings:id/password').set_text(WIFI_PWD)
            d(resourceId = 'com.android.settings:id/show_password').click.wait()
            assert d(text = WIFI_PWD).wait.exists(timeout = 2000), "input wrong password"
            d(text = 'Connect').click.wait()
            time.sleep(5)
            assert d(textContains = 'Connected').wait.exists(timeout = 5000)
        self.backToDesktop()
        print "\n"

    def runLeTv(self,cycle=1):
        for i in range(cycle):
            print "%s, "%(i+1),
            os.popen('adb shell am start -n com.letv.android.client/.activity.SplashActivity')
            while d(text = 'Allow').wait.exists(timeout = 2000):
                d(text = 'Allow').click.wait()
                time.sleep(1)
            d(text=u'电影').click.wait()
            d(text=u'电影').click.wait()
            d(resourceId='com.letv.android.client:id/channel_top_gallery_item_picture').click.wait()
            time.sleep(180)
            self.backToDesktop()
        print "\n"

    ######################################################################################

    def testST(self):
        '''
            steps:
                1. 
                2.
        '''
        ddiirr = "All_logs_20160902_start_night"
        try:
            os.makedirs(ddiirr)
        except:
            pass
        self.start_time = int(time.time())
        for i in range(100):
            print "- = - = - = %s times = - = - = -"%(i+1)
            # print "====> Connect WiFi: starts: %s "%(time.time()),
            # self.connectWiFi()
            # os.popen('adb shell logcat -v time -d > %s/%s.txt'%(ddiirr,int(time.time())))
            print "====> push/rm files: starts: %s "%(time.time()),
            self.addDelFile(10)
            os.popen('adb shell logcat -v time -d > %s/%s.txt'%(ddiirr,int(time.time())))
            print "====> play mp3: starts: %s "%(time.time()),
            self.playAudio(10)
            os.popen('adb shell logcat -v time -d > %s/%s.txt'%(ddiirr,int(time.time())))
            print "====> play video: starts: %s "%(time.time()),
            self.playVideo(10)
            os.popen('adb shell logcat -v time -d > %s/%s.txt'%(ddiirr,int(time.time())))
            print "====> run LeTV: starts: %s "%(time.time()),
            self.runLeTv(10)
            os.popen('adb shell logcat -v time -d > %s/%s.txt'%(ddiirr,int(time.time())))
