#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# ver 0.0.2 updated to support maya 2014 , and speed up by using qlabel
# ver 0.0.3 center dispaly icons and not scale them up
# ver 0.0.4 fix large icons not scaled down bug, now < 32 pixel icons will be kept to original size,  > 32 pixel width large .png images will be scaled to 32*32
# ver 0.0.5 use api v2, new style signal/slot, cleanup code


__author__ = "Jiang Han"
__copyright__ = "有版权么"
__credits__ = ["Nathan Horne"]
__license__ = "抄袭"
__version__ = "0.0.5"
__maintainer__ = "Jiang Han"
__email__ = "oglops@gmail.com"
__status__ = "totally fucked up"

from PyQt4 import uic

import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)

from PyQt4.QtGui import *  
from PyQt4.QtCore import *  

import maya.OpenMayaUI as apiUI
import maya.cmds as cmds

import sys,os
import platform

# The following code is copied from  qrc_resources.py
qt_resource_data = "\
\x00\x00\x01\x76\
\x89\
\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d\x49\x48\x44\x52\x00\
\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xff\x61\
\x00\x00\x01\x3d\x49\x44\x41\x54\x38\x8d\xad\xd2\x31\x4b\x1d\x51\
\x10\x86\xe1\xe7\x5a\x2c\x16\x92\x22\x48\xb8\x5c\x0c\x9c\x52\x82\
\xd8\x09\x81\x80\x2c\x89\x21\x7f\xc0\x2a\xd8\xd9\xd8\xa4\x10\x0b\
\x7f\x83\x95\x58\x48\x52\x06\xac\xac\xac\x0d\xb7\x38\x45\x8a\x40\
\x0a\x2d\x2c\x52\xa4\x58\x50\x82\x88\x88\x58\x85\x83\x04\x8b\xdd\
\x8b\x87\xeb\x6e\x10\x92\x69\x06\xe6\xcc\xbc\x7c\x33\xdf\xe1\x1f\
\xa3\x37\x5e\xa8\xca\x62\x0a\xaf\x31\x83\x73\x0c\x43\x4c\x37\x8f\
\x02\x54\x65\xb1\x82\x1d\x3c\xcd\xca\x37\xd8\x0c\x31\x7d\x6a\x03\
\x4c\x64\xc3\xef\xb1\x87\xdf\x58\xc7\x5b\x7c\xc0\x15\x3e\x56\x65\
\xb1\xd6\xa9\xa0\x2a\x8b\x49\x9c\xe2\x16\x0b\x21\xa6\xb3\x0c\x3c\
\x8d\xef\x98\xc6\xf3\x10\xd3\x75\x9b\x82\xc5\xa6\x61\x27\x1f\x86\
\x10\xd3\x25\xb6\x30\x85\xa5\xae\x15\xfa\x4d\xfe\xd1\x26\x33\xab\
\x0f\xba\x00\xbf\x9a\xfc\xa2\x03\x30\xd7\xe4\xb3\xf1\x87\x11\xe0\
\xab\xda\xb2\xf5\xaa\x2c\x42\xde\x50\x95\x45\x1f\x9b\x6a\x37\x86\
\xe3\x80\x5e\xd6\xb8\x8c\x7d\x5c\x62\x1b\x27\x98\x55\x3b\x32\xc0\
\x2a\x3e\x87\x98\xfe\xb4\x02\x32\xc8\x2e\x9e\x65\xe5\x2b\x6c\xe0\
\x0b\x0e\xb0\x1a\x62\x3a\x69\x05\x34\x90\x49\xb5\x2b\xa3\x9f\x18\
\x91\x70\xa4\xbe\xc5\x05\xde\x8c\x20\x0f\x00\x5d\x51\x95\xc5\x4b\
\x1c\xe2\x49\x03\x79\x15\x62\xfa\x39\xf1\xf7\xb1\xfb\x08\x31\x7d\
\xc3\x3b\xf5\x31\x8f\xb5\x38\xf2\x58\x25\xf3\xcd\x9a\xff\x27\xee\
\x00\xac\x17\x58\x7e\xdc\x36\xc0\xce\x00\x00\x00\x00\x49\x45\x4e\
\x44\xae\x42\x60\x82\
"

