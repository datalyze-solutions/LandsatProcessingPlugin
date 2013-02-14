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

from PyQt4 import QtCore, QtGui
from ui_landsatprocessingplugin import Ui_landsatProcessingPlugin
# create the dialog for zoom to point


class landsatProcessingPluginDialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_landsatProcessingPlugin()
        self.ui.setupUi(self)
