import base64
import os
import sys

from PIL import ImageQt
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QDesktopWidget, QPushButton, \
    QGridLayout, QLabel, QTextEdit, QFileDialog, QMainWindow, qApp, QAction
from PyQt5.QtGui import QIcon, QPixmap
import LSB
from img.icon_png import img as icon_png
from img.lock_png import img as lock_png
from img.unlock_png import img as unlock_png
from img.uptxt_png import img as uptxt_png
class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        #设置窗口大小
        # 显示器像素
        screen = QDesktopWidget().screenGeometry()
        self.screenW = screen.width()
        self.screenH = screen.height()

        self.QWax = 50
        self.QWay = 60
        self.QWaw = self.screenW - 100
        self.QWah = self.screenH - 100
        #初始化图片资源
        Icon = open('icon.png', 'wb')  # 创建临时的文件
        Icon.write(base64.b64decode(icon_png))  ##把这个one图片解码出来，写入文件中去。
        Icon.close()
        Lock = open('lock.png', 'wb')  # 创建临时的文件
        Lock.write(base64.b64decode(lock_png))  ##把这个one图片解码出来，写入文件中去。
        Lock.close()
        Unlock = open('unlock.png', 'wb')  # 创建临时的文件
        Unlock.write(base64.b64decode(unlock_png))  ##把这个one图片解码出来，写入文件中去。
        Unlock.close()
        Uptxt = open('uptxt.png', 'wb')  # 创建临时的文件
        Uptxt.write(base64.b64decode(uptxt_png))  ##把这个one图片解码出来，写入文件中去。
        Uptxt.close()

        self.initUI()#用于绘制界面

    def initUI(self):
        self.setGeometry(self.QWax, self.QWay, self.QWaw, self.QWah)
        self.setWindowTitle('图片隐写@author:HIT-1180301006')
        self.setWindowIcon(QIcon('icon.png'))#设置窗体图标
        #下面三部分设置工具栏工具
        lock = QAction(QIcon('lock.png'), '隐藏文档', self)
        lock.setShortcut('Ctrl+L')
        lock.triggered.connect(self.steghide)

        unlock=QAction(QIcon('unlock.png'),'解密文档',self)
        unlock.setShortcut('Ctrl+U')
        unlock.triggered.connect(self.docdecode)

        opentxt=QAction(QIcon('uptxt.png'),'上传文件',self)
        opentxt.setShortcut('Ctrl+O')
        opentxt.triggered.connect(self.OpenTxTDialog)

        self.toolbar = self.addToolBar('工具栏')
        self.toolbar.addAction(opentxt)
        self.toolbar.addAction(lock)
        self.toolbar.addAction(unlock)

        #主窗口中心是一个QWidget
        main_frame=QWidget()
        #设置QWidget内部控件
        self.textEdit = QTextEdit()
        self.textEdit1=QTextEdit()
        self.imglabel=QLabel()
        self.readtxtbtn=QPushButton('选择隐藏文本')
        self.encodebtn=QPushButton('选择加密图片')
        self.decodebtn=QPushButton('选择解密图片')
        #是设置布局
        self.grid=QGridLayout()
        self.grid.setSpacing(10)
        self.grid.addWidget(self.imglabel,1,1,5,1)
        self.grid.addWidget(self.textEdit,1,2,5,1)
        self.grid.addWidget(self.textEdit1,1,3,5,1)
        main_frame.setLayout(self.grid)
        self.center()
        self.setCentralWidget(main_frame)
        self.show()
    #文本读取
    def OpenTxTDialog(self):
        cwd = os.getcwd() # 获取当前程序文件位置
        fname = QFileDialog.getOpenFileName(self, '选择TXT文档', cwd,'Text Files (*.txt)')
        self.textEdit.clear()
        if fname[0]:
            f = open(fname[0], 'r',encoding='utf-8')
            with f:
                data = f.read()
                self.textEdit.setText(data)
    #退出程序询问
    def closeEvent(self, event):

        reply = QMessageBox.question(self, '退出',
                                     "确认退出吗?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
    #移动到屏幕中心
    def center(self):
        #获得窗口
        qr = self.frameGeometry()
        #获得屏幕中心点
        cp = QDesktopWidget().availableGeometry().center()
        #显示到屏幕中心
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    #加密算法
    def steghide(self):
        str=self.textEdit.toPlainText()#获取到文本内容
        if(not str):
            QMessageBox.about(self,'提示','要输入加密的文本或者从本地上传TXT文件')
            return
        #这里使用窗口选择图片
        fname = QFileDialog.getOpenFileName(self, '选择一张图片', './', ("Images (*.png *.jpg *.bmp *.jpeg)"))
        if fname[0]:
            cwd = os.getcwd() # 获取当前程序文件位置
            # with Image.open(fname[0]) as img:
            pixmap = QPixmap(fname[0])
            #先转化为Qimag然后转化为Image
            image = ImageQt.fromqpixmap(pixmap)
            print(type(image))
            LSB.encodeDataInImage(image, str).save(cwd + '/output.png')
            self.imglabel.setPixmap(pixmap)
            QMessageBox.about(self,'成功','文件已经藏好咯')
    #解密文档
    def docdecode(self):
        # 这里使用窗口选择图片
        fname = QFileDialog.getOpenFileName(self, '选择一张图片', './', ("Images (*.png *.jpg *.bmp *.jpeg)"))
        if fname[0]:
            cwd = os.getcwd()  # 获取当前程序文件位置
            # with Image.open(fname[0]) as img:
            pixmap = QPixmap(fname[0])
            # 先转化为Qimag然后转化为Image
            image = ImageQt.fromqpixmap(pixmap)
            # print(type(image))
            string=LSB.decodeImage(image)
            self.imglabel.setPixmap(pixmap)
            self.textEdit1.setText(string)
            QMessageBox.about(self, '成功', '文档已解密')
if __name__ == '__main__':
    app=QApplication(sys.argv)
    ex=Example()
    sys.exit(app.exec_())