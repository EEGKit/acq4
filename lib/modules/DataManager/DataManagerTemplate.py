# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './lib/modules/DataManager/DataManagerTemplate.ui'
#
# Created: Tue Jan 31 12:11:36 2012
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1000, 756)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setMargin(0)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.baseDirText = QtGui.QLineEdit(self.centralwidget)
        self.baseDirText.setObjectName(_fromUtf8("baseDirText"))
        self.gridLayout.addWidget(self.baseDirText, 0, 1, 1, 1)
        self.selectDirBtn = QtGui.QPushButton(self.centralwidget)
        self.selectDirBtn.setObjectName(_fromUtf8("selectDirBtn"))
        self.gridLayout.addWidget(self.selectDirBtn, 0, 2, 1, 1)
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.currentDirText = QtGui.QLineEdit(self.centralwidget)
        self.currentDirText.setObjectName(_fromUtf8("currentDirText"))
        self.gridLayout.addWidget(self.currentDirText, 1, 1, 1, 1)
        self.setCurrentDirBtn = QtGui.QPushButton(self.centralwidget)
        self.setCurrentDirBtn.setObjectName(_fromUtf8("setCurrentDirBtn"))
        self.gridLayout.addWidget(self.setCurrentDirBtn, 1, 2, 1, 1)
        self.logDirText = QtGui.QLineEdit(self.centralwidget)
        self.logDirText.setObjectName(_fromUtf8("logDirText"))
        self.gridLayout.addWidget(self.logDirText, 2, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.setLogDirBtn = QtGui.QPushButton(self.centralwidget)
        self.setLogDirBtn.setObjectName(_fromUtf8("setLogDirBtn"))
        self.gridLayout.addWidget(self.setLogDirBtn, 2, 2, 1, 1)
        self.verticalLayout_5.addLayout(self.gridLayout)
        self.splitter = QtGui.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.layoutWidget = QtGui.QWidget(self.splitter)
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setSpacing(3)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.newFolderList = QtGui.QComboBox(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.newFolderList.sizePolicy().hasHeightForWidth())
        self.newFolderList.setSizePolicy(sizePolicy)
        self.newFolderList.setObjectName(_fromUtf8("newFolderList"))
        self.verticalLayout_2.addWidget(self.newFolderList)
        self.fileTreeWidget = DirTreeWidget(self.layoutWidget)
        self.fileTreeWidget.setEditTriggers(QtGui.QAbstractItemView.EditKeyPressed|QtGui.QAbstractItemView.SelectedClicked)
        self.fileTreeWidget.setDragEnabled(True)
        self.fileTreeWidget.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
        self.fileTreeWidget.setObjectName(_fromUtf8("fileTreeWidget"))
        self.fileTreeWidget.headerItem().setText(0, _fromUtf8("1"))
        self.fileTreeWidget.header().setVisible(False)
        self.verticalLayout_2.addWidget(self.fileTreeWidget)
        self.layoutWidget1 = QtGui.QWidget(self.splitter)
        self.layoutWidget1.setObjectName(_fromUtf8("layoutWidget1"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setMargin(0)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.fileNameLabel = QtGui.QLabel(self.layoutWidget1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(5)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fileNameLabel.sizePolicy().hasHeightForWidth())
        self.fileNameLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(7)
        font.setWeight(75)
        font.setBold(True)
        self.fileNameLabel.setFont(font)
        self.fileNameLabel.setText(_fromUtf8(""))
        self.fileNameLabel.setObjectName(_fromUtf8("fileNameLabel"))
        self.verticalLayout_4.addWidget(self.fileNameLabel)
        self.fileDisplayTabs = QtGui.QTabWidget(self.layoutWidget1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(5)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fileDisplayTabs.sizePolicy().hasHeightForWidth())
        self.fileDisplayTabs.setSizePolicy(sizePolicy)
        self.fileDisplayTabs.setObjectName(_fromUtf8("fileDisplayTabs"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.tab)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.fileInfo = FileInfoView(self.tab)
        self.fileInfo.setObjectName(_fromUtf8("fileInfo"))
        self.verticalLayout_3.addWidget(self.fileInfo)
        self.fileDisplayTabs.addTab(self.tab, _fromUtf8(""))
        self.logTab = QtGui.QWidget()
        self.logTab.setObjectName(_fromUtf8("logTab"))
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.logTab)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setMargin(0)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.fileDisplayTabs.addTab(self.logTab, _fromUtf8(""))
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName(_fromUtf8("tab_3"))
        self.verticalLayout_7 = QtGui.QVBoxLayout(self.tab_3)
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.dataViewWidget = FileDataView(self.tab_3)
        self.dataViewWidget.setObjectName(_fromUtf8("dataViewWidget"))
        self.verticalLayout_7.addWidget(self.dataViewWidget)
        self.fileDisplayTabs.addTab(self.tab_3, _fromUtf8(""))
        self.analysisTab = QtGui.QWidget()
        self.analysisTab.setObjectName(_fromUtf8("analysisTab"))
        self.gridLayout_2 = QtGui.QGridLayout(self.analysisTab)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.fileDisplayTabs.addTab(self.analysisTab, _fromUtf8(""))
        self.verticalLayout_4.addWidget(self.fileDisplayTabs)
        self.verticalLayout_5.addWidget(self.splitter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.logDock = QtGui.QDockWidget(MainWindow)
        self.logDock.setFloating(False)
        self.logDock.setFeatures(QtGui.QDockWidget.AllDockWidgetFeatures)
        self.logDock.setObjectName(_fromUtf8("logDock"))
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.verticalLayout = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.logView = QtGui.QTextEdit(self.dockWidgetContents)
        self.logView.setReadOnly(True)
        self.logView.setObjectName(_fromUtf8("logView"))
        self.verticalLayout.addWidget(self.logView)
        self.logEntryText = QtGui.QLineEdit(self.dockWidgetContents)
        self.logEntryText.setObjectName(_fromUtf8("logEntryText"))
        self.verticalLayout.addWidget(self.logEntryText)
        self.logDock.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.logDock)

        self.retranslateUi(MainWindow)
        self.fileDisplayTabs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Data Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Top-level Directory:", None, QtGui.QApplication.UnicodeUTF8))
        self.selectDirBtn.setText(QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Storage Directory:", None, QtGui.QApplication.UnicodeUTF8))
        self.setCurrentDirBtn.setText(QtGui.QApplication.translate("MainWindow", "Set", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Log Directory:", None, QtGui.QApplication.UnicodeUTF8))
        self.setLogDirBtn.setText(QtGui.QApplication.translate("MainWindow", "Set", None, QtGui.QApplication.UnicodeUTF8))
        self.fileDisplayTabs.setTabText(self.fileDisplayTabs.indexOf(self.tab), QtGui.QApplication.translate("MainWindow", "Info", None, QtGui.QApplication.UnicodeUTF8))
        self.fileDisplayTabs.setTabText(self.fileDisplayTabs.indexOf(self.logTab), QtGui.QApplication.translate("MainWindow", "Log", None, QtGui.QApplication.UnicodeUTF8))
        self.fileDisplayTabs.setTabText(self.fileDisplayTabs.indexOf(self.tab_3), QtGui.QApplication.translate("MainWindow", "Data", None, QtGui.QApplication.UnicodeUTF8))
        self.fileDisplayTabs.setTabText(self.fileDisplayTabs.indexOf(self.analysisTab), QtGui.QApplication.translate("MainWindow", "Analysis", None, QtGui.QApplication.UnicodeUTF8))
        self.logDock.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Current Log", None, QtGui.QApplication.UnicodeUTF8))

from FileInfoView import FileInfoView
from DirTreeWidget import DirTreeWidget
from FileDataView import FileDataView
