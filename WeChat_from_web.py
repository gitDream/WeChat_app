from selenium import webdriver
from xml.dom.minidom import parse
import time,os,requests
import threading


#----------------------------提交操作------------------------------------
class action_Submit(threading.Thread):
    def __init__(self,files_path,Images_path,chrome_path):
        super(action_Submit, self).__init__()
        self.files_path=files_path
        self.Images_path=Images_path
        self.chrome_path=chrome_path

        self.daemon = True  # Allow main to exit even if still running.
        self.paused = True  # Start out paused.
        self.state = threading.Condition()

# URL检测站点正常！
    def getHttpStatusCode(self,url):
        try:
            request = requests.get(url)
            httpStatusCode = request.status_code
            return url,httpStatusCode
        except requests.exceptions.HTTPError as e:
            return e

#保证微信消息保存成xml
    def Start_saver_xml(self,msg,file_path):
        msg_files = open(file_path, 'w', encoding='utf-8')
        try:
            msg_files.write(msg)
        except Exception as e:
            msg_files.close()
            print(e)

#提交时并保存图片到目录下
    def saver_images(self):
        file_name  = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime(time.time()))
        dest_dir = self.Images_path+file_name+'.jpg'
        return dest_dir

#main操作方法--------------------------
    def run_main(self,url):
        driver = webdriver.Chrome(self.chrome_path)
        #driver.set_window_size(840, 600)
        driver.maximize_window()
        driver.get(str(url))
        time.sleep(50)

        try:
            ####输入姓名----------ok----------------
            input_text = driver.find_element_by_id("q1")
            input_text.send_keys("陈艺彬")
            driver.get_screenshot_as_file(self.saver_images())
            ####选择系统运行----------ok----------------
            answers = driver.find_elements_by_css_selector('.ui-controlgroup')
            driver.find_elements_by_class_name("ui-checkbox")[50].click()
            driver.find_elements_by_class_name("ui-checkbox")[78].click()
            driver.get_screenshot_as_file(self.saver_images())
            ####选择系统运行状态----------ok----------------
            driver.find_elements_by_class_name("ui-radio")[0].click()
            time.sleep(6)
            btn_reg = driver.find_element_by_id('ctlNext')
            btn_reg.click()
            time.sleep(6)
            driver.get_screenshot_as_file(self.saver_images())

        except Exception as e:
            print("代码运行出错： ERROR", format(e))
            driver.quit()
        ###关闭浏览器窗口----------ok----------------
        time.sleep(8)
        driver.quit()

#线程控制器------------------------------------------------------------
    def resume(self):  # 用来恢复/启动run
        with self.state:  # 在该条件下操作
            self.paused = False
            self.state.notify()  # Unblock self if waiting.

    def pause(self):  # 用来暂停run
        with self.state:  # 在该条件下操作
            self.paused = True  # Block self.

#线程操作主方法
    def run(self):
        while True:
            with self.state:
                if os.path.isfile(self.files_path):
                    count=0
                    while count < 4:
                        DOM_Tree = parse(self.files_path)
                        url = DOM_Tree.getElementsByTagName('url')[0].childNodes[0].data
                        HTTPS_URL,STATUS=self.getHttpStatusCode(url)
                        if STATUS == 200:
                            self.run_main(HTTPS_URL)
                            count+=1
                            time.sleep(30)
                    os.remove(self.files_path)

if __name__ == "__main__":
    #files_path = 'F:\\WeChat_app\\cache_msg.xml'
    #Images_path = 'F:\\WeChat_app\\images\\'
    #chrome_path='F:\\WeChat_app\\chromedriver.exe'

    files_path = 'C:\\Program Files\\Microsoft Games\\WeChat_app\\cache_msg.xml'
    Images_path = 'C:\\Program Files\\Microsoft Games\\WeChat_app\\images\\'
    chrome_path = 'C:\\Program Files\\Microsoft Games\\WeChat_app\\chromedriver.exe'
    app=action_Submit(files_path,Images_path,chrome_path)
    app.start()


