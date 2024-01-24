from PyQt6.QtWidgets import (
    QLabel,QMessageBox
)
from file.file import *
class video_water(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.water_path = ""
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
                    QMessageBox.information(self, '信息', '请直接拖入单个文件',
                                            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                elif(file_type==0):
                        self.water_path = file.toLocalFile()
                else:
                    self.setText(file.toLocalFile()+"无法识别文件类型")
                    break
        self.setText("获取的视频文件路径{}".format(self.water_path))