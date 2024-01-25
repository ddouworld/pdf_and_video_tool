# -*- coding: utf-8 -*-
import time
from PyQt6.QtCore import QThread, pyqtSignal
from video_tool.tool import *
from pdf_tool.tool import *
#定义一个线程类
class My_Thread(QThread):
    #自定义信号声明
    # 使用自定义信号和UI主线程通讯，参数是发送信号时附带参数的数据类型，可以是str、int、list等
    finishSignal = pyqtSignal(str)

    # 带一个参数t
    def __init__(self, mainwindow,ui,name,parent=None):
        super(My_Thread,self).__init__(parent)
        self.mainwindow = mainwindow
        self.ui = ui
        self.fun_name =name
        self.delete_video_time = delete_video_time
        self.delete_video_time_2 = delete_video_time_2
        self.fixed_watermarking = fixed_watermarking
        self.random_watermarking = random_watermarking
        self.delete_pdf_page = delete_pdf_page
        self.add_watermark_2 = add_watermark_2

    def set_delete_video_time_path(self,video_path, ad_path, delete_time,num,need_delete_time=600):
        self.video_path = video_path
        self.ad_path = ad_path
        self.delete_time = delete_time
        self.num = num
        self.need_delte_time = need_delete_time
    def set_add_water_video_path(self,video_path,water_path,scale_size,show_every_seconds, show_duration_seconds,x,y,num):
        self.video_path=video_path
        self.water_path = water_path
        self.scale_size = scale_size
        self.show_every_seconds = show_every_seconds
        self.show_duration_seconds = show_duration_seconds
        self.x = x
        self.y = y
        self.num = num
    def set_delete_pdf_page_path(self,path,A4path,num):
        self.pdf_path = path
        self.a4path = A4path
        self.num = num
    def set_add_watermark_path(self,path,a4_path,ppt_path,num):
        self.pdf_path = path
        self.a4path = a4_path
        self.ppt_path = ppt_path
        self.num = num
    def run(self):
        if self.fun_name == "delete_video_time":
            self.finishSignal.emit("正在处理第{}个视频".format(self.num))
            self.delete_video_time(self.video_path,self.ad_path,self.delete_time,self.need_delte_time)
            self.finishSignal.emit("第{}个视频处理完成".format(self.num))
        elif self.fun_name == "delete_video_time_2":
            self.finishSignal.emit("正在处理第{}个视频".format(self.num))
            self.delete_video_time_2(self.video_path, self.ad_path, self.delete_time)
            self.finishSignal.emit("第{}个视频处理完成".format(self.num))
        elif self.fun_name == "fixed_watermarking":
            self.finishSignal.emit("固定水印:正在处理第{}个视频".format(self.num))
            self.fixed_watermarking(self.video_path,self.water_path,self.scale_size,self.show_every_seconds, self.show_duration_seconds,self.x,self.y)
            self.finishSignal.emit("固定水印:第{}个视频处理完成".format(self.num))
        elif self.fun_name=="random_watermarking":
            self.finishSignal.emit("随机添加水印:正在处理第{}个视频".format(self.num))
            random_watermarking(self.video_path, self.water_path, self.scale_size, self.show_every_seconds,
                               self.show_duration_seconds)
            self.finishSignal.emit("随机添加水印:第{}个视频处理完成".format(self.num))
        elif self.fun_name=='delete_pdf_page':
            # to do
            self.finishSignal.emit("删除或者插入pdf操作:正在处理第{}个pdf".format(self.num))
            self.delete_pdf_page(self.pdf_path,self.a4path,self.num,True)
            self.finishSignal.emit("删除或者插入pdf操作:第{}个pdf处理完成".format(self.num))
        elif self.fun_name == 'add_watermark':
            self.finishSignal.emit("添加pdf水印操作:正在处理第{}个pdf".format(self.num))
            self.add_watermark_2(self.pdf_path,self.a4path,self.ppt_path)
            self.finishSignal.emit("添加pdf水印操作:第{}个pdf处理完成".format(self.num))