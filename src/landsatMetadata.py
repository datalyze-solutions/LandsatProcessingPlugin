import os
from landsatConst import *
from landsatExceptions import *

class landsatMetadata(object):

  def __init__(self, landsatType):
    if landsatType == landsat_type_5:
      self.metadata = landsat5MetadataDummy
      self.landsatType = landsatType
    elif landsatType == landsat_type_7:
      self.metadata = landsat7MetadataDummy
      self.landsatType = landsatType
    else:
      raise ExceptionValueNotInList(landsatType, landsat_types)

  @property
  def landsatType(self):
    return self.getValue(MD_spacecraft_id)

  @landsatType.setter
  def landsatType(self, landsatType):
    if landsatType in landsat_types:
      self.metadata[MD_product_metadata][MD_spacecraft_id] = landsatType
    else:
      raise ExceptionValueNotInList(landsatType, landsat_types)
    
  @property
  def keywords(self):
    keywords = {}
    for category in self.metadata.keys():
      for keyword in self.metadata[category].keys():
        keywords[keyword] = category
    return keywords

  def hasKeyword(self, keyword):
    return self.keywords.has_key(keyword)

  def getValue(self, keyword):
    if self.hasKeyword(keyword):
      category = self.keywords[keyword]
      return self.metadata[category][keyword]
    else:
      raise ExceptionKeywordNotFound(keyword)

      
class landsatMetadataFromMTL(landsatMetadata):

  def __init__(self, path):
    # TODO: is super needed???
    #super(landsatMetadataFromMTL, self).__init__(None)
    self.path = path

  @property
  def path(self):
    return self.__path

  @path.setter
  def path(self, path):
    if os.path.exists(path):
      self.__path = path
      self.metadata = self.__parseMetadata()
    else:
      raise ExceptionPathExistsNot(path)

  def __parseMetadata(self):
    # from http://metageta.googlecode.com/
    lines = iter(open(self.path).readlines())
    hdrdata = {}
    line = lines.next()
    while line:
        line = [item.strip() for item in line.replace('"','').split('=')]
        group = line[0].upper()
        if group in ['END;','END']:
          break
        value = line[1]
        if group in ['END_GROUP']:
          pass
        elif group in ['BEGIN_GROUP','GROUP']:
            group = value
            subdata = {}
            while line:
                line = lines.next()
                line = [l.replace('"','').strip() for l in line.split('=')]
                subgroup = line[0]
                subvalue = line[1]
                if subgroup == 'END_GROUP':
                    break
                elif line[1] == '(':
                    while line:
                        line = lines.next()
                        line = line.replace('"','').strip()
                        subvalue += line
                        if line[-1:] == ';':
                            subvalue = eval(subvalue.strip(';'))
                            break
                else:
                    subvalue = subvalue.strip(';')
                subdata[subgroup] = subvalue
            hdrdata[group] = subdata
        else: hdrdata[group] = value.strip(');')
        line = lines.next()
    return hdrdata

    
class landsatMetadataFromBandPaths(landsatMetadata):

  def __init__(self,
          landsatType,
          pathBand1,
          pathBand2,
          pathBand3,
          pathBand4,
          pathBand5,
          pathBand7,
          acquisitionDateTime,
          solarElevation
  ):
    super(landsatMetadataFromBandPaths, self).__init__(landsatType)

    self.pathBand1 = pathBand1
    self.pathBand2 = pathBand2
    self.pathBand3 = pathBand3
    self.pathBand4 = pathBand4
    self.pathBand5 = pathBand5
    self.pathBand7 = pathBand7

    self.solarElevation = solarElevation
    self.acquisitionDateTime = acquisitionDateTime

  @property
  def acquisitionDateTime(self):
    return '%s %s' % (self.getValue(MD_date_acquired), self.getValue(MD_scene_center_time))
  @acquisitionDateTime.setter
  def acquisitionDateTime(self, acquisitionDateTime):
    (date, time) = acquisitionDateTime.split(' ')
    self.metadata[MD_product_metadata][MD_date_acquired] = date
    self.metadata[MD_product_metadata][MD_scene_center_time] = time
      
  @property
  def solarElevation(self):
    return self.getValue(MD_sun_elevation)
  @solarElevation.setter
  def solarElevation(self, solarElevation): 
    if (solar_elevation_min <= solarElevation <= solar_elevation_max):
      self.metadata[MD_image_attributes][MD_sun_elevation] = solarElevation
    else:
      raise ExceptionValueNotBetween(solarElevation, solar_elevation_min, solar_elevation_max)

  @property
  def pathBand1(self):
    return self.getValue(MD_file_name_band_1)
  @pathBand1.setter
  def pathBand1(self, path):
    if os.path.exists(path):
      self.metadata[MD_product_metadata][MD_file_name_band_1] = path
    else:
      raise ExceptionPathExistsNot(path)

  @property
  def pathBand2(self):
    return self.getValue(MD_file_name_band_2)    
  @pathBand2.setter
  def pathBand2(self, path):
    if os.path.exists(path):
      self.metadata[MD_product_metadata][MD_file_name_band_2] = path
    else:
      raise ExceptionPathExistsNot(path)

  @property
  def pathBand3(self):
    return self.getValue(MD_file_name_band_3)    
  @pathBand3.setter
  def pathBand3(self, path):
    if os.path.exists(path):
      self.metadata[MD_product_metadata][MD_file_name_band_3] = path
    else:
      raise ExceptionPathExistsNot(path)

  @property
  def pathBand4(self):
    return self.getValue(MD_file_name_band_4)
  @pathBand4.setter
  def pathBand4(self, path):
    if os.path.exists(path):
      self.metadata[MD_product_metadata][MD_file_name_band_4] = path
    else:
      raise ExceptionPathExistsNot(path)

  @property
  def pathBand5(self):
    return self.getValue(MD_file_name_band_5)
  @pathBand5.setter
  def pathBand5(self, path):
    if os.path.exists(path):
      self.metadata[MD_product_metadata][MD_file_name_band_5] = path
    else:
      raise ExceptionPathExistsNot(path)

  @property
  def pathBand7(self):
    return self.getValue(MD_file_name_band_7)
  @pathBand7.setter
  def pathBand7(self, path):
    if os.path.exists(path):
      self.metadata[MD_product_metadata][MD_file_name_band_7] = path
    else:
      raise ExceptionPathExistsNot(path)

      