qt_resource_name = "\
\x00\x0d\
\x09\x39\xc9\x07\
\x00\x6d\
\x00\x61\x00\x67\x00\x6e\x00\x69\x00\x66\x00\x69\x00\x65\x00\x72\x00\x2e\x00\x70\x00\x6e\x00\x67\
"

qt_resource_struct = "\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\
"

def qInitResources():
    qRegisterResourceData(0x01, qt_resource_struct, qt_resource_name, qt_resource_data)

def qCleanupResources():
    qUnregisterResourceData(0x01, qt_resource_struct, qt_resource_name, qt_resource_data)

qInitResources()

##############################################################



# copied from nathan's website
def getMayaWindow():
    """
    Get the main Maya window as a QtGui.QMainWindow instance
    @return: QtGui.QMainWindow instance of the top level Maya windows
    """
    ptr = apiUI.MQtUtil.mainWindow()
    if ptr is not None:
        return sip.wrapinstance(long(ptr), QObject)

def toQtObject(mayaName):
    """
    Convert a Maya ui path to a Qt object
    @param mayaName: Maya UI Path to convert (Ex: "scriptEditorPanel1Window|TearOffPane|scriptEditorPanel1|testButton" )
    @return: PyQt representation of that object
    """
    ptr = apiUI.MQtUtil.findControl(mayaName)
    if ptr is None:
        ptr = apiUI.MQtUtil.findLayout(mayaName)
    if ptr is None:
        ptr = apiUI.MQtUtil.findMenuItem(mayaName)
    if ptr is not None:
        return sip.wrapinstance(long(ptr), QObject)


####################################################################

class IconDelegate(QStyledItemDelegate):

    def __init__(self,iconDir, icons,parent=None):
        super(IconDelegate, self).__init__(parent)
        self.icons = icons
        self.iconDir = iconDir
                
    def paint(self, painter, option, index):
        
        if option.state & QStyle.State_Selected:
            painter.fillRect(option.rect, option.palette.highlight())
        
        painter.save()
        if self.iconDir=='Internal Icons':
            png = ':/%s' % self.icons[index.row()]
        else:
            png = os.path.join(str(self.iconDir), self.icons[index.row()])

        pixmap = QPixmap(png)

        # option.rect.setSize(pixmap.size())
        
        if pixmap.width()>32:
            pixmap = pixmap.scaled(32,32,Qt.KeepAspectRatio,Qt.SmoothTransformation)
   

        rect = option.rect
        offsetX= (rect.width() -pixmap.width() )/2 
        offsetY =  (rect.height() -pixmap.height() )/2 
        
        painter.drawPixmap(rect.x()+offsetX,rect.y()+offsetY,pixmap)
        
        painter.restore()

class IconModel(QAbstractListModel):
    def __init__(self, iconDir,icons):
        super(IconModel, self).__init__()
        self.icons = icons
        self.iconDir = iconDir
    
    def rowCount(self, index=QModelIndex()):
        return len(self.icons)
    
    def data(self, index, role=Qt.DisplayRole):
        if index.isValid() and role == Qt.DisplayRole:
            pass
        elif role == Qt.ToolTipRole:
            return self.icons[index.row()]
        
        elif role == Qt.DecorationRole:
            if self.iconDir=='Internal Icons':
                cc = ':/%s' % self.icons[index.row()]
            else:
                cc = os.path.join(str(self.iconDir), self.icons[index.row()])

            label = QLabel()
            pixmap=QPixmap (cc)

            # pixmap = pixmap.scaled(32,32,Qt.KeepAspectRatio,Qt.SmoothTransformation)
            
            label.setPixmap(pixmap)
            # return pixmap
            return label

        else: 
            return None


