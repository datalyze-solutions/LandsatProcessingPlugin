# -*- coding: utf-8 -*-

import sys

import os
from osgeo import gdal
from osgeo.gdalconst import *
import numpy

# for system information like free memory, max. memory, etc.
import psutil

# http://rhodesmill.org/pyephem/
# pip install pyephem
import ephem

# load landsat modules
from landsatConst import *
from landsatMetadata import *
from landsatExceptions import *

gdal.UseExceptions()

###### Helper Objects

class systemInformation(object):

  @property
  def availableMemory(self):
    return int(psutil.phymem_usage()[0] / 1024**2)

  @property
  def freeMemory(self):
    return int(psutil.phymem_usage()[2] / 1024**2)
 
# notice: http://docs.scipy.org/doc/numpy/user/basics.subclassing.html
class ExtendedNumpyArray(numpy.ndarray):

  def __new__(cls, input_array, projection, transformation, fileFormat = 'GTiff', dataType = GDT_Float32):
    # Input array is an already formed ndarray instance
    # We first cast to be our class type
    obj = numpy.asarray(input_array).view(cls)
    # add the new attribute to the created instance
    obj.fileFormat = fileFormat
    obj.dataType = dataType
    obj.transformation = transformation
    obj.projection = projection
    try:
      # !!! reverse order for X -> index 1 and Y -> index 0
      obj.RasterXSize = input_array.shape[1]
      obj.RasterYSize = input_array.shape[0]
    except IndexError:
      raise Exception2DarrayNeeded(input_array.shape)
    # Finally, we must return the newly created object:
    return obj

  def __array_finalize__(self, obj):
    # see InfoArray.__array_finalize__ for comments
    if obj is None: return
    self.fileFormat = getattr(obj, 'fileFormat', None)
    self.dataType = getattr(obj, 'dataType', None)
    self.transformation = getattr(obj, 'transformation', None)
    self.projection = getattr(obj, 'projection', None)
    self.RasterXSize = getattr(obj, 'RasterXSize', None)
    self.RasterYSize = getattr(obj, 'RasterYSize', None)
  
  def save(self, outputPath):
    if not os.path.exists(outputPath):
      tiffDriver = gdal.GetDriverByName(self.fileFormat)
      outputDataset = tiffDriver.Create(outputPath, self.RasterXSize, self.RasterYSize, 1, self.dataType)

      if self.transformation is not None and self.transformation != (0.0, 1.0, 0.0, 0.0, 0.0, 1.0):
	outputDataset.SetGeoTransform(self.transformation)

      if self.projection is not None and len(self.projection) > 0:
	outputDataset.SetProjection(self.projection)

      outputBand = outputDataset.GetRasterBand(1)
      outputBand.WriteArray(self)
      outputBand = None

      outputDataset = None
      return True
    else:
      raise ExceptionPathExists(outputPath)

            
###### Initialization Objects

#class landsatInitialization(object):

  #def __init__(self, landsatType):
    #self.typeLandsat5 = 'LANDSAT_5'
    #self.typeLandsat7 = 'LANDSAT_7'
    #if landsatType not in [self.typeLandsat5, self.typeLandsat7]:
      #raise ExceptionNoLandsatImage()

    #if landsatType == self.__typeLandsat5:
      #self.bandNumbers = ['1', '2', '3', '4', '5', '6', '7']
    #elif landsatType == self.__typeLandsat7:
      #self.bandNumbers = ['1', '2', '3', '4', '5', '6_VCID_1', '6_VCID_2', '7', '8']
    #else:
      #raise ExceptionValueNotInList(landsatType, [self.__typeLandsat5, self.__typeLandsat7])
    #self.bandNumber = bandNumber

  #@property
  #def bandNumber(self):
    #return self.__bandNumber

  #@bandNumber.setter
  #def bandNumber(self, bandNumber):
    #if bandNumber in self.bandNumbers:
      #self.__bandNumber = bandNumber
    #else:
      #raise ExceptionValueNotInList(bandNumber, self.bandNumbers)

