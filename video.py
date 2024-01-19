from PyQt6.QtWidgets import (
    QLabel
)
from file.file import *
from pdf_tool.tool import *
class video(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.mp4path = []
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
        if (len(self.mp4path)!= 0):
            self.mp4path = []
        if event.mimeData().hasUrls():
            files = event.mimeData().urls()
            for file in files:
                file_type = check_path(file.toLocalFile())
                if(file_type==1):
                    mp4_list = get_dir(file.toLocalFile(),".mp4")#获取文件夹下所有pdf文件
                    for mp4 in mp4_list:
                            self.mp4path.append(mp4)
                elif(file_type==0):
                    if(check_pdf(file.toLocalFile(),'.mp4')):
                        self.mp4path.append(file.toLocalFile())
                else:
                    self.setText(file.toLocalFile()+"无法识别文件类型")
                    break
        self.setText("获取的视频文件个数{}".format(len(self.mp4path)))