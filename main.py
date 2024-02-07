import os
from PyQt6.QtWidgets import (
    QApplication, QDialog, QPushButton, QHBoxLayout, QMessageBox,QMainWindow
)
from My_Thread import *
from test import Ui_MainWindow,QtWidgets
import sys
from file.file import *
from pdf_tool.tool import *
from config import *
add_water_video_thread_list = []
add_watermark_thread_list = []
delete_pdf_page_list = []
delete_video_thread_list = []
def get_water_pdf():
    try:
        path = os.getcwd()
        path =path+'\\water_pdf'
        print(path)
        if os.path.exists(path):
            pdf_list = get_dir(path)
            str1 = ""
            for pdf in pdf_list:
                h,w = get_pdf_size(pdf)
                if(h>w):
                    str1 += "A4水印:"+pdf+"\n"
                    ui.label.A4path = pdf
                else:
                    str1 += "ppt水印:" + pdf + "\n"
                    ui.label.pptpath = pdf
            ui.label.setText(str1)
        else:
            os.makedirs(path)
            QMessageBox.information(mainWindow,'信息','不存在water_pdf文件夹。请将水印文件放到water_pdf',QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    except Exception as e:
        print(e)
def add_watermark():
    path_list = ui.label_2.path
    pdf_num = len(path_list)
    num = 1
    global add_watermark_thread_list
    thread_list = add_watermark_thread_list
    if add_watermark_thread_list !=[]:
        QMessageBox.information(mainWindow, '信息', '水印正在添加，请等待',
                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        return
    ui.progressBar.setValue(0)
    ui.progressBar.setRange(0, pdf_num)
    for path in path_list:
        add_watermark_thread = My_Thread(mainWindow, ui, "add_watermark")
        add_watermark_thread.finishSignal.connect(Change_pdf)
        add_watermark_thread.set_add_watermark_path(path, ui.label.A4path,ui.label.pptpath,num)
        add_watermark_thread.start()
        thread_list.append(add_watermark_thread)

        num+=1
    QMessageBox.information(mainWindow, '信息', '完成',
                            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
def delete_pdf_page_():
    num = ui.lineEdit.text()
    try:
        global delete_pdf_page_list
        thread_list = delete_pdf_page_list
        if delete_pdf_page_list != []:
            QMessageBox.information(mainWindow, '信息', '操作正在进行，请等待',
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            return
        num = int(num)
        ui.progressBar_2.setValue(0)
        delete_num = ui.delete_num_lineEdit.text()
        delete_num = int(delete_num)
        path_list = ui.label_pdf_path.path
        pdf_num = len(path_list)
        ui.progressBar_2.setRange(0,pdf_num)
        for path in path_list:
            if(not ui.direct_checkBox.isChecked()):
                if(get_pdf_type(path)):
                    delete_pdf_page_thread = My_Thread(mainWindow, ui, "delete_pdf_page_a4")
                    delete_pdf_page_thread.finishSignal.connect(Change_delete_pdf)
                    delete_pdf_page_thread.set_delete_pdf_page_path(path, ui.label_pdf_ad.A4path, ui.label_pdf_ad.pptpath,num,delete_num,True)
                    delete_pdf_page_thread.start()
                    thread_list.append(delete_pdf_page_thread)
                else:
                    delete_pdf_page_thread = My_Thread(mainWindow, ui, "delete_pdf_page_ppt")
                    delete_pdf_page_thread.finishSignal.connect(Change_delete_pdf)
                    delete_pdf_page_thread.set_delete_pdf_page_path(path, ui.label_pdf_ad.A4path, ui.label_pdf_ad.pptpath, num,
                                                                    delete_num,True)
                    delete_pdf_page_thread.start()
                    thread_list.append(delete_pdf_page_thread)
            else:
                if (get_pdf_type(path)):
                    delete_pdf_page_thread = My_Thread(mainWindow, ui, "delete_pdf_page_a4")
                    delete_pdf_page_thread.finishSignal.connect(Change_delete_pdf)
                    delete_pdf_page_thread.set_delete_pdf_page_path(path, ui.label_pdf_ad.A4path, ui.label_pdf_ad.pptpath, num,
                                                                    delete_num, False)
                    delete_pdf_page_thread.start()
                    thread_list.append(delete_pdf_page_thread)

                else:
                    delete_pdf_page_thread = My_Thread(mainWindow, ui, "delete_pdf_page_ppt")
                    delete_pdf_page_thread.finishSignal.connect(Change_delete_pdf)
                    delete_pdf_page_thread.set_delete_pdf_page_path(path, ui.label_pdf_ad.A4path, ui.label_pdf_ad.pptpath, num,
                                                                    delete_num, False)
                    delete_pdf_page_thread.start()
                    thread_list.append(delete_pdf_page_thread)
        QMessageBox.information(mainWindow, '信息', '完成',
                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    except:
        QMessageBox.information(mainWindow, '信息', '无法解析输入的页数，请检查输入的要删除的页数',
                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
def add_water_video():
    try:
        global add_water_video_thread_list
        if add_water_video_thread_list != []:
            QMessageBox.information(mainWindow, '信息', '水印正在添加，请等待',
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            return
        add_water_video_thread_list = []
        scale_size = ui.scale_size.text() #固定水印的缩放比例
        scale_size = float(scale_size) #缩放比例
        water_path = ui.video_water_label.water_path #固定水印的文件路径
        random_water_path = ui.video_water_label_3.water_path
        show_every_seconds = float(ui.interval_lineEdit.text()) #固定水印的间隔时间
        show_duration_seconds = float(ui.duration_lineEdit.text()) #固定水印的持续时间
        ui.progressBar_3.setValue(0)
        mp4_path_list = ui.video_label.mp4path
        ui.progressBar_3.setRange(0, len(mp4_path_list))
        num =1
        for video_path in mp4_path_list:
            if(ui.checkBox_2.isChecked() and ui.checkBox.isChecked()):
                scale_size_random = ui.scale_size_2.text()
                scale_size_random = float(scale_size_random)  # 缩放比例
                show_every_seconds_random = float(ui.interval_lineEdit_2.text())  # 随机水印的水印间隔时间
                show_duration_seconds_random = float(ui.duration_lineEdit_2.text())  # 随机水印的水印持续时间
                data = {}
                data['video_path'] = video_path
                data['random_water_path'] = random_water_path
                data['fix_water_path'] = water_path
                data['scale_size_random'] = scale_size_random
                data['scale_size_fix'] = scale_size
                data['show_every_seconds_random'] = show_every_seconds_random
                data['show_every_seconds_fix'] = show_every_seconds
                data['show_duration_seconds_random'] = show_duration_seconds_random
                data['show_duration_seconds_fix'] = show_duration_seconds
                x = int(ui.x_lineEdit.text())  # 水印的x坐标
                y = int(ui.y_lineEdit.text())  # 水印的y坐标
                data['x'] = x
                data['y'] = y
                fixed_and_random_watermarking_thread = My_Thread(mainWindow, ui, "fixed_and_random_watermarking")
                fixed_and_random_watermarking_thread.finishSignal.connect(Change_video)
                fixed_and_random_watermarking_thread.set_add_water_video_path("","","","","","","","",data)
                fixed_and_random_watermarking_thread.start()
                add_water_video_thread_list.append(fixed_and_random_watermarking_thread)
                #fixed_and_random_watermarking(data)
                # fixed_watermarking_thread = My_Thread(mainWindow, ui, "fixed_watermarking")
                # fixed_watermarking_thread.finishSignal.connect(Change_video)
                # fixed_watermarking_thread.set_add_water_video_path(video_path,water_path,scale_size,show_every_seconds, show_duration_seconds,x,y,num,random_data)
                # fixed_watermarking_thread.start()
                # add_water_video_thread_list.append(fixed_watermarking_thread)

            elif ui.checkBox_2.isChecked():#判断是否是固定水印
                x = int(ui.x_lineEdit.text())  # 水印的x坐标
                y = int(ui.y_lineEdit.text())  # 水印的y坐标
                fixed_watermarking_thread = My_Thread(mainWindow, ui, "fixed_watermarking")
                fixed_watermarking_thread.finishSignal.connect(Change_video)
                fixed_watermarking_thread.set_add_water_video_path(video_path, water_path, scale_size,
                                                                   show_every_seconds, show_duration_seconds, x, y, num,"")
                fixed_watermarking_thread.start()
                add_water_video_thread_list.append(fixed_watermarking_thread)
            elif ui.checkBox.isChecked():
                scale_size_random = ui.scale_size_2.text()
                scale_size_random = float(scale_size_random)  # 缩放比例
                show_every_seconds_random = float(ui.interval_lineEdit_2.text())  # 随机水印的水印间隔时间
                show_duration_seconds_random = float(ui.duration_lineEdit_2.text())  # 随机水印的水印持续时间
                x = int(ui.x_lineEdit.text())  # 水印的x坐标
                y = int(ui.y_lineEdit.text())  # 水印的y坐标
                random_watermarking_thread = My_Thread(mainWindow, ui, "random_watermarking")
                random_watermarking_thread.finishSignal.connect(Change_video)
                random_watermarking_thread.set_add_water_video_path(video_path, random_water_path, scale_size_random,
                                                                    show_every_seconds_random, show_duration_seconds_random, x, y,
                                                                    num,"")
                random_watermarking_thread.start()
                add_water_video_thread_list.append(random_watermarking_thread)
                # random_watermarking_thread.wait()
        num+=1
        QMessageBox.information(mainWindow, '信息', '正在添加水印',
                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    except Exception as e:
        print(e)
        QMessageBox.information(mainWindow, '信息', '请检查输入数据是否正确',
                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
def delete_video():
    try:
        global delete_video_thread_list
        if delete_video_thread_list != []:
            QMessageBox.information(mainWindow, '信息', '操作正在进行，请等待',
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            return
        thread_list = delete_video_thread_list
        delete_time = ui.lineEdit_2.text()
        delete_time = int(delete_time)
        need_delete_time = ui.delete_s_lineEdit.text()
        need_delete_time = int(need_delete_time)
        ad_path = ui.video_water_label_2.water_path
        num=1
        ui.progressBar_4.setValue(0)
        mp4_path_list = ui.video_label_2.mp4path
        ui.progressBar_4.setRange(0, len(mp4_path_list))
        for video_path in ui.video_label_2.mp4path:
            if ui.direct_video_checkBox.isChecked():
                delete_video_time_thread = My_Thread(mainWindow, ui, "delete_video_time")
                delete_video_time_thread.finishSignal.connect(Change_video_ad)
            # 启动线程，执行线程类中run函数
                delete_video_time_thread.set_delete_video_time_path(video_path,ad_path,delete_time,num,need_delete_time)
                delete_video_time_thread.start()
                thread_list.append(delete_video_time_thread)
            else:
                delete_video_time_2_thread = My_Thread(mainWindow, ui, "delete_video_time_2")  # 实例化一个线程，参数t设置为100
                # 将线程thread的信号finishSignal和UI主线程中的槽函数Change进行连接
                delete_video_time_2_thread.finishSignal.connect(Change_video_ad)
                delete_video_time_2_thread.set_delete_video_time_path(video_path,ad_path,delete_time,num)
                delete_video_time_2_thread.start()
                thread_list.append(delete_video_time_2_thread)
            num+=1
        QMessageBox.information(mainWindow, '信息', '正在添加广告',
                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    except Exception as e:
        print(e)
        QMessageBox.information(mainWindow, '信息', '请检查输入数据是否正确',
                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
def Change_video(msg):
        miValue = ui.progressBar_3.value()
        ui.progressBar_3.setValue(int(miValue) + 1)
        if ui.progressBar_3.maximum() == int(miValue) + 1:
            global add_water_video_thread_list
            add_water_video_thread_list = []
            # if msg == '1':
            #     mp4_path_list = ui.video_label.mp4path
            #     for video_path in mp4_path_list :
            #         try:
            #             time.sleep(1)
            #             print("尝试删除缓存")
            #             os.remove(video_path[:-4] + "_1.mp4")
            #             os.rename(video_path[:-4] + "_2.mp4", video_path[:-4] + "_1.mp4")#重命名，将加了随机水印和固定水印的_2重命名为_1
            #         except:
            #             print("视频占用中，删除失败")


def Change_pdf(num):
    # print(num)
    miValue = ui.progressBar.value()

    ui.progressBar.setValue(int(miValue)+1)
    if ui.progressBar.maximum() == int(miValue) + 1:
        global add_watermark_thread_list
        add_watermark_thread_list = []


def Change_delete_pdf():
    miValue = ui.progressBar_2.value()
    ui.progressBar_2.setValue(int(miValue) + 1)
    if ui.progressBar_2.maximum() == int(miValue) + 1:
        global delete_pdf_page_list
        delete_pdf_page_list = []
def Change_video_ad(msg):
    # print(msg)
    miValue = ui.progressBar_4.value()
    ui.progressBar_4.setValue(int(miValue) + 1)
    if ui.progressBar_4.maximum() == int(miValue) + 1:
        global delete_video_thread_list
        delete_video_thread_list = []
def close_event(event):
    pdf_line = ui.lineEdit.text()
    pdf_delete_num = ui.delete_num_lineEdit.text()
    pdf_ad_ppt = ui.label_pdf_ad.pptpath
    pdf_ad_a4 = ui.label_pdf_ad.A4path

    video_x = ui.x_lineEdit.text()
    video_y = ui.y_lineEdit.text()
    scale_size = ui.scale_size.text()
    interval = ui.interval_lineEdit.text()
    duration = ui.duration_lineEdit.text()
    video_water = ui.video_water_label.water_path
    video_water_3 = ui.video_water_label_3.water_path

    scale_size_2 = ui.scale_size.text()
    interval_2 = ui.interval_lineEdit.text()
    duration_2 = ui.duration_lineEdit.text()
    video_ad_line = ui.lineEdit_2.text()
    video_ad_delete = ui.delete_s_lineEdit.text()
    video_ad_water = ui.video_water_label_2.water_path
    data = {"pdf_line":pdf_line,"pdf_delete_num":pdf_delete_num,"pdf_ad_ppt":pdf_ad_ppt,"pdf_ad_a4":pdf_ad_a4,"video_x":video_x,"video_y":video_y,"scale_size":scale_size,"interval":interval,"duration":duration,"video_water":video_water,"video_water_3":video_water_3,"scale_size_2":scale_size_2,"interval_2":interval_2,"duration_2":duration_2,"video_ad_line":video_ad_line,"video_ad_delete":video_ad_delete,"video_ad_water":video_ad_water}
    config = Config()
    config.set_config(data)
def check_is_empty(data,str1):
    if(data==''):
        return str1
    else:
        return data
def set_config():
    #to do
    #当上一次保存失败，为空的时候
    config = Config()
    data = config.get_config()
    if(data!=''):
        ui.lineEdit.setText(data['pdf_line'])
        ui.delete_num_lineEdit.setText(data['pdf_delete_num'])
        if data['pdf_ad_ppt']!="":
            ui.label_pdf_ad.setText(check_is_empty(data['pdf_ad_ppt'],"获取到的广告pdf:"))
        else:
            ui.label_pdf_ad.setText(check_is_empty(data['pdf_ad_a4'],"获取到的广告pdf:"))
        ui.x_lineEdit.setText(data['video_x'])
        ui.y_lineEdit.setText(data['video_y'])
        ui.scale_size.setText(data['scale_size'])
        ui.interval_lineEdit.setText(data['interval'])
        ui.duration_lineEdit.setText(data['duration'])
        ui.video_water_label.setText(check_is_empty(data['video_water'],"将固定水印放到此处"))
        ui.video_water_label_3.setText(check_is_empty(data['video_water_3'],"将随机水印放到此处"))
        ui.video_water_label.water_path = data['video_water']
        ui.video_water_label_3.water_path = data['video_water_3']


        ui.scale_size_2.setText(data['scale_size_2'])
        ui.interval_lineEdit_2.setText(data['interval_2'])
        ui.duration_lineEdit_2.setText(data['duration_2'])
        ui.lineEdit_2.setText(data['video_ad_line'])
        ui.delete_s_lineEdit.setText(data['video_ad_delete'])
        ui.video_water_label_2.setText(check_is_empty(data['video_ad_water'],"将广告视频文件放到此处"))
        ui.video_water_label_2.water_path = data['video_ad_water']

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)  # 创建一个QApplication，也就是你要开发的应用程序
    mainWindow = QtWidgets.QMainWindow()  # 创建一个QMainWindow，用来装载你需要的各种组件、控件
    ui = Ui_MainWindow()  # ui是你创建的ui类的实例化对象，这里调用的便是刚才生成的register.py中的Ui_MainWindow类
    ui.setupUi(mainWindow)  # 执行类中的setupUi方法，方法的参数是第二步中创建的QMainWindow
    set_config()
    ui.pushButton_2.clicked.connect(get_water_pdf)
    ui.pushButton.clicked.connect(add_watermark)
    ui.pushButton_3.clicked.connect(delete_pdf_page_)
    ui.pushButton_4.clicked.connect(add_water_video)
    ui.pushButton_5.clicked.connect(delete_video)
    mainWindow.show()  # 执行QMainWindow的show()方法，显示这个QMainWindow
    mainWindow.closeEvent =close_event
    sys.exit(app.exec())  # 使用exit()或者点击关闭按钮退出QApplication