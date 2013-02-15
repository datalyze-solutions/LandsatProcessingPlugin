# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_landsatprocessingplugin.ui'
#
# Created: Thu Feb 14 17:26:58 2013
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_landsatProcessingPlugin(object):
    def setupUi(self, landsatProcessingPlugin):
        landsatProcessingPlugin.setObjectName("landsatProcessingPlugin")
        landsatProcessingPlugin.resize(500, 369)
        self.horizontalLayout = QtGui.QHBoxLayout(landsatProcessingPlugin)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.treeWidgetFileSystem = QtGui.QTreeWidget(landsatProcessingPlugin)
        self.treeWidgetFileSystem.setObjectName("treeWidgetFileSystem")
        self.treeWidgetFileSystem.headerItem().setText(0, "1")
        self.horizontalLayout.addWidget(self.treeWidgetFileSystem)
        self.groupBoxMetadata = QtGui.QGroupBox(landsatProcessingPlugin)
        self.groupBoxMetadata.setObjectName("groupBoxMetadata")
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBoxMetadata)
        self.verticalLayout.setObjectName("verticalLayout")
        self.treeWidgetMetadata = QtGui.QTreeWidget(self.groupBoxMetadata)
        self.treeWidgetMetadata.setColumnCount(2)
        self.treeWidgetMetadata.setObjectName("treeWidgetMetadata")
        self.verticalLayout.addWidget(self.treeWidgetMetadata)
        self.horizontalLayout.addWidget(self.groupBoxMetadata)

        self.retranslateUi(landsatProcessingPlugin)
        QtCore.QMetaObject.connectSlotsByName(landsatProcessingPlugin)

    def retranslateUi(self, landsatProcessingPlugin):
        landsatProcessingPlugin.setWindowTitle(QtGui.QApplication.translate("landsatProcessingPlugin", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBoxMetadata.setTitle(QtGui.QApplication.translate("landsatProcessingPlugin", "Metadata", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidgetMetadata.headerItem().setText(0, QtGui.QApplication.translate("landsatProcessingPlugin", "Property", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidgetMetadata.headerItem().setText(1, QtGui.QApplication.translate("landsatProcessingPlugin", "Value", None, QtGui.QApplication.UnicodeUTF8))

