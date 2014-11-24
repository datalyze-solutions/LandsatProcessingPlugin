import unittest
import os
from landsatMetadata import *
from landsatConst import *
from landsatExceptions import *

class landsatMetadataUnittest(unittest.TestCase):

  def test_landsatMetadata(self):
    self.assertRaises(ExceptionValueNotInList, landsatMetadata, 'LANDSAT_10')
    self.assertEqual(landsat5MetadataDummy, landsatMetadata('LANDSAT_5').metadata)
    self.assertEqual(landsat7MetadataDummy, landsatMetadata('LANDSAT_7').metadata)

    keywords = {
        'FILE_NAME_BAND_3': 'PRODUCT_METADATA',
        'FILE_NAME_BAND_2': 'PRODUCT_METADATA',
        'FILE_NAME_BAND_1': 'PRODUCT_METADATA',
        'REFLECTIVE_LINES': 'PRODUCT_METADATA',
        'THERMAL_LINES': 'PRODUCT_METADATA',
        'FILE_NAME_BAND_6': 'PRODUCT_METADATA',
        'FILE_NAME_BAND_5': 'PRODUCT_METADATA',
        'FILE_NAME_BAND_4': 'PRODUCT_METADATA',
        'SCENE_CENTER_TIME': 'PRODUCT_METADATA',
        'SPACECRAFT_ID': 'PRODUCT_METADATA',
        'SUN_ELEVATION': 'IMAGE_ATTRIBUTES',
        'THERMAL_SAMPLES': 'PRODUCT_METADATA',
        'REFLECTIVE_SAMPLES': 'PRODUCT_METADATA',
        'FILE_NAME_BAND_7': 'PRODUCT_METADATA',
        'DATE_ACQUIRED': 'PRODUCT_METADATA'
      }
    self.assertEqual(keywords, landsatMetadata('LANDSAT_5').keywords)

    self.assertFalse(landsatMetadata('LANDSAT_5').hasKeyword('Peter Pan'))
    self.assertTrue(landsatMetadata('LANDSAT_5').hasKeyword('FILE_NAME_BAND_1'))

    self.assertEqual(None, landsatMetadata(landsat_type_5).getValue('FILE_NAME_BAND_1'))
    self.assertRaises(ExceptionKeywordNotFound, landsatMetadata('LANDSAT_5').getValue, 'FILE_NAME_BAND_8')

    self.assertEqual(landsat_type_5, landsatMetadata(landsat_type_5).landsatType)
    self.assertNotEqual(landsat_type_7, landsatMetadata(landsat_type_5).landsatType)
    # TODO    
    self.assertRaises(ExceptionValueNotInList, setattr, landsatMetadata(landsat_type_5), "landsatType", 'LANDSAT_10')

    
  def test_landsatMetadataFromMTL(self):
    self.assertRaises(ExceptionPathExistsNot, landsatMetadataFromMTL, '123')
    path = "/media/sdb5/kaotika/Dokumente/BahirDar/LT51690522011273MLK00/LT51690522011273MLK00_MTL.txt"
    metadata = landsatMetadataFromMTL(path)
    # TODO    
    self.assertRaises(ExceptionPathExistsNot, setattr, metadata, "path", '123')
    self.assertEqual(path, metadata.path)

    band1Path = "LT51690522011273MLK00_B1.TIF"
    band2Path = "LT51690522011273MLK00_B2.TIF"
    band3Path = "LT51690522011273MLK00_B3.TIF"
    band4Path = "LT51690522011273MLK00_B4.TIF"
    band5Path = "LT51690522011273MLK00_B5.TIF"
    band6Path = "LT51690522011273MLK00_B6.TIF"
    band7Path = "LT51690522011273MLK00_B7.TIF"
    solarElevation = '60.73930445'
    
    self.assertEqual(solarElevation, metadata.getValue('SUN_ELEVATION'))
    self.assertEqual(band1Path, metadata.getValue('FILE_NAME_BAND_1'))
    self.assertEqual(band2Path, metadata.getValue('FILE_NAME_BAND_2'))
    self.assertEqual(band3Path, metadata.getValue('FILE_NAME_BAND_3'))
    self.assertEqual(band4Path, metadata.getValue('FILE_NAME_BAND_4'))
    self.assertEqual(band5Path, metadata.getValue('FILE_NAME_BAND_5'))
    self.assertEqual(band6Path, metadata.getValue('FILE_NAME_BAND_6'))
    self.assertEqual(band7Path, metadata.getValue('FILE_NAME_BAND_7'))
    

  def test_landsatMetadataFromBandPaths(self):
    basePath = "/media/sdb5/kaotika/Dokumente/BahirDar/LT51690522011273MLK00/"
    band1Path = os.path.join(basePath, "LT51690522011273MLK00_B1.TIF")
    band2Path = os.path.join(basePath, "LT51690522011273MLK00_B2.TIF")
    band3Path = os.path.join(basePath, "LT51690522011273MLK00_B3.TIF")
    band4Path = os.path.join(basePath, "LT51690522011273MLK00_B4.TIF")
    band5Path = os.path.join(basePath, "LT51690522011273MLK00_B5.TIF")
    band6Path = os.path.join(basePath, "LT51690522011273MLK00_B6.TIF")
    band7Path = os.path.join(basePath, "LT51690522011273MLK00_B7.TIF")
    solarElevation = 60.73930445
    acquisitionDateTime = '2011-09-30' + ' ' + '07:34:00.0800250Z'

    metadata = landsatMetadataFromBandPaths(
        landsatType = landsat_type_5,
        pathBand1 = band1Path,
        pathBand2 = band2Path,
        pathBand3 = band3Path,
        pathBand4 = band4Path,
        pathBand5 = band5Path,
        pathBand7 = band7Path,
        solarElevation = solarElevation,
        acquisitionDateTime = acquisitionDateTime
      )
      
    self.assertEqual(landsat_type_5, metadata.landsatType)
    self.assertEqual(band1Path, metadata.pathBand1)
    self.assertEqual(band2Path, metadata.pathBand2)
    self.assertEqual(band3Path, metadata.pathBand3)
    self.assertEqual(band4Path, metadata.pathBand4)
    self.assertEqual(band5Path, metadata.pathBand5)
    self.assertEqual(band7Path, metadata.pathBand7)
    self.assertEqual(solarElevation, metadata.solarElevation)
    self.assertEqual(acquisitionDateTime, metadata.acquisitionDateTime)
    # TODO
    self.assertRaises(ExceptionValueNotBetween, setattr, metadata, "solarElevation", 100)

    
  def test_landsat5MetadataFromBandPaths(self):
    basePath = "/media/sdb5/kaotika/Dokumente/BahirDar/LE71730612003031SGS00/"
    band1Path = os.path.join(basePath, "LE71730612003031SGS00_B1.TIF")
    band2Path = os.path.join(basePath, "LE71730612003031SGS00_B2.TIF")
    band3Path = os.path.join(basePath, "LE71730612003031SGS00_B3.TIF")
    band4Path = os.path.join(basePath, "LE71730612003031SGS00_B4.TIF")
    band5Path = os.path.join(basePath, "LE71730612003031SGS00_B5.TIF")
    band6v1Path = os.path.join(basePath, "LE71730612003031SGS00_B6_VCID_1.TIF")
    band6v2Path = os.path.join(basePath, "LE71730612003031SGS00_B6_VCID_2.TIF")
    band7Path = os.path.join(basePath, "LE71730612003031SGS00_B7.TIF")
    band8Path = os.path.join(basePath, "LE71730612003031SGS00_B8.TIF")
    solarElevation = 53.50130631
    acquisitionDateTime = '2003-01-31' + ' ' + '08:02:37.7196561Z'

    metadata = landsat7MetadataFromBandPaths(
        landsatType = landsat_type_7,
        pathBand1 = band1Path,
        pathBand2 = band2Path,
        pathBand3 = band3Path,
        pathBand4 = band4Path,
        pathBand5 = band5Path,
        pathBand6v1 = band6v1Path,
        pathBand6v2 = band6v2Path,
        pathBand7 = band7Path,
        pathBand8 = band8Path,
        solarElevation = solarElevation,
        acquisitionDateTime = acquisitionDateTime
      )

    self.assertEqual(landsat_type_7, metadata.landsatType)
    self.assertEqual(band1Path, metadata.pathBand1)
    self.assertEqual(band2Path, metadata.pathBand2)
    self.assertEqual(band3Path, metadata.pathBand3)
    self.assertEqual(band4Path, metadata.pathBand4)
    self.assertEqual(band5Path, metadata.pathBand5)
    self.assertEqual(band6v1Path, metadata.pathBand6v1)
    self.assertEqual(band6v2Path, metadata.pathBand6v2)
    self.assertEqual(band7Path, metadata.pathBand7)
    self.assertEqual(band8Path, metadata.pathBand8)
    self.assertEqual(solarElevation, metadata.solarElevation)
    self.assertEqual(acquisitionDateTime, metadata.acquisitionDateTime)

    self.assertRaises(
      ExceptionNoLandsat7Image,
      landsat7MetadataFromBandPaths,
      landsat_type_5, band1Path, band2Path, band3Path, band4Path, band5Path, band6v1Path, band6v2Path, band7Path, band8Path, acquisitionDateTime, solarElevation
    )
    # TODO
    #self.assertRaises(ExceptionValueNotBetween, metadata.solarElevation,

  #def test_landsat5MetadataFromBandPaths(self):
    #basePath = "/media/sdb5/kaotika/Dokumente/BahirDar/LE71730612003031SGS00/"
    #band1Path = os.path.join(basePath, "LT51690522011273MLK00_B1.TIF")
    #band2Path = os.path.join(basePath, "LT51690522011273MLK00_B2.TIF")
    #band3Path = os.path.join(basePath, "LT51690522011273MLK00_B3.TIF")
    #band4Path = os.path.join(basePath, "LT51690522011273MLK00_B4.TIF")
    #band5Path = os.path.join(basePath, "LT51690522011273MLK00_B5.TIF")
    #band6Path = os.path.join(basePath, "LT51690522011273MLK00_B6.TIF")
    #band7Path = os.path.join(basePath, "LT51690522011273MLK00_B7.TIF")
    #solarElevation = 60.73930445
    #acquisitionDateTime = '2011-09-30' + ' ' + '07:34:00.0800250Z'

    #metadata = landsat5MetadataFromBandPaths(
        #landsatType = landsat_type_5,
        #pathBand1 = band1Path,
        #pathBand2 = band2Path,
        #pathBand3 = band3Path,
        #pathBand4 = band4Path,
        #pathBand5 = band5Path,
        #pathBand6 = band6Path,
        #pathBand7 = band7Path,
        #solarElevation = solarElevation,
        #acquisitionDateTime = acquisitionDateTime
      #)

    #self.assertEqual(landsat_type_5, metadata.landsatType)
    #self.assertEqual(band1Path, metadata.pathBand1)
    #self.assertEqual(band2Path, metadata.pathBand2)
    #self.assertEqual(band3Path, metadata.pathBand3)
    #self.assertEqual(band4Path, metadata.pathBand4)
    #self.assertEqual(band5Path, metadata.pathBand5)
    #self.assertEqual(band6Path, metadata.pathBand6)
    #self.assertEqual(band7Path, metadata.pathBand7)
    #self.assertEqual(solarElevation, metadata.solarElevation)
    #self.assertEqual(acquisitionDateTime, metadata.acquisitionDateTime)
    ## TODO
    #self.assertRaises(ExceptionValueNotBetween, metadata.solarElevation,    