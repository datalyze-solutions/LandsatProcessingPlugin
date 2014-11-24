# -*- coding: utf-8 -*-

from osgeo import gdal
from osgeo.gdalconst import *
import os
import numpy

# PyEphem
import ephem

# from http://metageta.googlecode.com/
def parseheader(f):
    lines=iter(open(f).readlines())
    hdrdata={}
    line=lines.next()
    while line:
        line=[item.strip() for item in line.replace('"','').split('=')]
        group=line[0].upper()
        if group in ['END;','END']:break
        value=line[1]
        if group in ['END_GROUP']:pass
        elif group in ['BEGIN_GROUP','GROUP']:
            group=value
            subdata={}
            while line:
                line=lines.next()
                line = [l.replace('"','').strip() for l in line.split('=')]
                subgroup=line[0]
                subvalue=line[1]
                if subgroup == 'END_GROUP':
                    break
                elif line[1] == '(':
                    while line:
                        line=lines.next()
                        line = line.replace('"','').strip()
                        subvalue+=line
                        if line[-1:]==';':
                            subvalue=eval(subvalue.strip(';'))
                            break
                else:subvalue=subvalue.strip(';')
                subdata[subgroup]=subvalue
            hdrdata[group]=subdata
        else: hdrdata[group]=value.strip(');')
        line=lines.next()
    return hdrdata  
      
  
gdal.AllRegister()
tiffDriver = gdal.GetDriverByName('GTiff')
tiffDriver.Register()
#type = GDT_Byte
type = GDT_Float32
inNoData = None
outNoData = None

# http://www.yale.edu/ceo/Documentation/Landsat_DN_to_Kelvin.pdf
LS5toLS7values = {}
LS5toLS7values[1] = {'slope': 0.943, 'intercept': 4.21, 'gain': 0.778740, 'bias': -6.98, 'Esun': 1997}
LS5toLS7values[2] = {'slope': 1.776, 'intercept': 2.58, 'gain': 0.798819, 'bias': -7.20, 'Esun': 1812}
LS5toLS7values[3] = {'slope': 1.538, 'intercept': 2.50, 'gain': 0.621654, 'bias': -5.62, 'Esun': 1533}
LS5toLS7values[4] = {'slope': 1.427, 'intercept': 4.80, 'gain': 0.639764, 'bias': -5.74, 'Esun': 1039}
LS5toLS7values[5] = {'slope': 0.984, 'intercept': 6.96, 'gain': 0.126220, 'bias': -1.13, 'Esun': 230.8}
LS5toLS7values[6] = {'slope': 1, 'intercept': 0, 'gain': 0.05518, 'bias': 1.2378}
LS5toLS7values[7] = {'slope': 1.304, 'intercept': 5.76, 'gain': 0.043898, 'bias': -0.39, 'Esun': 84.9}
K1 = 607.76
K2 = 1260.56
emissivity = 0.95


#landsatDir = "/home/kaotika/Dokumente/BahirDar/LT51700522011264MLK00"
#landsatDir = "/home/kaotika/Dokumente/BahirDar/LT51690522011273MLK00"
landsatDir = "/home/kaotika/Dokumente/BahirDar/LT51700512011264MLK00"
outputDir = os.path.join(landsatDir, 'output')
#metadataFilename = "LT51700522011264MLK00_MTL.txt"
#metadataFilename = "LT51690522011273MLK00_MTL.txt"
metadataFilename = "LT51700512011264MLK00_MTL.txt"

metadataFilepath = os.path.join(landsatDir, metadataFilename)
print metadataFilepath
if not os.path.exists(metadataFilepath): 
  print "no Metadatafile"
  
metadata = parseheader(metadataFilepath)
#print metadata.keys()
#print metadata['IMAGE_ATTRIBUTES']['SUN_AZIMUTH']


for i in range(1,8):
#for i in [6]:
  print metadata['PRODUCT_METADATA']['FILE_NAME_BAND_%i' % i]
  
  solarElevation = metadata['IMAGE_ATTRIBUTES']['SUN_ELEVATION']
  solarElevation = (float(solarElevation)* numpy.pi) / 180
  print 'solarElevation', solarElevation
  acquisitionDate = metadata['PRODUCT_METADATA']['DATE_ACQUIRED']
  earthSunDistance = ephem.Sun(acquisitionDate).earth_distance
  
  currentFile = metadata['PRODUCT_METADATA']['FILE_NAME_BAND_%i' % i]
  inputfile = os.path.join(landsatDir, currentFile)
  outputfile = os.path.join(outputDir, currentFile)
  
  try:
    os.mkdir(outputDir)
  except:
    print 'directory exists'

  indataset = gdal.Open(inputfile, GA_ReadOnly )
  if i == 6:
    type = GDT_Float32  
  outdataset = tiffDriver.Create(outputfile, indataset.RasterXSize, indataset.RasterYSize, indataset.RasterCount, type)

  gt = indataset.GetGeoTransform()
  if gt is not None and gt != (0.0, 1.0, 0.0, 0.0, 0.0, 1.0):
    outdataset.SetGeoTransform(gt)

  prj = indataset.GetProjectionRef()
  if prj is not None and len(prj) > 0:
    outdataset.SetProjection(prj)

  inband = indataset.GetRasterBand(1).ReadAsArray()
  outband = outdataset.GetRasterBand(1)
  
  # get NoData Cells
  noDataIndizes = inband <= 0
  
  # LS5 to LS7
  inband = (LS5toLS7values[i]['slope'] * inband) + LS5toLS7values[i]['intercept']
  # LS7 to reflectance
  inband = (LS5toLS7values[i]['gain'] * inband) + LS5toLS7values[i]['bias']
  
  if not i == 6:
    # radiance to reflectance
    inband = ( numpy.pi * inband * earthSunDistance ** 2 ) / ( LS5toLS7values[i]['Esun'] * numpy.sin(solarElevation) )
    subZeroValues = inband < 0
    inband[subZeroValues] = 0
  
  if i == 6:
    # reflectance to temperature in Kelvin
    inband = K2 / ( numpy.log((K1*emissivity / inband) + 1) )

  # set NoData
  inband[noDataIndizes] = 0
  
  #print inband
  outband.WriteArray(inband)
  inband = None
  indataset = None
  outdataset = None
 

