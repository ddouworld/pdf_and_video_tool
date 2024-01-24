import os
from concurrent.futures import ThreadPoolExecutor
from PyQt6.QtWidgets import (
    QApplication, QDialog, QPushButton, QHBoxLayout, QMessageBox,QMainWindow
)
from My_Thread import *
from test import Ui_MainWindow,QtWidgets
import sys
from file.file import *
from pdf_tool.tool import *
from video_tool.tool import *
def get_water_pdf():
    try:
        path = os.getcwd()
        path =path+'\\water_pdf'
        print(path)
        if os.path.exists(path):
            print("存在")
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
    for path in path_list:
        ui.label_3.setText("总共获取到{}个pdf,正在获取第{}个,正在获取:{}".format(pdf_num,num,path))
        # if(get_pdf_type(path)):
        #     add_watermark_2(path,ui.label.A4path)
        # else:
        #     add_watermark_2(path, ui.label.pptpath)
        # add_watermark_2(path, ui.label.A4path,ui.label.pptpath)
        add_watermark_thread = My_Thread(mainWindow, ui, "add_watermark")
        add_watermark_thread.finishSignal.connect(Change_2)
        add_watermark_thread.set_add_watermark_path(path, ui.label.A4path,ui.label.pptpath,num)
        add_watermark_thread.start()
        # ui.label_3.setText(path+"获取完成")

        num+=1
    QMessageBox.information(mainWindow, '信息', '完成',
                            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
def delete_pdf_page_():
    num = ui.lineEdit.text()
    try:
        num = int(num)
        path_list = ui.label_pdf_path.path
        pdf_num = len(path_list)
        for path in path_list:
            ui.label_6.setText("总共获取到{}个pdf,正在获取第{}个,正在获取:{}".format(pdf_num, num, path))
            if(ui.direct_checkBox.isChecked()):
                if(get_pdf_type(path)):
                    delete_pdf_page(path,ui.label.A4path,num,True)
                else:
                    delete_pdf_page(path, ui.label.pptpath, num,True)
            else:
                if (get_pdf_type(path)):
                    delete_pdf_page(path, ui.label.A4path, num, False)
                else:
                    delete_pdf_page(path, ui.label.pptpath, num, False)
        QMessageBox.information(mainWindow, '信息', '完成',
                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    except:
        QMessageBox.information(mainWindow, '信息', '无法解析输入的页数，请检查输入的要删除的页数',
                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
def add_water_video():
    try:
        scale_size = ui.scale_size.text()
        scale_size = float(scale_size) #缩放比例
        water_path = ui.video_water_label.water_path
        show_every_seconds = float(ui.interval_lineEdit.text())
        show_duration_seconds = float(ui.duration_lineEdit.text())
        num =1
        for video_path in ui.video_label.mp4path:
            if(ui.checkBox_2.isChecked() and ui.checkBox.isChecked()):
                x = int(ui.x_lineEdit.text())  # 水印的x坐标
                y = int(ui.y_lineEdit.text())  # 水印的y坐标
                fixed_watermarking_thread = My_Thread(mainWindow, ui, "fixed_watermarking")
                fixed_watermarking_thread.finishSignal.connect(Change)
                fixed_watermarking_thread.set_add_water_video_path(video_path,water_path,scale_size,show_every_seconds, show_duration_seconds,x,y,num)
                fixed_watermarking_thread.start()

                random_watermarking_thread = My_Thread(mainWindow, ui, "random_watermarking")
                random_watermarking_thread.finishSignal.connect(Change)
                random_watermarking_thread.set_add_water_video_path(video_path[:-4]+"_1.mp4", water_path, scale_size,
                                                                   show_every_seconds, show_duration_seconds, x, y,num)
                random_watermarking_thread.start()
            elif ui.checkBox_2.isChecked():#判断是否是固定水印
                # w,h = get_video_dimensions(video_path)
                x = int(ui.x_lineEdit.text())  # 水印的x坐标
                y = int(ui.y_lineEdit.text())  # 水印的y坐标
                fixed_watermarking_thread = My_Thread(mainWindow, ui, "fixed_watermarking")
                fixed_watermarking_thread.finishSignal.connect(Change)
                fixed_watermarking_thread.set_add_water_video_path(video_path, water_path, scale_size,
                                                                   show_every_seconds, show_duration_seconds, x, y, num)
                fixed_watermarking_thread.start()
            elif ui.checkBox.isChecked():
                x = int(ui.x_lineEdit.text())  # 水印的x坐标
                y = int(ui.y_lineEdit.text())  # 水印的y坐标
                random_watermarking_thread = My_Thread(mainWindow, ui, "random_watermarking")
                random_watermarking_thread.finishSignal.connect(Change)
                random_watermarking_thread.set_add_water_video_path(video_path, water_path, scale_size,
                                                                    show_every_seconds, show_duration_seconds, x, y,
                                                                    num)
                random_watermarking_thread.start()
        num+=1
        QMessageBox.information(mainWindow, '信息', '正在添加水印',
                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    except Exception as e:
        print(e)
        QMessageBox.information(mainWindow, '信息', '请检查输入数据是否正确',
                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
def delete_video():
    print("加广告")
    try:
        delete_time = ui.lineEdit_2.text()
        delete_time = int(delete_time)
        ad_path = ui.video_water_label.water_path
        num=1
        for video_path in ui.video_label.mp4path:
            if ui.direct_video_checkBox.isChecked():
                delete_vidoe_time_thread = My_Thread(mainWindow, ui, "delete_vidoe_time")
                delete_vidoe_time_thread.finishSignal.connect(Change)
            # 启动线程，执行线程类中run函数
                delete_vidoe_time_thread.set_delete_video_time_path(video_path,ad_path,delete_time,num)
                delete_vidoe_time_thread.start()
            else:
                delete_video_time_2_thread = My_Thread(mainWindow, ui, "delete_video_time_2")  # 实例化一个线程，参数t设置为100
                # 将线程thread的信号finishSignal和UI主线程中的槽函数Change进行连接
                delete_video_time_2_thread.finishSignal.connect(Change)
                delete_video_time_2_thread.set_delete_video_time_path(video_path,ad_path,delete_time,num)
                delete_video_time_2_thread.start()
            num+=1
        QMessageBox.information(mainWindow, '信息', '正在添加广告',
                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    except Exception as e:
        print(e)
        QMessageBox.information(mainWindow, '信息', '请检查输入数据是否正确',
                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
def Change(msg):
        print(msg)
        ui.label_5.setText(str(msg))
def Change_2(msg):
    print(msg)
    ui.label_3.setText(str(msg))
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)  # 创建一个QApplication，也就是你要开发的应用程序
    mainWindow = QtWidgets.QMainWindow()  # 创建一个QMainWindow，用来装载你需要的各种组件、控件
    ui = Ui_MainWindow()  # ui是你创建的ui类的实例化对象，这里调用的便是刚才生成的register.py中的Ui_MainWindow类
    ui.setupUi(mainWindow)  # 执行类中的setupUi方法，方法的参数是第二步中创建的QMainWindow
    ui.pushButton_2.clicked.connect(get_water_pdf)
    ui.pushButton.clicked.connect(add_watermark)
    ui.pushButton_3.clicked.connect(delete_pdf_page_)
    ui.pushButton_4.clicked.connect(add_water_video)
    ui.pushButton_5.clicked.connect(delete_video)
    mainWindow.show()  # 执行QMainWindow的show()方法，显示这个QMainWindow
    sys.exit(app.exec())  # 使用exit()或者点击关闭按钮退出QApplication