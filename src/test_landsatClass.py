import unittest
import landsatClass

# python -m unittest test_landsatClass

class landsatUnittest(unittest.TestCase):  
  
  # method name has to start with test_
  def test_Landsat5metadataFromPath(self):
    band1Path = "/media/sdb5/kaotika/Dokumente/BahirDar/LT51690522011273MLK00/LT51690522011273MLK00_B1.TIF"
    band2Path = "/media/sdb5/kaotika/Dokumente/BahirDar/LT51690522011273MLK00/LT51690522011273MLK00_B2.TIF"
    band3Path = "/media/sdb5/kaotika/Dokumente/BahirDar/LT51690522011273MLK00/LT51690522011273MLK00_B3.TIF"
    band4Path = "/media/sdb5/kaotika/Dokumente/BahirDar/LT51690522011273MLK00/LT51690522011273MLK00_B4.TIF"
    band5Path = "/media/sdb5/kaotika/Dokumente/BahirDar/LT51690522011273MLK00/LT51690522011273MLK00_B5.TIF"
    band6Path = "/media/sdb5/kaotika/Dokumente/BahirDar/LT51690522011273MLK00/LT51690522011273MLK00_B6.TIF"
    band7Path = "/media/sdb5/kaotika/Dokumente/BahirDar/LT51690522011273MLK00/LT51690522011273MLK00_B7.TIF"
    metadata = landsatClass.landsatMetadataFromPaths(
      landsatType = 'LANDSAT_5',
      pathBand1 = band1Path,
      pathBand2 = band2Path,
      pathBand3 = band3Path,
      pathBand4 = band4Path,
      pathBand5 = band5Path,
      pathBand6 = band6Path,
      pathBand7 = band7Path,
      acquisitionDateTime = '2011-09-30' + ' ' + '07:34:00.0800250Z',
      solarElevation = '60.73930445'
    )
    

  
  #def test_Landsat5metadata(self):
    #path = "/media/sdb5/kaotika/Dokumente/BahirDar/LT51690522011273MLK00/LT51690522011273MLK00_MTL.txt"
    #metadata = landsatClass.landsatMetadata(path)
    #self.assertEqual(path, metadata.path)
    #self.assertEqual('LANDSAT_5', metadata.landsatType)   
    
  #def test_Landsat7metadata(self):
    #path = "/media/sdb5/kaotika/Dokumente/BahirDar/LE71730612003031SGS00/LE71730612003031SGS00_MTL.txt"
    #metadata = landsatClass.landsatMetadata(path)
    #self.assertEqual(path, metadata.path)
    #self.assertEqual('LANDSAT_7', metadata.landsatType)

  #def test_Landsat5(self):
    #landsat5MetadataPath = "/media/sdb5/kaotika/Dokumente/BahirDar/LT51690522011273MLK00/LT51690522011273MLK00_MTL.txt"
    #landsat7MetadataPath = "/media/sdb5/kaotika/Dokumente/BahirDar/LE71730612003031SGS00/LE71730612003031SGS00_MTL.txt"
    #metadata = landsatClass.landsatMetadata(landsat5MetadataPath)
    #landsatInitializationByMetadata = landsatClass.landsatInitializationByMetadata(metadata)
    #self.assertRaises(landsatClass.ExceptionWrongClass, landsatClass.landsat5Processor, 'text')
    #processor = landsatClass.landsat5Processor(landsatInitializationByMetadata)

    #sizeX = 7931
    #sizeY = 6961
    #self.assertEqual(sizeX, processor.RasterXSize)
    #self.assertEqual(sizeY, processor.RasterYSize)
    #testProjection = 'PROJCS["WGS 84 / UTM zone 37N",GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433],AUTHORITY["EPSG","4326"]],PROJECTION["Transverse_Mercator"],PARAMETER["latitude_of_origin",0],PARAMETER["central_meridian",39],PARAMETER["scale_factor",0.9996],PARAMETER["false_easting",500000],PARAMETER["false_northing",0],UNIT["metre",1,AUTHORITY["EPSG","9001"]],AUTHORITY["EPSG","32637"]]'    
    #self.assertEqual(testProjection, processor.projection)
    #testTransformation = (309585.0, 30.0, 0.0, 1381815.0, 0.0, -30.0)
    #self.assertEqual(testTransformation, processor.transformation)
    #self.assertEqual(0.5, processor.soilBrightnessCorrectionFactor)

    #self.assertIsInstance(processor.band1, landsatClass.landsat5Band)
    #self.assertIsInstance(processor.band2, landsatClass.landsat5Band)
    #self.assertIsInstance(processor.band3, landsatClass.landsat5Band)
    #self.assertIsInstance(processor.band4, landsatClass.landsat5Band)
    #self.assertIsInstance(processor.band5, landsatClass.landsat5Band)
    #self.assertIsInstance(processor.band6, landsatClass.landsat5Band)
    #self.assertIsInstance(processor.band7, landsatClass.landsat5Band)

    #self.assertEqual('LT51690522011273MLK00_B1.TIF', processor.band1.filename)
    #self.assertEqual('LT51690522011273MLK00_B2.TIF', processor.band2.filename)
    #self.assertEqual('LT51690522011273MLK00_B3.TIF', processor.band3.filename)
    #self.assertEqual('LT51690522011273MLK00_B4.TIF', processor.band4.filename)
    #self.assertEqual('LT51690522011273MLK00_B5.TIF', processor.band5.filename)
    #self.assertEqual('LT51690522011273MLK00_B6.TIF', processor.band6.filename)
    #self.assertEqual('LT51690522011273MLK00_B7.TIF', processor.band7.filename)

    #self.assertEqual('1', processor.band1.bandNumber)
    #self.assertEqual('2', processor.band2.bandNumber)
    #self.assertEqual('3', processor.band3.bandNumber)
    #self.assertEqual('4', processor.band4.bandNumber)
    #self.assertEqual('5', processor.band5.bandNumber)
    #self.assertEqual('6', processor.band6.bandNumber)
    #self.assertEqual('7', processor.band7.bandNumber)

    #self.assertEqual(1.0016041994094849, processor.band1.earthSunDistance)
    #self.assertEqual(1.0601008480237435, processor.band1.solarElevation)
    #self.assertEqual('2011-09-30 07:34:00.0800250Z', processor.band1.acquisitionDateTime)
    
    #testLocationX = 1574
    #testLocationY = 2329
    ##self.assertFalse(processor.band1.noDataMask[10][1246])    
    ##self.assertTrue(processor.band1.noDataMask[testLocationY][testLocationX])
    ##self.assertEqual(87, processor.band1.imageLS5[testLocationY][testLocationX])
    ##self.assertEqual(43, processor.band2.imageLS5[testLocationY][testLocationX])
    ##self.assertEqual(45, processor.band3.imageLS5[testLocationY][testLocationX])
    ##self.assertEqual(92, processor.band4.imageLS5[testLocationY][testLocationX])
    ##self.assertEqual(86, processor.band5.imageLS5[testLocationY][testLocationX])
    ##self.assertEqual(134, processor.band6.imageLS5[testLocationY][testLocationX])
    ##self.assertEqual(35, processor.band7.imageLS5[testLocationY][testLocationX])

    ##self.assertEqual(86.250999999999991, processor.band1.imageLS7[testLocationY][testLocationX])
    ##self.assertEqual(78.947999999999993, processor.band2.imageLS7[testLocationY][testLocationX])
    ##self.assertEqual(71.710000000000008, processor.band3.imageLS7[testLocationY][testLocationX])
    ##self.assertEqual(136.084, processor.band4.imageLS7[testLocationY][testLocationX])
    ##self.assertEqual(91.583999999999989, processor.band5.imageLS7[testLocationY][testLocationX])
    ##self.assertEqual(134, processor.band6.imageLS7[testLocationY][testLocationX])
    ##self.assertEqual(51.399999999999999, processor.band7.imageLS7[testLocationY][testLocationX])
    
    ##self.assertEqual(60.187103739999984, processor.band1.radiance[testLocationY][testLocationX])
    ##self.assertEqual(55.865162411999989, processor.band2.radiance[testLocationY][testLocationX])
    ##self.assertEqual(38.958808340000012, processor.band3.radiance[testLocationY][testLocationX])
    ##self.assertEqual(81.321644176000007, processor.band4.radiance[testLocationY][testLocationX])
    ##self.assertEqual(10.429732479999998, processor.band5.radiance[testLocationY][testLocationX])
    ##self.assertEqual(8.6319200000000009, processor.band6.radiance[testLocationY][testLocationX])
    ##self.assertEqual(1.8663571999999999, processor.band7.radiance[testLocationY][testLocationX])

    ##self.assertEqual(0.10888034546010468, processor.band1.reflectance[testLocationY][testLocationX])
    ##self.assertEqual(0.11137994066584163, processor.band2.reflectance[testLocationY][testLocationX])
    ##self.assertEqual(0.09180949939372389, processor.band3.reflectance[testLocationY][testLocationX])
    ##self.assertEqual(0.28275787749128928, processor.band4.reflectance[testLocationY][testLocationX])
    ##self.assertEqual(0.16325311412667493, processor.band5.reflectance[testLocationY][testLocationX])   
    ###self.assertEqual(8.6319200000000009, processor.band6.reflectance[testLocationY][testLocationX])
    ##self.assertEqual(0.079416580996734043, processor.band7.reflectance[testLocationY][testLocationX])
    
    #self.assertIsInstance(processor.band1.dataset, landsatClass.gdal.Dataset)
    #self.assertEqual(testProjection, processor.band1.projection)
    #self.assertEqual(testTransformation, processor.band1.transformation)
    #self.assertEqual(sizeX, processor.band1.RasterXSize)
    #self.assertEqual(sizeY, processor.band1.RasterYSize)

    ##self.assertEqual(0.50978379293342413, processor.ndvi[testLocationY][testLocationX])
    ##self.assertEqual(-0.26794129653866811, processor.ndsi[testLocationY][testLocationX])
    ##self.assertEqual(-0.28010226095812069, processor.ndwi[testLocationY][testLocationX])
    #self.assertEqual(0.32750200238032257, processor.savi[testLocationY][testLocationX])
    
    

    ##self.assertRaises(landsatClass.ExceptionPathExistsNot, landsatClass.landsatInitializationByPath('/not_existing_path', '1', 'LANDSAT_7') )

  #def test_systemInformation(self):
    #systemInformation = landsatClass.systemInformation()
    #self.assertIsInstance(systemInformation.availableMemory, int)
    #self.assertIsInstance(systemInformation.freeMemory, int)
    #self.assertTrue(systemInformation.availableMemory > 0)
    #self.assertTrue(systemInformation.freeMemory > 0)

    