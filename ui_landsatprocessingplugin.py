# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_landsatprocessingplugin.ui'
#
# Created: Fri Feb 15 16:09:01 2013
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_landsatProcessingPlugin(object):
    def setupUi(self, landsatProcessingPlugin):
        landsatProcessingPlugin.setObjectName("landsatProcessingPlugin")
        landsatProcessingPlugin.resize(500, 369)
        self.verticalLayout_2 = QtGui.QVBoxLayout(landsatProcessingPlugin)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox = QtGui.QGroupBox(landsatProcessingPlugin)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.labelChoosenMetadata = QtGui.QLabel(self.groupBox)
        self.labelChoosenMetadata.setObjectName("labelChoosenMetadata")
        self.horizontalLayout.addWidget(self.labelChoosenMetadata)
        self.buttonChooseMetadata = QtGui.QToolButton(self.groupBox)
        self.buttonChooseMetadata.setObjectName("buttonChooseMetadata")
        self.horizontalLayout.addWidget(self.buttonChooseMetadata)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.groupBoxMetadata = QtGui.QGroupBox(landsatProcessingPlugin)
        self.groupBoxMetadata.setObjectName("groupBoxMetadata")
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBoxMetadata)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableWidgetMetadata = QtGui.QTableWidget(self.groupBoxMetadata)
        self.tableWidgetMetadata.setObjectName("tableWidgetMetadata")
        self.tableWidgetMetadata.setColumnCount(2)
        self.tableWidgetMetadata.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidgetMetadata.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidgetMetadata.setHorizontalHeaderItem(1, item)
        self.verticalLayout.addWidget(self.tableWidgetMetadata)
        self.verticalLayout_2.addWidget(self.groupBoxMetadata)

        self.retranslateUi(landsatProcessingPlugin)
        QtCore.QMetaObject.connectSlotsByName(landsatProcessingPlugin)

    def retranslateUi(self, landsatProcessingPlugin):
        landsatProcessingPlugin.setWindowTitle(QtGui.QApplication.translate("landsatProcessingPlugin", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("landsatProcessingPlugin", "Loaded Metadatafile", None, QtGui.QApplication.UnicodeUTF8))
        self.labelChoosenMetadata.setText(QtGui.QApplication.translate("landsatProcessingPlugin", "\\", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonChooseMetadata.setText(QtGui.QApplication.translate("landsatProcessingPlugin", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBoxMetadata.setTitle(QtGui.QApplication.translate("landsatProcessingPlugin", "Metadata", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidgetMetadata.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("landsatProcessingPlugin", "key", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidgetMetadata.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("landsatProcessingPlugin", "value", None, QtGui.QApplication.UnicodeUTF8))