#class landsatInitializationByPath(landsatInitialization):

  #def __init__(self, band1Path, band2Path, band3Path, band4Path, band5Path, band6Path, band7Path):
    #super(landsatInitializationByPath, self).__init__(landsatType)
    #if os.path.exists(band1Path):
      #self.band1Path = band1Path
    #else:
      #raise ExceptionPathExistsNot(band1Path)

      
#class landsatInitializationByMetadata(landsatInitialization):

  #def __init__(self, metadata):
    #if isinstance(metadata, landsatMetadata):
      #self.metadata = metadata
      #super(landsatInitializationByMetadata, self).__init__(self.metadata.landsatType)
    #else:
      #raise ExceptionWrongClass(metadata, landsatMetadata)

    
###### Processor Objects

class landsatProcessor(object):

  def __init__(self, metadata):
    self.metadata = metadata
    self.systemInformation = systemInformation()
    
    self.__soilBrightnessCorrectionFactor = 0.5
    self.__initializeImages()
    
  def __del__(self):
    self.__initializeImages()

  def __initializeImages(self):
    self.__ndvi = None
    self.__savi = None
    self.__ndwi = None
    self.__ndsi = None
    self.__tasseledCapBrightness = None
    self.__tasseledCapGreenness = None
    self.__tasseledCapWetness = None
    
  # TODO: read from metadata instead of band
  @property
  def transformation(self):
    return self.band3.transformation

  # TODO: read from metadata instead of band    
  @property
  def projection(self):
    return self.band3.projection

  @property
  def RasterXSize(self):
    return int(self.metadata.getValue('REFLECTIVE_SAMPLES'))

  @property
  def RasterYSize(self):
    return int(self.metadata.getValue('REFLECTIVE_LINES'))

  @property
  def noDataMask(self):
    return self.band1.noDataMask * self.band2.noDataMask * self.band3.noDataMask * self.band4.noDataMask * self.band5.noDataMask * self.band7.noDataMask
    
  # Normalized Differential Vegetation Index
  @property
  def ndvi(self):
    if self.__ndvi == None:
      self.__ndvi = ExtendedNumpyArray(
	  input_array = ((self.band4.reflectance - self.band3.reflectance) / (self.band4.reflectance + self.band3.reflectance)) * self.noDataMask,
	  transformation = self.transformation,
	  projection = self.projection
      )
    try:
      return self.__ndvi
    finally:
      if self.systemInformation.freeMemory < 16 * 1024:
        self.__ndvi = None

  @property
  def soilBrightnessCorrectionFactor(self):
    return self.__soilBrightnessCorrectionFactor

  @soilBrightnessCorrectionFactor.setter
  def soilBrightnessCorrectionFactor(self, value):
    self.__soilBrightnessCorrectionFactor = value

  # Soil Adjusted Vegetation Index
  @property
  def savi(self):
    if self.__savi == None:
      self.__savi = ExtendedNumpyArray(
	  input_array = (1.0 + self.soilBrightnessCorrectionFactor) * (self.band4.reflectance - self.band3.reflectance) / (self.band4.reflectance + self.band3.reflectance + self.soilBrightnessCorrectionFactor) * self.noDataMask,
	  transformation = self.transformation,
	  projection = self.projection
      )
    try:
      return self.__savi
    finally:
      if self.systemInformation.freeMemory < 16 * 1024:
        self.__savi = None

  # Normalized Differential Water Index
  @property
  def ndwi(self):
    if self.__ndwi == None:
      self.__ndwi = ExtendedNumpyArray(
	  input_array = (self.band3.reflectance - self.band5.reflectance) / (self.band3.reflectance + self.band5.reflectance) * self.noDataMask,
	  transformation = self.transformation,
	  projection = self.projection
      )
    try:
      return self.__ndwi
    finally:
      if self.systemInformation.freeMemory < 16 * 1024:
        self.__ndwi = None

  # Normalized Differential Soil Index
  @property
  def ndsi(self):
    if self.__ndsi == None:
      self.__ndsi = ExtendedNumpyArray(
	  input_array = (self.band5.reflectance - self.band4.reflectance) / (self.band5.reflectance + self.band4.reflectance) * self.noDataMask,
	  transformation = self.transformation,
	  projection = self.projection
      )
    try:
      return self.__ndsi
    finally:
      if self.systemInformation.freeMemory < 16 * 1024:
        self.__ndsi = None

  @property
  def tasseledCapBrightness(self):
    if self.__tasseledCapBrightness == None:
      self.__tasseledCapBrightness = ExtendedNumpyArray(
          input_array = self.__tasseledCapIndex('brightness') * self.noDataMask,
          transformation = self.transformation,
          projection = self.projection
      )
    try:
      return self.__tasseledCapBrightness
    finally:
      if self.systemInformation.freeMemory < 16 * 1024:
        self.__tasseledCapBrightness = None

  @property
  def tasseledCapGreenness(self):
    if self.__tasseledCapGreenness == None:
      self.__tasseledCapGreenness = ExtendedNumpyArray(
          input_array = self.__tasseledCapIndex('greenness') * self.noDataMask,
          transformation = self.transformation,
          projection = self.projection
      )
    try:
      return self.__tasseledCapGreenness
    finally:
      if self.systemInformation.freeMemory < 16 * 1024:
        self.__tasseledCapGreenness = None

  @property
  def tasseledCapWetness(self):
    if self.__tasseledCapWetness == None:
      self.__tasseledCapWetness = ExtendedNumpyArray(
          input_array = self.__tasseledCapIndex('wetness') * self.noDataMask,
          transformation = self.transformation,
          projection = self.projection
      )
    try:
      return self.__tasseledCapWetness
    finally:
      if self.systemInformation.freeMemory < 16 * 1024:
        self.__tasseledCapWetness = None      
    
  def __tasseledCapIndex(self, index):
    if index in ['brightness', 'greenness', 'wetness']:
      tasseledCapIndex = (self.band1.reflectance * getattr(self.band1, index))
      tasseledCapIndex += (self.band2.reflectance * getattr(self.band2, index))
      tasseledCapIndex += (self.band3.reflectance * getattr(self.band3, index))
      tasseledCapIndex += (self.band4.reflectance * getattr(self.band4, index))
      tasseledCapIndex += (self.band5.reflectance * getattr(self.band5, index))
      tasseledCapIndex += (self.band7.reflectance * getattr(self.band7, index))
      return tasseledCapIndex
    else:
      raise ExceptionKeywordNotFound(index)
  
  def GetColorComposit321(self, outputPath):
    return self.__GetMultiBandImage(outputPath, bands = [self.band3.reflectance, self.band2.reflectance, self.band1.reflectance])
    
  def GetColorComposit432(self, outputPath):
    return self.__GetMultiBandImage(outputPath, bands = [self.band4.reflectance, self.band3.reflectance, self.band2.reflectance])

  def GetColorComposit453(self, outputPath):
    return self.__GetMultiBandImage(outputPath, bands = [self.band4.reflectance, self.band5.reflectance, self.band3.reflectance])
    self.metadata = landsatMetadata(metadataPath)
  def GetColorComposit742(self, outputPath):
    return self.__GetMultiBandImage(outputPath, bands = [self.band7.reflectance, self.band4.reflectance, self.band2.reflectance])
    
  def __GetMultiBandImage(self,
	outputPath,
	bands,
	dataType = GDT_Float32,
	fileFormat = 'GTiff'
      ):
    if not os.path.exists(outputPath):
      tiffDriver = gdal.GetDriverByName(fileFormat)
      outputDataset = tiffDriver.Create(outputPath, self.RasterXSize, self.RasterYSize, len(bands), dataType)

      if self.transformation is not None and self.transformation != (0.0, 1.0, 0.0, 0.0, 0.0, 1.0):
	outputDataset.SetGeoTransform(self.transformation)

      if self.projection is not None and len(self.projection) > 0:
	outputDataset.SetProjection(self.projection)

      for bandNumber in range(len(bands)):
	outputBand = outputDataset.GetRasterBand(bandNumber + 1)
	outputBand.WriteArray(bands[bandNumber] * self.noDataMask)

      return outputDataset
    else:
      raise ExceptionPathExists(outputPath)

