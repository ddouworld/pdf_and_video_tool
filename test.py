# Form implementation generated from reading ui file 'D:\tools\python_tool\test.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(parent=self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 811, 601))
        self.tabWidget.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.pushButton = QtWidgets.QPushButton(parent=self.tab)
        self.pushButton.setGeometry(QtCore.QRect(70, 50, 131, 71))
        self.pushButton.setObjectName("pushButton")
        self.label = mylabel2(parent=self.tab)
        self.label.setGeometry(QtCore.QRect(0, 170, 791, 111))
        self.label.setStyleSheet("background:rgb(255, 255, 255)")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = mylabel(parent=self.tab)
        self.label_2.setGeometry(QtCore.QRect(0, 320, 801, 251))
        self.label_2.setStyleSheet("background:rgb(255, 255, 255)")
        self.label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.pushButton_2 = QtWidgets.QPushButton(parent=self.tab)
        self.pushButton_2.setGeometry(QtCore.QRect(100, 140, 81, 24))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_3 = QtWidgets.QLabel(parent=self.tab)
        self.label_3.setGeometry(QtCore.QRect(150, 520, 481, 20))
        self.label_3.setObjectName("label_3")
        self.pushButton_3 = QtWidgets.QPushButton(parent=self.tab)
        self.pushButton_3.setGeometry(QtCore.QRect(540, 20, 141, 71))
        self.pushButton_3.setObjectName("pushButton_3")
        self.lineEdit = QtWidgets.QLineEdit(parent=self.tab)
        self.lineEdit.setGeometry(QtCore.QRect(550, 140, 161, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.label_4 = QtWidgets.QLabel(parent=self.tab)
        self.label_4.setGeometry(QtCore.QRect(410, 140, 121, 20))
        self.label_4.setObjectName("label_4")
        self.direct_checkBox = QtWidgets.QCheckBox(parent=self.tab)
        self.direct_checkBox.setGeometry(QtCore.QRect(470, 110, 79, 20))
        self.direct_checkBox.setObjectName("direct_checkBox")
        self.pushButton.raise_()
        self.label.raise_()
        self.label_2.raise_()
        self.pushButton_2.raise_()
        self.pushButton_3.raise_()
        self.lineEdit.raise_()
        self.label_4.raise_()
        self.label_3.raise_()
        self.direct_checkBox.raise_()
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.video_label = video(parent=self.tab_2)
        self.video_label.setGeometry(QtCore.QRect(0, 310, 811, 261))
        self.video_label.setStyleSheet("background:rgb(255, 255, 255)")
        self.video_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.video_label.setObjectName("video_label")
        self.pushButton_4 = QtWidgets.QPushButton(parent=self.tab_2)
        self.pushButton_4.setGeometry(QtCore.QRect(80, 40, 171, 41))
        self.pushButton_4.setObjectName("pushButton_4")
        self.checkBox = QtWidgets.QCheckBox(parent=self.tab_2)
        self.checkBox.setGeometry(QtCore.QRect(270, 150, 79, 20))
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName("checkBox")
        self.video_water_label = video_water(parent=self.tab_2)
        self.video_water_label.setGeometry(QtCore.QRect(0, 180, 771, 81))
        self.video_water_label.setStyleSheet("background:rgb(255, 255, 255)")
        self.video_water_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.video_water_label.setObjectName("video_water_label")
        self.lineEdit_2 = QtWidgets.QLineEdit(parent=self.tab_2)
        self.lineEdit_2.setGeometry(QtCore.QRect(590, 90, 113, 21))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_7 = QtWidgets.QLabel(parent=self.tab_2)
        self.label_7.setGeometry(QtCore.QRect(460, 90, 121, 21))
        self.label_7.setObjectName("label_7")
        self.pushButton_5 = QtWidgets.QPushButton(parent=self.tab_2)
        self.pushButton_5.setGeometry(QtCore.QRect(540, 10, 141, 41))
        self.pushButton_5.setObjectName("pushButton_5")
        self.scale_size = QtWidgets.QLineEdit(parent=self.tab_2)
        self.scale_size.setGeometry(QtCore.QRect(130, 160, 113, 20))
        self.scale_size.setObjectName("scale_size")
        self.label_8 = QtWidgets.QLabel(parent=self.tab_2)
        self.label_8.setGeometry(QtCore.QRect(40, 160, 81, 20))
        self.label_8.setObjectName("label_8")
        self.checkBox_2 = QtWidgets.QCheckBox(parent=self.tab_2)
        self.checkBox_2.setGeometry(QtCore.QRect(270, 120, 79, 20))
        self.checkBox_2.setObjectName("checkBox_2")
        self.x_label = QtWidgets.QLabel(parent=self.tab_2)
        self.x_label.setGeometry(QtCore.QRect(40, 100, 81, 20))
        self.x_label.setObjectName("x_label")
        self.y_label = QtWidgets.QLabel(parent=self.tab_2)
        self.y_label.setGeometry(QtCore.QRect(40, 130, 81, 20))
        self.y_label.setObjectName("y_label")
        self.x_lineEdit = QtWidgets.QLineEdit(parent=self.tab_2)
        self.x_lineEdit.setGeometry(QtCore.QRect(130, 100, 113, 20))
        self.x_lineEdit.setObjectName("x_lineEdit")
        self.y_lineEdit = QtWidgets.QLineEdit(parent=self.tab_2)
        self.y_lineEdit.setGeometry(QtCore.QRect(130, 130, 113, 20))
        self.y_lineEdit.setObjectName("y_lineEdit")
        self.interval_lineEdit = QtWidgets.QLineEdit(parent=self.tab_2)
        self.interval_lineEdit.setGeometry(QtCore.QRect(590, 120, 113, 20))
        self.interval_lineEdit.setObjectName("interval_lineEdit")
        self.interval_label = QtWidgets.QLabel(parent=self.tab_2)
        self.interval_label.setGeometry(QtCore.QRect(470, 120, 91, 20))
        self.interval_label.setObjectName("interval_label")
        self.duration_label = QtWidgets.QLabel(parent=self.tab_2)
        self.duration_label.setGeometry(QtCore.QRect(470, 150, 101, 20))
        self.duration_label.setObjectName("duration_label")
        self.duration_lineEdit = QtWidgets.QLineEdit(parent=self.tab_2)
        self.duration_lineEdit.setGeometry(QtCore.QRect(590, 150, 113, 20))
        self.duration_lineEdit.setObjectName("duration_lineEdit")
        self.direct_video_checkBox = QtWidgets.QCheckBox(parent=self.tab_2)
        self.direct_video_checkBox.setGeometry(QtCore.QRect(480, 60, 79, 20))
        self.direct_video_checkBox.setObjectName("direct_video_checkBox")
        self.label_5 = QtWidgets.QLabel(parent=self.tab_2)
        self.label_5.setGeometry(QtCore.QRect(190, 505, 301, 31))
        self.label_5.setObjectName("label_5")
        self.tabWidget.addTab(self.tab_2, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "运行加水印"))
        self.label.setText(_translate("MainWindow", "获取到的默认pdf为:"))
        self.label_2.setText(_translate("MainWindow", "将需要加水印的pdf文件或者要删除的pdf文件或者文件夹拖动到这里"))
        self.pushButton_2.setText(_translate("MainWindow", "获取默认水印"))
        self.label_3.setText(_translate("MainWindow", "进度:"))
        self.pushButton_3.setText(_translate("MainWindow", "运行加广告页"))
        self.lineEdit.setText(_translate("MainWindow", "0"))
        self.label_4.setText(_translate("MainWindow", "删除或要插入的的页数"))
        self.direct_checkBox.setText(_translate("MainWindow", "直接插入"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "pdf处理"))
        self.video_label.setText(_translate("MainWindow", "将视频文件拖入到此处"))
        self.pushButton_4.setText(_translate("MainWindow", "运行加水印"))
        self.checkBox.setText(_translate("MainWindow", "随机水印"))
        self.video_water_label.setText(_translate("MainWindow", "将水印文件或者广告视频文件拖动到此处"))
        self.label_7.setText(_translate("MainWindow", "从第多少秒开始删除"))
        self.pushButton_5.setText(_translate("MainWindow", "加入广告视频"))
        self.label_8.setText(_translate("MainWindow", "水印缩放比例:"))
        self.checkBox_2.setText(_translate("MainWindow", "固定水印"))
        self.x_label.setText(_translate("MainWindow", "固定水印x坐标:"))
        self.y_label.setText(_translate("MainWindow", "固定水印y坐标:"))
        self.interval_label.setText(_translate("MainWindow", "间隔显示时间"))
        self.duration_label.setText(_translate("MainWindow", "每次显示多少秒"))
        self.direct_video_checkBox.setText(_translate("MainWindow", "直接插入"))
        self.label_5.setText(_translate("MainWindow", "进度:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "视频处理"))
from mylabel import mylabel
from mylabel2 import mylabel2
from video import video
from video_water import video_water