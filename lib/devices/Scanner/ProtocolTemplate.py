# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ProtocolTemplate.ui'
#
# Created: Fri Jul 01 11:53:48 2011
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(898, 481)
        self.gridLayout_2 = QtGui.QGridLayout(Form)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label = QtGui.QLabel(Form)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_3.addWidget(self.label)
        self.cameraCombo = QtGui.QComboBox(Form)
        self.cameraCombo.setObjectName(_fromUtf8("cameraCombo"))
        self.horizontalLayout_3.addWidget(self.cameraCombo)
        self.gridLayout_2.addLayout(self.horizontalLayout_3, 0, 0, 1, 2)
        self.label_5 = QtGui.QLabel(Form)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_2.addWidget(self.label_5, 0, 2, 1, 1)
        self.label_8 = QtGui.QLabel(Form)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout_2.addWidget(self.label_8, 0, 3, 1, 1)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_4.addWidget(self.label_2)
        self.laserCombo = QtGui.QComboBox(Form)
        self.laserCombo.setObjectName(_fromUtf8("laserCombo"))
        self.horizontalLayout_4.addWidget(self.laserCombo)
        self.gridLayout_2.addLayout(self.horizontalLayout_4, 1, 0, 1, 2)
        self.itemList = QtGui.QListWidget(Form)
        self.itemList.setObjectName(_fromUtf8("itemList"))
        self.gridLayout_2.addWidget(self.itemList, 1, 2, 7, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.addLineScanBtn = QtGui.QPushButton(Form)
        self.addLineScanBtn.setEnabled(False)
        self.addLineScanBtn.setObjectName(_fromUtf8("addLineScanBtn"))
        self.verticalLayout.addWidget(self.addLineScanBtn)
        self.addCircleScanBtn = QtGui.QPushButton(Form)
        self.addCircleScanBtn.setEnabled(False)
        self.addCircleScanBtn.setObjectName(_fromUtf8("addCircleScanBtn"))
        self.verticalLayout.addWidget(self.addCircleScanBtn)
        self.addSpiralScanBtn = QtGui.QPushButton(Form)
        self.addSpiralScanBtn.setEnabled(False)
        self.addSpiralScanBtn.setObjectName(_fromUtf8("addSpiralScanBtn"))
        self.verticalLayout.addWidget(self.addSpiralScanBtn)
        self.deleteStepBtn = QtGui.QPushButton(Form)
        self.deleteStepBtn.setEnabled(False)
        self.deleteStepBtn.setObjectName(_fromUtf8("deleteStepBtn"))
        self.verticalLayout.addWidget(self.deleteStepBtn)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.previewBtn = QtGui.QPushButton(Form)
        self.previewBtn.setEnabled(False)
        self.previewBtn.setObjectName(_fromUtf8("previewBtn"))
        self.verticalLayout.addWidget(self.previewBtn)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.programTable = QtGui.QTableWidget(Form)
        self.programTable.setObjectName(_fromUtf8("programTable"))
        self.programTable.setColumnCount(0)
        self.programTable.setRowCount(0)
        self.horizontalLayout.addWidget(self.programTable)
        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 3, 7, 1)
        spacerItem1 = QtGui.QSpacerItem(63, 25, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 1, 4, 1, 1)
        self.simulateShutterCheck = QtGui.QCheckBox(Form)
        self.simulateShutterCheck.setObjectName(_fromUtf8("simulateShutterCheck"))
        self.gridLayout_2.addWidget(self.simulateShutterCheck, 2, 0, 1, 2)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.minTimeSpin = SpinBox(Form)
        self.minTimeSpin.setSuffix(_fromUtf8(""))
        self.minTimeSpin.setDecimals(2)
        self.minTimeSpin.setMaximum(1000000.0)
        self.minTimeSpin.setObjectName(_fromUtf8("minTimeSpin"))
        self.gridLayout.addWidget(self.minTimeSpin, 0, 0, 1, 1)
        self.minDistSpin = SpinBox(Form)
        self.minDistSpin.setSuffix(_fromUtf8(""))
        self.minDistSpin.setMaximum(1000000.0)
        self.minDistSpin.setObjectName(_fromUtf8("minDistSpin"))
        self.gridLayout.addWidget(self.minDistSpin, 1, 0, 1, 1)
        self.label_4 = QtGui.QLabel(Form)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 1, 1, 1, 1)
        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 0, 1, 1, 1)
        self.packingSpin = SpinBox(Form)
        self.packingSpin.setMinimum(0.1)
        self.packingSpin.setMaximum(1000.0)
        self.packingSpin.setSingleStep(0.1)
        self.packingSpin.setProperty(_fromUtf8("value"), 1.0)
        self.packingSpin.setObjectName(_fromUtf8("packingSpin"))
        self.gridLayout.addWidget(self.packingSpin, 2, 0, 1, 1)
        self.label_7 = QtGui.QLabel(Form)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout.addWidget(self.label_7, 2, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 3, 0, 1, 2)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.spotSizeLabel = QtGui.QLabel(Form)
        self.spotSizeLabel.setObjectName(_fromUtf8("spotSizeLabel"))
        self.verticalLayout_2.addWidget(self.spotSizeLabel)
        self.sizeFromCalibrationRadio = QtGui.QRadioButton(Form)
        self.sizeFromCalibrationRadio.setChecked(True)
        self.sizeFromCalibrationRadio.setObjectName(_fromUtf8("sizeFromCalibrationRadio"))
        self.verticalLayout_2.addWidget(self.sizeFromCalibrationRadio)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.sizeCustomRadio = QtGui.QRadioButton(Form)
        self.sizeCustomRadio.setObjectName(_fromUtf8("sizeCustomRadio"))
        self.horizontalLayout_2.addWidget(self.sizeCustomRadio)
        self.sizeSpin = SpinBox(Form)
        self.sizeSpin.setSuffix(_fromUtf8(""))
        self.sizeSpin.setMinimum(0.0)
        self.sizeSpin.setMaximum(100000.0)
        self.sizeSpin.setSingleStep(1e-06)
        self.sizeSpin.setProperty(_fromUtf8("value"), 0.0)
        self.sizeSpin.setObjectName(_fromUtf8("sizeSpin"))
        self.horizontalLayout_2.addWidget(self.sizeSpin)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.gridLayout_2.addLayout(self.verticalLayout_2, 4, 0, 1, 2)
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.addPointBtn = QtGui.QPushButton(Form)
        self.addPointBtn.setObjectName(_fromUtf8("addPointBtn"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.addPointBtn)
        self.addOcclusionBtn = QtGui.QPushButton(Form)
        self.addOcclusionBtn.setObjectName(_fromUtf8("addOcclusionBtn"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.addOcclusionBtn)
        self.addGridBtn = QtGui.QPushButton(Form)
        self.addGridBtn.setObjectName(_fromUtf8("addGridBtn"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.addGridBtn)
        self.addProgramBtn = QtGui.QPushButton(Form)
        self.addProgramBtn.setObjectName(_fromUtf8("addProgramBtn"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.addProgramBtn)
        self.deleteBtn = QtGui.QPushButton(Form)
        self.deleteBtn.setObjectName(_fromUtf8("deleteBtn"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.deleteBtn)
        self.deleteAllBtn = QtGui.QPushButton(Form)
        self.deleteAllBtn.setObjectName(_fromUtf8("deleteAllBtn"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.deleteAllBtn)
        self.gridLayout_2.addLayout(self.formLayout, 5, 0, 1, 2)
        spacerItem2 = QtGui.QSpacerItem(83, 59, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem2, 6, 0, 1, 1)
        self.recomputeBtn = QtGui.QPushButton(Form)
        self.recomputeBtn.setObjectName(_fromUtf8("recomputeBtn"))
        self.gridLayout_2.addWidget(self.recomputeBtn, 7, 0, 1, 1)
        self.checkBox = QtGui.QCheckBox(Form)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.gridLayout_2.addWidget(self.checkBox, 7, 1, 1, 1)
        self.timeLabel = QtGui.QLabel(Form)
        self.timeLabel.setObjectName(_fromUtf8("timeLabel"))
        self.gridLayout_2.addWidget(self.timeLabel, 8, 0, 1, 1)
        self.hideCheck = QtGui.QCheckBox(Form)
        self.hideCheck.setEnabled(True)
        self.hideCheck.setChecked(False)
        self.hideCheck.setObjectName(_fromUtf8("hideCheck"))
        self.gridLayout_2.addWidget(self.hideCheck, 8, 2, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "Camera Module:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Form", "Items", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("Form", "Program Controls:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Form", "Laser Device:", None, QtGui.QApplication.UnicodeUTF8))
        self.addLineScanBtn.setText(QtGui.QApplication.translate("Form", "Add Line Scan", None, QtGui.QApplication.UnicodeUTF8))
        self.addCircleScanBtn.setText(QtGui.QApplication.translate("Form", "Add Circle Scan", None, QtGui.QApplication.UnicodeUTF8))
        self.addSpiralScanBtn.setText(QtGui.QApplication.translate("Form", "Add Spiral Scan", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteStepBtn.setText(QtGui.QApplication.translate("Form", "Delete Step", None, QtGui.QApplication.UnicodeUTF8))
        self.previewBtn.setText(QtGui.QApplication.translate("Form", "Preview", None, QtGui.QApplication.UnicodeUTF8))
        self.programTable.setSortingEnabled(True)
        self.simulateShutterCheck.setText(QtGui.QApplication.translate("Form", "Simulate Shutter", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Form", "Minimum distance", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Form", "Minimum time", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("Form", "Grid Spacing", None, QtGui.QApplication.UnicodeUTF8))
        self.spotSizeLabel.setText(QtGui.QApplication.translate("Form", "Spot Display Size:", None, QtGui.QApplication.UnicodeUTF8))
        self.sizeFromCalibrationRadio.setText(QtGui.QApplication.translate("Form", "Use size from calibration", None, QtGui.QApplication.UnicodeUTF8))
        self.sizeCustomRadio.setText(QtGui.QApplication.translate("Form", "Use custom size:", None, QtGui.QApplication.UnicodeUTF8))
        self.addPointBtn.setText(QtGui.QApplication.translate("Form", "Add Point", None, QtGui.QApplication.UnicodeUTF8))
        self.addOcclusionBtn.setText(QtGui.QApplication.translate("Form", "Add Occlusion", None, QtGui.QApplication.UnicodeUTF8))
        self.addGridBtn.setText(QtGui.QApplication.translate("Form", "Add Grid", None, QtGui.QApplication.UnicodeUTF8))
        self.addProgramBtn.setText(QtGui.QApplication.translate("Form", "Add Program", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteBtn.setText(QtGui.QApplication.translate("Form", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteAllBtn.setText(QtGui.QApplication.translate("Form", "Delete All", None, QtGui.QApplication.UnicodeUTF8))
        self.recomputeBtn.setText(QtGui.QApplication.translate("Form", "Recompute", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox.setText(QtGui.QApplication.translate("Form", "Auto recompute", None, QtGui.QApplication.UnicodeUTF8))
        self.timeLabel.setText(QtGui.QApplication.translate("Form", "Total Time:", None, QtGui.QApplication.UnicodeUTF8))
        self.hideCheck.setText(QtGui.QApplication.translate("Form", "Hide items", None, QtGui.QApplication.UnicodeUTF8))

from SpinBox import SpinBox