class landsat5Processor(landsatProcessor):

  def __init__(self, metadata):
    super(landsat5Processor, self).__init__(metadata)
    if self.metadata.landsatType == landsatType5:
      self.band1 = landsat5Band(self.metadata, '1')
      self.band2 = landsat5Band(self.metadata, '2')
      self.band3 = landsat5Band(self.metadata, '3')
      self.band4 = landsat5Band(self.metadata, '4')
      self.band5 = landsat5Band(self.metadata, '5')
      # TODO: seperate band 6 in extra class
      self.band6 = landsat5Band(self.metadata, '6')
      self.band7 = landsat5Band(self.metadata, '7')
    else:
      raise Exception('Not a Landsat 5 Image')
     
    
###### Band Objects

class landsatBand(object):

  def __init__(self, metadata=None, bandNumber=None):


    if metadata == None and bandNumber == None :
      pass
      
    self.systemInformation = systemInformation()    
    self.__allMetadata = metadata

  
class landsat5Band(object):

  def __init__(self, metadata, bandNumber):
    self.systemInformation = systemInformation()
  
    self.__allMetadata = metadata
    if not self.__allMetadata.landsatType == landsatType5:
      raise Exception('Not a Landsat 5 Image')
    
    self.bandNumbers = ['1', '2', '3', '4', '5', '6', '7']
    self.bandNumber = bandNumber

    self.__initializeImages()
    self.__initializeKeywords()
    self.__initializeConvertionValues()

    self.path = os.path.join(os.path.dirname(self.__allMetadata.path), self.filename )

  def __del__(self):
    self.__initializeImages()

  def __initializeImages(self):
    self.__dataset = None
    self.__imageLS5 = None
    self.__imageLS7 = None
    self.__radiance = None
    self.__reflectance = None
    
  def __initializeKeywords(self):
    self.__keywords = {}
    self.__keywords['filename'] = ('FILE_NAME_BAND_%s' % self.bandNumber)
    # not needed at the moment
    #self.__keywords['radiance_max'] = ('RADIANCE_MAXIMUM_BAND_%s' % self.bandNumber)
    #self.__keywords['radiance_min'] = ('RADIANCE_MINIMUM_BAND_%s' % self.bandNumber)
    #self.__keywords['quantize_max'] = ('QUANTIZE_CAL_MAX_BAND_%s' % self.bandNumber)
    #self.__keywords['quantize_min'] = ('QUANTIZE_CAL_MIN_BAND_%s' % self.bandNumber)
    #self.__keywords['correction_gain'] = ('CORRECTION_GAIN_BAND_%s' % self.bandNumber)
    #self.__keywords['correction_bias'] = ('CORRECTION_BIAS_BAND_%s' % self.bandNumber)
    #self.__keywords['radiance_mult'] = ('RADIANCE_MULT_BAND_%s' % self.bandNumber)
    #self.__keywords['radiance_add'] = ('RADIANCE_ADD_BAND_%s' % self.bandNumber)
    
  def __initializeConvertionValues(self):
    if self.bandNumber == '1':
      self.slope = 0.943
      self.intercept = 4.21
      self.gain = 0.778740
      self.bias = -6.98
      self.Esun = 1997
      self.brightness = 0.3561
      self.greenness = -0.3344
      self.wetness = 0.2626
    elif self.bandNumber == '2':
      self.slope = 1.776
      self.intercept = 2.58
      self.gain = 0.798819
      self.bias = -7.20
      self.Esun = 1812
      self.brightness = 0.3972
      self.greenness = -0.3544
      self.wetness = 0.2141
    elif self.bandNumber == '3':
      self.slope = 1.538
      self.intercept = 2.50
      self.gain = 0.621654
      self.bias = -5.62
      self.Esun = 1533
      self.brightness = 0.3904
      self.greenness = -0.4556
      self.wetness = 0.0926
    elif self.bandNumber == '4':
      self.slope = 1.427
      self.intercept = 4.80
      self.gain = 0.639764
      self.bias = -5.74
      self.Esun = 1039
      self.brightness = 0.6966
      self.greenness = 0.6966
      self.wetness = 0.0656
    elif self.bandNumber == '5':
      self.slope = 0.984
      self.intercept = 6.96
      self.gain = 0.126220
      self.bias = -1.13
      self.Esun = 230.8
      self.brightness = 0.6966
      self.greenness = 0.6966
      self.wetness = 0.0656
    elif self.bandNumber == '6':
      self.slope = 1
      self.intercept = 0
      self.gain = 0.05518
      self.bias = 1.2378
      self.Esun = None
      self.brightness = None
      self.greenness = None
      self.wetness = None
    elif self.bandNumber == '7':
      self.slope = 1.304
      self.intercept = 5.76
      self.gain = 0.043898
      self.bias = -0.39
      self.Esun = 84.9
      self.brightness = 0.1596
      self.greenness = -0.2630
      self.wetness = -0.5388
     
  @property
  def bandNumber(self):
    return self.__bandNumber

  @bandNumber.setter
  def bandNumber(self, bandNumber):
    if bandNumber in self.bandNumbers:
      self.__bandNumber = bandNumber
    else:
      raise ExceptionValueNotInList(bandNumber, self.bandNumbers)
   
  @property
  def __allMetadata(self):
    return self.___allMetadata

  @__allMetadata.setter
  def __allMetadata(self, metadata):
    if isinstance(metadata, landsatMetadata):
      self.___allMetadata = metadata
    else:
      raise ExceptionWrongClass(metadata, landsatMetadata)
    
  @property
  def path(self):    
    if os.path.exists(self.__path):
      return self.__path
    else:
      raise ExceptionPathExistsNot(self.__path)

  @path.setter
  def path(self, path):
    if os.path.exists(path):
      self.__path = path
    else:
      raise ExceptionPathExistsNot(path)    

  @property
  def metadata(self):
    metadata = {}
    for keyword in self.__keywords.values():
      metadata[keyword] = self.__allMetadata.getValue(keyword)
    return metadata

  @property
  def filename(self):
    return self.__allMetadata.getValue(self.__keywords['filename'])

  # not needed at the moment
  #@property
  #def radiance_max(self):
    #return self.__allMetadata.getValue(self.__keywords['radiance_max'])

  #@property
  #def radiance_min(self):
    #return self.__allMetadata.getValue(self.__keywords['radiance_min'])

  #@property
  #def radiance_mult(self):
    #return self.__allMetadata.getValue(self.__keywords['radiance_mult'])

  #@property
  #def radiance_add(self):
    #return self.__allMetadata.getValue(self.__keywords['radiance_add'])

  #@property
  #def quantize_max(self):
    #return self.__allMetadata.getValue(self.__keywords['quantize_max'])

  #@property
  #def quantize_min(self):
    #return self.__allMetadata.getValue(self.__keywords['quantize_min'])

  #@property
  #def correction_bias(self):
    #return self.__allMetadata.getValue(self.__keywords['correction_bias'])

  #@property
  #def correction_gain(self):
    #return self.__allMetadata.getValue(self.__keywords['correction_gain'])
    
  @property
  def dataset(self):
    if self.__dataset == None:
      self.__dataset = gdal.Open(self.path, GA_ReadOnly)
    return self.__dataset
    
  @property
  def projection(self):
    return self.dataset.GetProjectionRef()

  @property
  def transformation(self):
    return self.dataset.GetGeoTransform()

  @property
  def RasterXSize(self):
    return self.dataset.RasterXSize

  @property
  def RasterYSize(self):
    return self.dataset.RasterYSize

  @property
  def acquisitionDateTime(self):
    return '%s %s' % (self.__allMetadata.getValue('DATE_ACQUIRED'), self.__allMetadata.getValue('SCENE_CENTER_TIME') )
    
  @property
  def earthSunDistance(self):
    return ephem.Sun(self.acquisitionDateTime).earth_distance

  @property
  def solarElevation(self):
    return (float(self.__allMetadata.getValue('SUN_ELEVATION')) * numpy.pi) / 180.0
    
  @property
  def imageLS5(self):
    if self.__imageLS5 == None:
      self.__imageLS5 = ExtendedNumpyArray(
          input_array = self.dataset.ReadAsArray(),
          transformation = self.transformation,
          projection = self.projection
      )
    # release memory if less than 16GB available
    try:
      return self.__imageLS5
    finally:
      if self.systemInformation.freeMemory < 16 * 1024:
        self.__imageLS5 = None

  @property
  def imageLS7(self):
    if self.__imageLS7 == None:
      self.__imageLS7 = ExtendedNumpyArray(
	  input_array = (self.slope * self.imageLS5) + self.intercept,
	  transformation = self.transformation,
	  projection = self.projection
      )
    # release memory if less than 16GB available      
    try:
      return self.__imageLS7
    finally:
      if self.systemInformation.freeMemory < 16 * 1024:
        self.__imageLS7 = None

  @property
  def radiance(self):
    if self.__radiance == None:
      self.__radiance = ExtendedNumpyArray(
	  input_array = (self.gain * self.imageLS7) + self.bias,
	  transformation = self.transformation,
	  projection = self.projection
      )
    # release memory if less than 16GB available      
    try:
      return self.__radiance
    finally:
      if self.systemInformation.freeMemory < 16 * 1024:
        self.__radiance = None

  @property
  def reflectance(self):
    # release memory if less than 1,5GB available
    try:
      if self.__reflectance == None:
        self.__reflectance = ExtendedNumpyArray(
            input_array = (numpy.pi * self.radiance * self.earthSunDistance**2) / (self.Esun * numpy.sin(self.solarElevation)),
            transformation = self.transformation,
            projection = self.projection
        )
      return self.__reflectance
    finally:
      if self.systemInformation.freeMemory < 1.5 * 1024:
        self.__reflectance = None
    
  @property
  def noDataMask(self):
    return ExtendedNumpyArray(
	  ###### don't use self.image inside, cause self.image self.noDataMask is used inside self.image
	  input_array = self.dataset.ReadAsArray() > 0,
	  transformation = self.transformation,
	  projection = self.projection
      )

  
    