class landsat5MetadataFromBandPaths(landsatMetadataFromBandPaths):

  def __init__(self,
          landsatType,
          pathBand1,
          pathBand2,
          pathBand3,
          pathBand4,
          pathBand5,
          pathBand6,
          pathBand7,
          acquisitionDateTime,
          solarElevation
  ):
    if landsatType != landsat_type_5:
      raise ExceptionNoLandsat5Image()
    super(landsat5MetadataFromBandPaths, self).__init__(
        landsatType = landsatType,
        pathBand1 = pathBand1,
        pathBand2 = pathBand2,
        pathBand3 = pathBand3,
        pathBand4 = pathBand4,
        pathBand5 = pathBand5,
        pathBand7 = pathBand7,
        solarElevation = solarElevation,
        acquisitionDateTime = acquisitionDateTime
    )
    self.pathBand6 = pathBand6

  @property
  def pathBand6(self):
    return self.getValue(MD_file_name_band_6)
  @pathBand6.setter
  def pathBand6(self, path):
    if os.path.exists(path):
      self.metadata[MD_product_metadata][MD_file_name_band_6] = path
    else:
      raise ExceptionPathExistsNot(path)


class landsat7MetadataFromBandPaths(landsatMetadataFromBandPaths):

  def __init__(self,
          landsatType,
          pathBand1,
          pathBand2,
          pathBand3,
          pathBand4,
          pathBand5,
          pathBand6v1,
          pathBand6v2,
          pathBand7,
          pathBand8,
          acquisitionDateTime,
          solarElevation
  ):
    if landsatType != landsat_type_7:
      raise ExceptionNoLandsat7Image()
    super(landsat7MetadataFromBandPaths, self).__init__(
        landsatType = landsatType,
        pathBand1 = pathBand1,
        pathBand2 = pathBand2,
        pathBand3 = pathBand3,
        pathBand4 = pathBand4,
        pathBand5 = pathBand5,
        pathBand7 = pathBand7,
        solarElevation = solarElevation,
        acquisitionDateTime = acquisitionDateTime
    )
    self.pathBand6v1 = pathBand6v1
    self.pathBand6v2 = pathBand6v2
    self.pathBand8 = pathBand8

  @property
  def pathBand6v1(self):
    return self.getValue(MD_file_name_band_6v1)
  @pathBand6v1.setter
  def pathBand6v1(self, path):
    if os.path.exists(path):
      self.metadata[MD_product_metadata][MD_file_name_band_6v1] = path
    else:
      raise ExceptionPathExistsNot(path)

  @property
  def pathBand6v2(self):
    return self.getValue(MD_file_name_band_6v2)
  @pathBand6v2.setter
  def pathBand6v2(self, path):
    if os.path.exists(path):
      self.metadata[MD_product_metadata][MD_file_name_band_6v2] = path
    else:
      raise ExceptionPathExistsNot(path)

  @property
  def pathBand8(self):
    return self.getValue(MD_file_name_band_8)
  @pathBand8.setter
  def pathBand8(self, path):
    if os.path.exists(path):
      self.metadata[MD_product_metadata][MD_file_name_band_8] = path
    else:
      raise ExceptionPathExistsNot(path)    