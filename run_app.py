from WechatPCAPI import WechatPCAPI
from WeChat_from_web import action_Submit
import time
import logging
from queue import Queue
import threading,os

# 监听群名
group_receive_list = ['程序测试']
#group_receive_list = ['03 HW-2020值守及应急处置工作群']

#初始化程序
logging.basicConfig(level=logging.INFO)
queue_recved_message = Queue()

#将消息送进队列
def on_message(message):
    queue_recved_message.put(message)


#线程控制台
def thread_handle_message(wx_inst,app,xml_path):
    # 线程指针
    One_Status=True

    while True:
        #取到所有消息队列
        message = queue_recved_message.get()
        #print("微信实时接收到的信息：-----------------------------" +str(message))

        # 消息对列取出群名
        from_chatroom_nickname = message.get(
            'data', {}).get('from_chatroom_nickname', '')

        # 消息对列取出消息
        from_chatroom_nickname_msg=message.get(
            'data', {}).get('msg', '')

        #判断是否是我们想监听的群  不是不处理
        if from_chatroom_nickname in group_receive_list:
            #判断消息xml文件是否包含url 并可访问
            try:
                if not from_chatroom_nickname_msg.find('<?xml version="1.0"?>'):
                    print(">>>>>>>>>接收到过滤URL--->>>>>>>正在保存！--->>>>>>>准备填表>>>>>>>>>>>>")
                    #将消息保存成xml
                    if not os.path.isfile(xml_path):
                            app.Start_saver_xml(from_chatroom_nickname_msg,xml_path)
                            #app.setDaemon(True)
                            print("开始填表！")
                            if One_Status:
                                app.start()
                                app.join()
                                app.pause()
                                One_Status=False
                            print("文件是否存-1：",os.path.isfile(xml_path))
                            if not os.path.isfile(xml_path):
                                app.pause()
                            if os.path.isfile(xml_path):
                                app.resume()
                            print("文件是否-2：", os.path.isfile(xml_path))


                print("监听工作群接收的信息：---->>>" +str(from_chatroom_nickname_msg))
                print("继续等待接收消息 -----------------------!")
            except Exception as e:
                print("代码运行出错： ERROR", format(e))

#主方法
def main():
    xml_path='C:\\Program Files\\Microsoft Games\\WeChat_app\\cache_msg.xml'
    Images_path = 'C:\\Program Files\\Microsoft Games\\WeChat_app\\images\\'
    chrome_path = 'C:\\Program Files\\Microsoft Games\\WeChat_app\\chromedriver.exe'

    wx_inst = WechatPCAPI(on_message=on_message, log=logging)
    wx_inst.start_wechat(block=True)
    while not wx_inst.get_myself():
        time.sleep(5)
        print('登陆成功')
        #填表应用
        app = action_Submit(files_path=xml_path, Images_path=Images_path, chrome_path=chrome_path)
        #微信监听app
        threading.Thread(target=thread_handle_message, args=(wx_inst,app,xml_path)).start()
        time.sleep(5)

#开始运行
if __name__ == '__main__':
    main()