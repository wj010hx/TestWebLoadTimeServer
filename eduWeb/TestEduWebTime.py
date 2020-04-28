from selenium.webdriver.common.by import By
from datetime import date
from _pytest import fixtures
from selenium import webdriver
import pytest
import os
import hashlib
import time


class TestWebLoadTime:
    _loadtimeResultPath = "D:\\AllTestResult\\webLoadTime\\result.txt"
    chromdriverPath = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe"
    second = 0
    f = None
    wnyzm = ''
    load_time = {}

    test_index_expectTime = 0.1
    test_tologin_expectTime = 4
    test_signup_expectTime = 3
    test_fogetPass_expectTime = 3
    test_login_expectTime = 6
    test_jxhd_expectTime = 6
    test_eduNews_expectTime = 5
    test_appCenter_expectTime = 6
    test_personalCenter_expectTime = 3
    test_liveIndex_expectTime = 5
    test_liveDetail_expectTime = 8

    @pytest.fixture(scope="module")
    def remove_file(self):
        if os.path.exists(self._loadtimeResultPath):
            os.remove(self._loadtimeResultPath)
        else:
            print("无此文件")

    def login(self):
        self.driver.get("https://edu.10086.cn/sso/login?mode=1&service=http://edu.10086.cn/cloud/login/login")
        self.driver.maximize_window()
        self.driver.find_element(By.XPATH, "//img[@class='tab']").click()
        self.driver.find_element(By.ID, "tel-name").send_keys("23897010016")
        self.driver.find_element(By.XPATH, "//div[@class='login']//input[@class='login_pass']").send_keys("1q2w3e4r")
        self.driver.find_element(By.CSS_SELECTOR, "input.login_yzm").send_keys(self.wnyzm)
        time.sleep(2)
        self.driver.find_element(By.XPATH, "//input[@name='type']").click()
        self.driver.find_element(By.XPATH, "//div[@class='btn-wrap']//a[@id='js_login-btn']").click()

    def setup(self):
        PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))
        chrome_driver = PATH(self.chromdriverPath)
        os.environ["webdriver.chrome.driver"] = chrome_driver
        self.driver = webdriver.Chrome(chrome_driver)
        self.driver.implicitly_wait(10)
        self.wnyzm = self.getCheckCode()

    def test_index(self, remove_file):
        self.driver.get("http://edu.10086.cn")
        self.countTiming()
        self.f.write('test_index=%.2f\n' % self.second)
        self.f.close()
        self.load_time['test_index'] = self.second

    def test_tologin(self, remove_file):
        self.driver.get("https://edu.10086.cn/sso/login?mode=1&service=http://edu.10086.cn/cloud/login/login")
        self.countTiming()
        self.f.write('test_tologin=%.2f\n' % self.second)
        self.f.close()
        self.load_time['test_tologin'] = self.second

    def test_signup(self, remove_file):
        self.driver.get(
            "https://edu.10086.cn/sso/register/show/1?service=http%3a%2f%2fedu.10086.cn%2fcloud%2flogin%2flogin")
        self.countTiming()
        self.f.write('test_signup=%.2f\n' % self.second)
        self.f.close()
        self.load_time['test_signup'] = self.second

    def test_fogetPass(self, remove_file):
        self.driver.get(
            "https://edu.10086.cn/sso/password/show/1?service=http%3a%2f%2fedu.10086.cn%2fcloud%2flogin%2flogin")
        self.countTiming()
        self.f.write('test_fogetPass=%.2f\n' % self.second)
        self.f.close()
        self.load_time['test_fogetPass'] = self.second

    def test_login(self, remove_file):
        self.login()
        self.countTiming()
        self.f.write('test_login=%.2f\n' % self.second)
        self.f.close()
        self.load_time['test_login'] = self.second

    def test_jxhd(self, remove_file):
        self.login()    # 校讯通用户登录
        self.driver.find_element(By.XPATH, "//li[@data-name='interaction']/a").click()  # 点击首页家校互动
        self.countTiming()  # 调用封装的计时方法
        self.f.write('test_jxhd=%.2f\n' % self.second)  # 保存测试数据至本地文件，实现数据持久化
        self.f.close()
        self.load_time['test_jxhd'] = self.second   # 保存测试数据至字典中，用于后续判断是否需要触发邮件发送

    def test_eduNews(self, remove_file):
        self.login()
        self.driver.get("http://edu.10086.cn/cloud/index/activictylist")
        self.countTiming()
        self.f.write('test_eduNews=%.2f\n' % self.second)
        self.f.close()
        self.load_time['test_eduNews'] = self.second

    def test_appCenter(self, remove_file):
        self.login()
        self.driver.get("http://edu.10086.cn/cloud/newApp/findPGroupList")
        self.countTiming()
        self.f.write('test_appCenter=%.2f\n' % self.second)
        self.f.close()
        self.load_time['test_appCenter'] = self.second

    def test_personalCenter(self, remove_file):
        self.login()
        self.driver.find_element(By.XPATH, "//li[@class='ali persionLogo']//img").click()
        self.countTiming()
        self.f.write('test_personalCenter=%.2f\n' % self.second)
        self.f.close()
        self.load_time['test_personalCenter'] = self.second

    def test_liveIndex(self, remove_file):
        self.driver.get("http://edu.10086.cn/cloud/liveClassroom/redirectLive?type=live_Index")
        self.countTiming()
        self.f.write('test_liveIndex=%.2f\n' % self.second)
        self.f.close()
        self.load_time['test_liveIndex'] = self.second

    def test_liveDetail(self, remove_file):
        self.driver.get("http://edu.10086.cn/cloud/liveClassroom/redirectLive?type=live_detail&courseId=5193058")
        self.countTiming()
        self.f.write('test_liveDetail=%.2f\n' % self.second)
        self.f.close()
        self.load_time['test_liveDetail'] = self.second

    def teardown(self):
        self.driver.quit()

    # 另一种方法算页面加载时间 用performance.timing
    # def test_NewApi(self):
    #     # timing = performance.timing
    #     self.driver.get("http://edu.10086.cn")
    #     data = self.driver.execute_script("return window.performance.timing;")
    #     print(data['test_NewApi'] - data['navigationStart'])

    def countTiming(self):
        data = self.driver.execute_script("return window.performance.getEntries();")
        self.second = round(data[0]['duration'] / 1000, 2)
        self.f = open(self._loadtimeResultPath, 'a+', encoding='utf-8')

    # 万能验证码生成规则：md5(日期+盐)的后四位 如 20200426K315*p#q的md5值的最后4位
    def getCheckCode(self):
        today = date.today().strftime('%Y%m%d')
        str1 = today + "K315*p#q"
        input_name = hashlib.md5()
        input_name.update(str1.encode("utf-8"))
        return input_name.hexdigest()[-4:]

    def isTestSuccess(self):
        # print(self.load_time)
        if self.load_time['test_index'] > self.test_index_expectTime or \
                self.load_time['test_tologin'] > self.test_tologin_expectTime or \
                self.load_time['test_signup'] > self.test_signup_expectTime or \
                self.load_time['test_fogetPass'] > self.test_fogetPass_expectTime or \
                self.load_time['test_login'] > self.test_login_expectTime or \
                self.load_time['test_jxhd'] > self.test_jxhd_expectTime or \
                self.load_time['test_eduNews'] > self.test_eduNews_expectTime or \
                self.load_time['test_appCenter'] > self.test_appCenter_expectTime or \
                self.load_time['test_personalCenter'] > self.test_personalCenter_expectTime or \
                self.load_time['test_liveIndex'] > self.test_liveIndex_expectTime or \
                self.load_time['test_liveDetail'] > self.test_liveDetail_expectTime:
            self.f = open(self._loadtimeResultPath, 'a+', encoding='utf-8')
            self.f.write('fail')
            self.f.close()

    def teardown_class(self):
        self.isTestSuccess(self)
