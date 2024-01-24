from PyQt6.QtWidgets import (
    QLabel
)
from file.file import *
class mylabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.path = []
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if len(urls) > 0 and urls[0].scheme() == "file":
                event.accept()
            else:
                event.ignore()
        else:
            event.ignore()
    def dropEvent(self, event):
        if(len(self.path)!=0):
            self.path = []
        if event.mimeData().hasUrls():
            files = event.mimeData().urls()
            for file in files:
                file_type = check_path(file.toLocalFile())
                if(file_type==1):
                    path_list = get_dir(file)#获取文件夹下所有pdf文件
                    self.path = self.path+path_list
                elif(file_type==0):
                    if(check_pdf(file.toLocalFile())):
                        self.path.append(file.toLocalFile())
                else:
                    self.setText(file.toLocalFile()+"无法识别文件类型")
                    break
            pdfnum = len(self.path)
            if(pdfnum==1):
                self.setText("获取到的pdf文件为:"+self.path[0])
            else:
                self.setText("总共获取到pdf{}个pdf文件".format(pdfnum))