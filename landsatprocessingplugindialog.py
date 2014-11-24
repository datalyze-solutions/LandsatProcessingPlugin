# -*- coding: utf-8 -*-
"""
/***************************************************************************
 landsatProcessingPluginDialog
                                 A QGIS plugin
 Provides several processing steps on Landsat data. Landsat5 to Landsat7 conversion, DNs to radiance and reflectance conversion, TIR to temperature conversion, Indice calculation(NDVI, SAVI, NDWI, NDSI, tasseled cap indices)
                             -------------------
        begin                : 2013-02-14
        copyright            : (C) 2013 by Matthias Ludwig - Datalyze Solutions
        email                : development@datalyze-solutions.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ui_landsatprocessingplugin import Ui_landsatProcessingPlugin

class Communicate(QObject):    
    sendFilename = pyqtSignal(QString)
    doNothingSignal = pyqtSignal()
    
class landsatProcessingPluginDialog(QDialog):
    def __init__(self):
	QDialog.__init__(self)

	# Set up the user interface from Designer.
	self.ui = Ui_landsatProcessingPlugin()
	self.ui.setupUi(self)
	self.ui.buttonChooseMetadata.clicked.connect(self.test)
	
	self.filestuff = Communicate()

    def test(self):
	print "hallo welt"
	filename = self.getFile()

	self.filestuff.sendFilename.emit(filename)
	self.filestuff.doNothingSignal.emit()
	    
	#self.emit(SIGNAL("xyCoordinates(const QString &)"), QString(filename))
	
    def getFile(self, filterList = 'Alle Dateien(*.*)'):
	return QFileDialog.getOpenFileName(self, 'Datei wählen', '.', filterList)
	#try:
	    #return QFileDialog.getOpenFileName(self.iface.mainWindow(), 'Datei wählen', '.', filterList)
	#except:
	    #pass
	  
	  
	  
    #item = QtGui.QTreeWidgetItem(['name', 'tags'])
    #item2 = QtGui.QTreeWidgetItem(['name2', 'tags2'])
    #item.setCheckState(0,QtCore.Qt.Checked)
    ##self.ui.treeWidgetMetadata.addTopLevelItem(item)
    #self.ui.treeWidgetMetadata.insertTopLevelItem(0, item)
    #self.ui.treeWidgetMetadata.insertTopLevelItem(0, item2)
       
  #def updateTreeWidget():
    #update(metadata)