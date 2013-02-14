# -*- coding: utf-8 -*-
"""
/***************************************************************************
 landsatProcessingPlugin
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
 This script initializes the plugin, making it known to QGIS.
"""


def name():
    return "Landsat Processing Plugin"


def description():
    return "Provides several processing steps on Landsat data. Landsat5 to Landsat7 conversion, DNs to radiance and reflectance conversion, TIR to temperature conversion, Indice calculation(NDVI, SAVI, NDWI, NDSI, tasseled cap indices)"


def version():
    return "Version 0.1"


def icon():
    return "icon.png"


def qgisMinimumVersion():
    return "1.8"

def author():
    return "Matthias Ludwig - Datalyze Solutions"

def email():
    return "development@datalyze-solutions.com"

def classFactory(iface):
    # load landsatProcessingPlugin class from file landsatProcessingPlugin
    from landsatprocessingplugin import landsatProcessingPlugin
    return landsatProcessingPlugin(iface)
