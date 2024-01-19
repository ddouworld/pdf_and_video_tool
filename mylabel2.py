from PyQt6.QtWidgets import (
    QLabel
)
from file.file import *
from pdf_tool.tool import *
class mylabel2(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.A4path = ""
        self.pptpath = ""
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
        if event.mimeData().hasUrls():
            files = event.mimeData().urls()
            for file in files:
                file_type = check_path(file.toLocalFile())
                if(file_type==1):
                    path_list = get_dir(file.toLocalFile())#获取文件夹下所有pdf文件
                    for pdf in path_list:
                        if(get_pdf_type(pdf)==1):
                            self.A4path = pdf
                        else:
                            self.pptpath = pdf
                elif(file_type==0):
                    if(check_pdf(file.toLocalFile())):
                        if(get_pdf_type(file.toLocalFile())):
                            self.A4path = file.toLocalFile()
                        else:
                            self.pptpath = file.toLocalFile()
                else:
                    self.setText(file.toLocalFile()+"无法识别文件类型")
                    break
        str1 = "A4水印:"+self.A4path+"\n"+"ppt水印"+self.pptpath
        self.setText(str1)