# prepare for indize calculation
#currentFile = metadata['PRODUCT_METADATA']['FILE_NAME_BAND_%i' % 3]
#inputfile = os.path.join(outputDir, currentFile)
#VIS = gdal.Open(inputfile, GA_ReadOnly )
#currentFile = metadata['PRODUCT_METADATA']['FILE_NAME_BAND_%i' % 4]
#inputfile = os.path.join(outputDir, currentFile)
#NIR = gdal.Open(inputfile, GA_ReadOnly )
#currentFile = metadata['PRODUCT_METADATA']['FILE_NAME_BAND_%i' % 7]
#print "SWIR path", currentFile
#inputfile = os.path.join(outputDir, currentFile)
#SWIR = gdal.Open(inputfile, GA_ReadOnly )

#VIS_Band = VIS.GetRasterBand(1).ReadAsArray()
#NIR_Band = NIR.GetRasterBand(1).ReadAsArray()
#SWIR_Band = SWIR.GetRasterBand(1).ReadAsArray()

#print VIS_Band
#print NIR_Band
#print SWIR_Band

#VIS_Band = 1.0 * VIS_Band
#NIR_Band = 1.0 * NIR_Band
#SWIR_Band = 1.0 * SWIR_Band

#gt = VIS.GetGeoTransform()
#prj = VIS.GetProjectionRef()

# NDVI
#print 'Calculate NDVI'

#outputfile = os.path.join(outputDir, 'NDVI')
#type = GDT_Float32
#outdataset = tiffDriver.Create(outputfile, VIS.RasterXSize, VIS.RasterYSize, VIS.RasterCount, type)

#if gt is not None and gt != (0.0, 1.0, 0.0, 0.0, 0.0, 1.0):
  #outdataset.SetGeoTransform(gt)
#if prj is not None and len(prj) > 0:
  #outdataset.SetProjection(prj)

#outband = outdataset.GetRasterBand(1)
#ndvi = (NIR_Band - VIS_Band) / (NIR_Band + VIS_Band)
#outband.WriteArray(ndvi)
#ndvi = None
  
  
## SAVI
#print 'Calculate SAVI'

#outputfile = os.path.join(outputDir, 'SAVI')
#type = GDT_Float32
#outdataset = tiffDriver.Create(outputfile, VIS.RasterXSize, VIS.RasterYSize, VIS.RasterCount, type)

#if gt is not None and gt != (0.0, 1.0, 0.0, 0.0, 0.0, 1.0):
  #outdataset.SetGeoTransform(gt)
#if prj is not None and len(prj) > 0:
  #outdataset.SetProjection(prj)

#outband = outdataset.GetRasterBand(1)
#savi = (1 + 0.5) * (NIR_Band - VIS_Band) / (NIR_Band + VIS_Band + 0.5)
#outband.WriteArray(savi)
#savi = None


# NDWI
#print 'Calculate NDWI'

#outputfile = os.path.join(outputDir, 'NDWI')
#type = GDT_Float32
#outdataset = tiffDriver.Create(outputfile, VIS.RasterXSize, VIS.RasterYSize, VIS.RasterCount, type)

#if gt is not None and gt != (0.0, 1.0, 0.0, 0.0, 0.0, 1.0):
  #outdataset.SetGeoTransform(gt)
#if prj is not None and len(prj) > 0:
  #outdataset.SetProjection(prj)

#outband = outdataset.GetRasterBand(1)
#ndwi = (VIS_Band - SWIR_Band) / (VIS_Band + SWIR_Band)
##ndwi = SWIR_Band
#outband.WriteArray(ndwi)
#ndwi = None


## NDSI
#print 'Calculate NDSI'

#outputfile = os.path.join(outputDir, 'NDSI')
#type = GDT_Float32
#outdataset = tiffDriver.Create(outputfile, VIS.RasterXSize, VIS.RasterYSize, VIS.RasterCount, type)

#if gt is not None and gt != (0.0, 1.0, 0.0, 0.0, 0.0, 1.0):
  #outdataset.SetGeoTransform(gt)
#if prj is not None and len(prj) > 0:
  #outdataset.SetProjection(prj)

#outband = outdataset.GetRasterBand(1)
#ndsi = (SWIR_Band - NIR_Band) / (SWIR_Band + NIR_Band)
#outband.WriteArray(ndsi)
#ndsi = None