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
        # self.image_column_size_Edit.setValidator(pIntValidator)
        # self.image_row_size_Edit.setValidator(pIntValidator)
        # self.image_column_size_Edit.textChanged.connect(self.handleTextChanged)
        # self.image_row_size_Edit.textChanged.connect(self.handleTextChanged)
        self.merge_column_radio.clicked.connect(self.handleRadioChanged)
        self.merge_row_radio.clicked.connect(self.handleRadioChanged)
        self.startButton.clicked.connect(self.mergeImage)
        self.resetButton.clicked.connect(self.reset)
        self.upButton.clicked.connect(self.sortItemUp)
        self.downButton.clicked.connect(self.sortItemDown)
        # self.auto_size.clicked.connect(self.autoSize)
        self.autoSize()
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
          
    def checkImage(self,index):
         r=self.listWidget.currentRow()
         self.f=r
       
    def removeImage(self,QAction):
        try:
            self.listWidget.removeItemWidget(self.listWidget.takeItem(self.f))
            del self.image_names[self.f]
            if len(self.image_names)<2:
#                
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
        # self.image_size_ready=0
        # self.merge_radio_ready=0
        self.image_save_path_ready=0
        self.image_items_ready=0
        #self.merge_column=0
        #self.merge_row=0
        self.listWidget.clear()
        self.image_save_path_Edit.clear()
        self.merge_column_radio.setChecked(False)
        self.merge_row_radio.setChecked(False)
        # self.image_column_size_Edit.clear()
        # self.image_row_size_Edit.clear()
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
        # if self.auto_size.isChecked():
        # self.auto_size.setChecked(True)
        # self.image_column_size_Edit.setEnabled(False)
        # self.image_row_size_Edit.setEnabled(False)
        self.image_size_ready=1
        self.checkInput()

        # else:
        #     self.image_column_size_Edit.setEnabled(True)
        #     self.image_row_size_Edit.setEnabled(True)
        #     self.image_size_ready=0
        #     self.checkInput()


    #拼接开始
    def mergeImage(self):
        # print(self.image_names)
        # exit()
        if 2>1:
            # image=self.image_names[0]
            self.image_column_size_arr=[]
            self.image_row_size_arr=[]
            for item in self.image_names:
                im = Image.open(item)
                image_column_size=int(im.size[0])
                image_row_size=int(im.size[1])
                self.image_column_size_arr.append(image_column_size)
                self.image_row_size_arr.append(image_row_size)
            self.image_column_size=sum(self.image_column_size_arr)
            # print(self.image_column_size)
            self.image_row_size=sum(self.image_row_size_arr)
            # print(self.image_row_size)
            # exit()
        if self.merge_column==1:
            image_column=len(self.image_names)
            image_row=1
            to_image = Image.new('RGB', (self.image_column_size, max(self.image_row_size_arr))) #创建一个新图
        if self.merge_row==1:
            image_column=1
            image_row=len(self.image_names)
            to_image = Image.new('RGB', (max(self.image_column_size_arr), self.image_row_size)) #创建一个新图
        
        if self.filetype=='JPEG (*.jpg;*.jpeg;*.jpe;*.jfif)' and to_image.size[0]>65535 or to_image.size[1]>65535:
            QMessageBox.warning(self,'图片尺寸错误','JPG类型图片长宽不得大于65535px')
            return False
            # 循环遍历，把每张图片按顺序粘贴到对应位置上，当横向拼接时x轴定位为第一张图片到上一张图片的宽度总和，Y轴定位为0
            # 当纵向拼接时x轴定位为0，y轴定位为第一张图片到上一张图片的高度总和
      
        marge_wide_arr=[]
        marge_high_arr=[]
        
        for y in range(1, image_row + 1):
            for x in range(1, image_column + 1):
                
                from_image = Image.open(self.image_names[image_column * (y - 1) + x - 1])
                previous_image = Image.open(self.image_names[(image_column * (y - 1) + x - 1)-1])#打开上一张图
                if (image_column * (y - 1) + x - 1)-1==-1: #第一次循环得到的索引是-1，需要把粘贴宽高值设为起点0
                    marge_wide=0
                    marge_high=0
                else:
                    marge_wide=previous_image.size[0]#得到上一张图的宽
                    marge_high=previous_image.size[1]#得到上一张图的高
               
                if self.merge_column==1:#当横向拼接时拼接图片的高度定位为0
                    marge_high=0
                if self.merge_row==1:#当纵向拼接时拼接图片的宽度定位为0
                    marge_wide=0
                marge_wide_arr.append(marge_wide)#将每一张小图的宽加入数组
                marge_high_arr.append(marge_high)#将每一张小图的高加入数组
                to_image.paste(from_image, (sum(marge_wide_arr), sum(marge_high_arr)))#拼接定位的宽高即为上面数组的和
      
        try:
            to_image.save(self.save_file_url) # 保存新图
        except IOError:
            QMessageBox.error(self,'错误','请联系开发人员寻求支持！')
            return False
            #PIL.ImageFile.MAXBLOCK = image_column * self.image_column_size * image_row * self.image_row_size
        QMessageBox.information(self,'提示','完成！')