if __name__ == '__main__':

    #path = "/home/kaotika/Dokumente/BahirDar/LT51690522011273MLK00/LT51690522011273MLK00_MTL.txt"

    # Landsat 5
    path = "/media/sdb5/kaotika/Dokumente/BahirDar/LT51690522011273MLK00/LT51690522011273MLK00_MTL.txt"
    pathBand1 = "/media/sdb5/kaotika/Dokumente/BahirDar/LT51690522011273MLK00/LT51690522011273MLK00_B1.TIF"
    pathBand2 = "/media/sdb5/kaotika/Dokumente/BahirDar/LT51690522011273MLK00/LT51690522011273MLK00_B2.TIF"
    pathBand3 = "/media/sdb5/kaotika/Dokumente/BahirDar/LT51690522011273MLK00/LT51690522011273MLK00_B3.TIF"
    pathBand4 = "/media/sdb5/kaotika/Dokumente/BahirDar/LT51690522011273MLK00/LT51690522011273MLK00_B4.TIF"
    pathBand5 = "/media/sdb5/kaotika/Dokumente/BahirDar/LT51690522011273MLK00/LT51690522011273MLK00_B5.TIF"
    pathBand6 = "/media/sdb5/kaotika/Dokumente/BahirDar/LT51690522011273MLK00/LT51690522011273MLK00_B6.TIF"
    pathBand7 = "/media/sdb5/kaotika/Dokumente/BahirDar/LT51690522011273MLK00/LT51690522011273MLK00_B7.TIF"
    acquisitionDateTime = "2011-09-30 07:34:00.0800250Z"
    solarElevation = 60.73930445
    
    
    # Landsat 7
    #path = "/media/sdb5/kaotika/Dokumente/BahirDar/LE71730612003031SGS00/LE71730612003031SGS00_MTL.txt"
    #processor = landsat5Processor(path)
    #metadata = landsatMetadata(path)
    metadata = landsatMetadataFromPaths(landsatType = landsatType5, pathBand1 = pathBand1, pathBand2 = pathBand2,
      pathBand3 = pathBand3, pathBand4 = pathBand4, pathBand5 = pathBand5, pathBand6 = pathBand6, pathBand7 = pathBand7,
      acquisitionDateTime = acquisitionDateTime, solarElevation = solarElevation)
      
    print metadata.pathBand1
    print metadata.pathBand2
    print metadata.pathBand3
    print metadata.pathBand4
    print metadata.pathBand5
    print metadata.pathBand7
    print metadata.path
    metadata.path = path
    print metadata.metadata
    #processor = landsat5Processor(metadata)

    #print processor.savi
    #print processor.ndwi
    #print processor.ndsi

    #print processor.band1.path
    #print processor.band1.dataset.ReadAsArray()[10][1247]
    #print type(processor.band1.dataset.ReadAsArray())

    #print processor.band1.image[10][1247]
    #print processor.band1.imageLS7[10][1247]
    #print type(processor.band1.imageLS7)

    #print processor.RasterXSize, processor.RasterYSize
    #print processor.band1.earthSunDistance
    #print processor.band1.acquisitionDateTime
    #print processor.band1.solarElevation
    #processor.band1.radiance.save('/media/ramdisk/radiance.tif')
    #processor.band1.reflectance.save('/media/ramdisk/reflectance.tif')
    
    #processor.GetColorComposit321('/media/ramdisk/321.tif')
    #processor.GetColorComposit432('/media/ramdisk/432.tif')
    #processor.GetColorComposit453('/media/ramdisk/453.tif')
    #processor.GetColorComposit742('/media/ramdisk/742.tif')
    #processor.band1.noDataMask.save('/media/ramdisk/noDataMask.tif')
    
    #processor.ndvi.save('/media/ramdisk/ndvi.tif')
    #processor.ndsi.save('/media/ramdisk/ndsi.tif')
    #processor.savi.save('/media/ramdisk/savi.tif')
    #processor.ndwi.save('/media/ramdisk/ndwi.tif')

    #input_array = ((processor.band3.reflectance - processor.band5.reflectance) / (processor.band3.reflectance + processor.band5.reflectance))
    #print input_array
    #test = ExtendedNumpyArray(input_array = input_array, transformation = processor.band1.transformation, projection = processor.band1.projection)
    #test.save('/media/ramdisk/test.tif')

    #processor.band1.image.save('/media/ramdisk/image.tif')
    #processor.tasseledCapBrightness.save('/media/ramdisk/brightness.tif')
    #processor.tasseledCapGreenness.save('/media/ramdisk/greenness.tif')
    #processor.tasseledCapWetness.save('/media/ramdisk/wetness.tif')
    
    
    #processor.band1.reflectance.save('/media/ramdisk/band1.tif')
    #processor.band2.reflectance.save('/media/ramdisk/band2.tif')

    
    #print processor.band1.noDataMask[10][1246]
    #print type(processor.band1.noDataMask)

    #processor.calculateNDVI("/tmp/ndvi.tif")
    #processor.band1.saveReflectance("/tmp/reflectance.tif")
    #print processor.band2.path

    
    #print processor.metadata.hasKeyword('FILE_NAME_BAND_1')
    #print processor.metadata.getValue('FILE_NAME_BAND_1')

    #print landsatProcessor.keywords.has_key('THERMAL_LINES')

    #keyword = 'THERMAL_LINES'
    #category = landsatProcessor.keywords[keyword]
    #print landsatProcessor.metadata[category][keyword]

    #raw_input("Press Enter to continue...")