#If you put the .ui file for this example elsewhere, just change this path.
UI_DIRPATH = os.path.dirname(os.path.normpath(__file__))
UI_FULLPATH = os.path.join(UI_DIRPATH, 'iconChooser.ui')
form_class, base_class = uic.loadUiType(UI_FULLPATH)

class Window(form_class, base_class):
    
    StyleSheet = '''
    QLineEdit#lineEdit {
        background-image: url(:magnifier.png);
        background-repeat: no-repeat;
        background-position: left;
        background-clip: padding;
        padding-left: 16px;
        
        border-style: outset;
        border-width: 2px; 
        border-color: gray;
        border-radius: 10px;
        padding 2px;
        }
    '''

    def __init__(self, parent=getMayaWindow()):
        super(Window, self).__init__(parent)
        self.setupUi(self)
        self.setStyleSheet(Window.StyleSheet)
        
        self.setWindowTitle('icon chooser %s by %s' % (__version__,u'大叔'))
        
        delimiter = ':'
        if platform.system() == 'Windows':
            delimiter = ';'
        self.iconPath = os.environ['XBMLANGPATH'].split(delimiter)
        
        if platform.system() == 'Linux':
            self.iconPath = [os.path.dirname(p) for p in self.iconPath if p.endswith('%B')]

        pathWithIcons=[]
        for p in self.iconPath:
            print p
            if os.path.isdir(p):
                files = os.listdir(p)
                if files:
                    pathWithIcons.append(p)

        self.allIcons = cmds.resourceManager(nameFilter="*.png")

        pathWithIcons.insert(0,'Internal Icons')
        self.comboBox.addItems(pathWithIcons)
        
        self.initialize()
        
        self.listView.clicked.connect(self.selectIcon)
        self.comboBox.currentIndexChanged.connect(self.initialize)

    def buildCompleter(self):
        self.completer = QCompleter()
        self.lineEdit.setCompleter(self.completer)
        self.searchModel = QStringListModel()
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        
        allIcons = [i.split('.')[0] for i in self.curAllIcons]
        self.searchModel.setStringList(self.curAllIcons)
        self.completer.setModel(self.searchModel)
        
    @pyqtSlot(QModelIndex)
    def selectIcon(self,index):
        name = index.model().data(index,Qt.ToolTipRole)
        self.label.setText(name)


    @pyqtSlot(str)
    def on_lineEdit_textChanged(self):
        text= self.lineEdit.text()
        search = QRegExp(    text,
                                    Qt.CaseInsensitive,
                                    QRegExp.RegExp
                                    )
        self.proxyModel.setFilterRegExp(search)
#        print 'search result:',self.proxyModel.rowCount()

    @pyqtSlot(str)
    def initialize(self):
        # see what is current path, then get allicons
        self.curIconPath = self.comboBox.currentText()

        if self.comboBox.currentIndex()==0:
            self.curAllIcons = self.allIcons
        else:
            self.curAllIcons = os.listdir(self.curIconPath)
        
        self.curAllIcons = self.excludeIcons(self.curAllIcons)

        self.listView.setUniformItemSizes(True)
        
        self.model = IconModel(self.curIconPath,self.curAllIcons)
        self.proxyModel = QSortFilterProxyModel ()
        self.proxyModel.setSourceModel(self.model)
        self.proxyModel.setFilterRole(Qt.ToolTipRole)
        
        self.listView.setModel(self.proxyModel)
        self.listView.setViewMode(QListView.IconMode)
        
        self.delegate = IconDelegate(self.curIconPath,self.curAllIcons)
        self.listView.setItemDelegate(self.delegate)
        
        self.lineEdit.editingFinished.connect(self.on_lineEdit_textChanged)
        
        self.buildCompleter()
        
    def excludeIcons(self,icons):
        excludeList=('tdi','iff')
        goodIcons=[]
        for i in icons:
            if '.' not in i or i.split('.')[-1] in excludeList:
                continue
            else:
                goodIcons.append(i)
        return goodIcons

def main():
    global gui
    try:
        gui.close()
        gui.destroy()
        del gui
    except:
        pass
    
    gui = Window()
    gui.show()

  