# -*- coding:utf-8 -*-
# cython: language_level=3
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication,QMainWindow,QFileDialog,QMessageBox,QRadioButton,QListView,QAbstractItemView,QAction
from image_merge_ui import Ui_Form
from PyQt5.QtGui import QIntValidator, QDoubleValidator, QRegExpValidator
from PyQt5.QtCore import QRegExp,QStringListModel,QModelIndex
import sys,os,re,platform
import PIL
from PIL import Image


class MainWindow(QtWidgets.QMainWindow,Ui_Form):
    #初始化
    def __init__(self,parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.image_names=[]
        self.image_size_ready=0
        self.merge_radio_ready=0
        self.image_save_path_ready=0
        self.image_items_ready=0
        self.merge_column=0
        self.merge_row=0
        self.image_path=[]
        self.filetype=''
        self.addImageButton.clicked.connect(self.chooseImagePath)
        self.listWidget.currentItemChanged.connect(self.checkImage)
        self.listWidget.doubleClicked.connect(self.previewImage)
        self.removeImageButton.clicked.connect(self.removeImage)
        self.image_save_choose.clicked.connect(self.chooseSaveFile)
        pIntValidator = QIntValidator(self)
        self.image_column_size_Edit.setValidator(pIntValidator)
        self.image_row_size_Edit.setValidator(pIntValidator)
        self.image_column_size_Edit.textChanged.connect(self.handleTextChanged)
        self.image_row_size_Edit.textChanged.connect(self.handleTextChanged)
        self.merge_column_radio.clicked.connect(self.handleRadioChanged)
        self.merge_row_radio.clicked.connect(self.handleRadioChanged)
        self.startButton.clicked.connect(self.mergeImage)
        self.resetButton.clicked.connect(self.reset)
        self.upButton.clicked.connect(self.sortItemUp)
        self.downButton.clicked.connect(self.sortItemDown)
        self.auto_size.clicked.connect(self.autoSize)
    #用户选择原图片路径
    def chooseImagePath(self):
        self.image_path, filetype=QFileDialog.getOpenFileNames(self,
                  "选取文件",
                  "./","JPEG (*.jpg;*.jpeg;*.jpe;*.jfif);;PNG (*.png)")                #起始路径
  
        self.image_names.extend(self.image_path)
        for item in self.image_path:
             if len(item.strip())==0:
                 return False
             self.listWidget.addItem(item)
             if len(self.image_names)>=2:
                 self.image_items_ready=1
             else:
                 self.image_items_ready=0
             self.checkInput()
                 #self.startbutton.setenabled(true)
        print(self.image_names)
    def checkImage(self,index):
         r=self.listWidget.currentRow()
         self.f=r
         #print(self.f)
    def removeImage(self,QAction):
        try:
            self.listWidget.removeItemWidget(self.listWidget.takeItem(self.f))
            del self.image_names[self.f]
            if len(self.image_names)<2:
#                self.startButton.setEnabled(False)
                 self.image_items_ready=0
                 self.checkInput()
        except AttributeError as e:
            return False
        except IndexError as f:
            return False

    #用户选择最终图片保存路径以及文件名
    def chooseSaveFile(self):
        self.save_file_url, self.filetype=QFileDialog.getSaveFileName(self,
                  "文件保存",
                  "./",
                  "JPEG (*.jpg;*.jpeg;*.jpe;*.jfif);;PNG (*.png)")
        #print(re.search("\.\w+$",self.save_file_url))
        if re.search("\.\w+$",self.save_file_url)==None:
            if self.filetype=='JPEG (*.jpg;*.jpeg;*.jpe;*.jfif)':
                self.save_file_url=self.save_file_url+'.jpg'
            if self.filetype=='PNG (*.png)':
                self.save_file_url=self.save_file_url+'.png'
        self.image_save_path_Edit.setText(self.save_file_url)
        if len(self.save_file_url.strip())>0:
            self.image_save_path_ready=1
        else:
            self.image_save_path_ready=0
        self.checkInput()
    def reset(self):
        self.image_names=[]
        self.image_size_ready=0
        self.merge_radio_ready=0
        self.image_save_path_ready=0
        self.image_items_ready=0
        #self.merge_column=0
        #self.merge_row=0
        self.listWidget.clear()
        self.image_save_path_Edit.clear()
        self.merge_column_radio.setChecked(False)
        self.merge_row_radio.setChecked(False)
        self.image_column_size_Edit.clear()
        self.image_row_size_Edit.clear()
        self.startButton.setEnabled(False)
        self.auto_size.setChecked(False)
    def handleTextChanged(self):
        if len(self.image_column_size_Edit.displayText().strip())>0 and len(self.image_row_size_Edit.displayText().strip())>0:
            self.image_size_ready=1
            self.image_column_size=int(self.image_column_size_Edit.displayText().strip())
            self.image_row_size=int(self.image_row_size_Edit.displayText().strip())
        else:
            self.image_size_ready=0
        self.checkInput()
    def handleRadioChanged(self):
        if self.merge_column_radio.isChecked():
            #self.merge_column_radio_ready=1
            self.merge_column=1
            #self.checkInput()
        else:
            self.merge_column=0
        if self.merge_row_radio.isChecked():
            #self.merge_row_radio_ready=1
            self.merge_row=1
            #self.checkInput()
        else:
            self.merge_row=0
        if self.merge_column_radio.isChecked() or self.merge_row_radio.isChecked():
            self.merge_radio_ready=1
        self.checkInput()
    def sortItemUp(self):
        try:
            currect_item=self.image_names[self.f]
#            print(self.listWidget.takeItem(self.f))
           
            new_item=self.f-1
 
            self.image_names[self.f]=self.image_names[new_item]
            self.image_names[new_item]=currect_item
            self.listWidget.clear()
            for item in self.image_names:
                self.listWidget.addItem(item)
            self.listWidget.setCurrentRow(new_item)
#            self.listWidget.setCurrentItem(self.listWidget.findItems(self.image_names[new_item],QtCore.Qt.MatchContains))
        except IndexError as e:
                 return False

    def sortItemDown(self):
        try:
            currect_item=self.image_names[self.f]
#            print(self.listWidget.takeItem(self.f))
            new_item=self.f+1
            self.image_names[self.f]=self.image_names[new_item]
            self.image_names[new_item]=currect_item
            self.listWidget.clear()
            for item in self.image_names:
                self.listWidget.addItem(item)
            self.listWidget.setCurrentRow(new_item)
#            self.listWidget.setCurrentItem(self.listWidget.findItems(self.image_names[new_item],QtCore.Qt.MatchContains))
        except IndexError as e:
                return False
    #预览文件
    def previewImage(self):
        #os.system(self.listWidget.currentItem().text())
        QtGui.QDesktopServices.openUrl(QtCore.QUrl("file:///"+self.listWidget.currentItem().text()))

    #检查用户输入
    def checkInput(self):
            if self.image_size_ready==1\
            and self.image_items_ready==1 and self.merge_radio_ready==1\
            and self.image_save_path_ready==1:
                self.startButton.setEnabled(True)
            else:
                self.startButton.setEnabled(False)
    def autoSize(self):
        if self.auto_size.isChecked():
            self.image_column_size_Edit.setEnabled(False)
            self.image_row_size_Edit.setEnabled(False)
            self.image_size_ready=1
            self.checkInput()

        else:
            self.image_column_size_Edit.setEnabled(True)
            self.image_row_size_Edit.setEnabled(True)
            self.image_size_ready=0
            self.checkInput()


    #拼接开始
    def mergeImage(self):
        # print(self.image_names)
        # exit()
        if self.auto_size.isChecked:
            image=self.image_names[0]
            im = Image.open(image)
            self.image_column_size=int(im.size[0])
            # print(self.image_column_size)
            self.image_row_size=int(im.size[1])
            # print(self.image_row_size)
            # exit()
        if self.merge_column==1:
            image_column=len(self.image_names)
            image_row=1
        if self.merge_row==1:
            image_column=1
            image_row=len(self.image_names) 
        to_image = Image.new('RGB', (image_column * self.image_column_size, image_row * self.image_row_size)) #创建一个新图
        if self.filetype=='JPEG (*.jpg;*.jpeg;*.jpe;*.jfif)' and to_image.size[0]>65535 or to_image.size[1]>65535:
            QMessageBox.warning(self,'图片尺寸错误','JPG类型图片长宽不得大于65535px')
            return False
            # 循环遍历，把每张图片按顺序粘贴到对应位置上
        for y in range(1, image_row + 1):
            for x in range(1, image_column + 1):

                 from_image = Image.open(self.image_names[image_column * (y - 1) + x - 1]).resize(
                    (self.image_column_size, self.image_row_size),Image.ANTIALIAS)
                 to_image.paste(from_image, ((x - 1) * self.image_column_size, (y - 1) * self.image_row_size))
        try:
            to_image.save(self.save_file_url) # 保存新图
        except IOError:
            #PIL.ImageFile.MAXBLOCK = image_column * self.image_column_size * image_row * self.image_row_size
            QMessageBox.error(self,'错误','请联系开发人员寻求支持！')
            return False
        QMessageBox.information(self,'提示','完成！')