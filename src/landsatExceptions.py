###### Exceptions
class ExceptionOperationNotAvailable(Exception):
  def __init__(self, band):
    self.band = band

  def __str__(self):
    return "Operation not available for band " % (self.band)

class ExceptionNoLandsatImage(Exception):
  def __str__(self):
    return "not a landsat image or wrong metadata"

class ExceptionNoLandsat5Image(Exception):
  def __str__(self):
    return "not a landsat 5 image"

class ExceptionNoLandsat7Image(Exception):
  def __str__(self):
    return "not a landsat 7 image"
    
class ExceptionWrongClass(Exception):
  def __init__(self, isClass, targetClass):
    self.isClass = isClass
    self.targetClass = targetClass

  def __str__(self):
    return "class '%s' is not '%s'" % (self.isClass, self.targetClass)

class ExceptionPathExistsNot(Exception):
  def __init__(self, path):
    self.path = path

  def __str__(self):
    return "file: %s doesn't exists" % (self.path)

class Exception2DarrayNeeded(Exception):
  def __init__(self, shape):
    self.shape = shape

  def __str__(self):
    return "2D array needed. Dimensions are: %s" % (self.shape)

class ExceptionPathExists(Exception):
  def __init__(self, path):
    self.path = path

  def __str__(self):
    return "file: %s still exists. Don't overwrite.'" % (self.path)

class ExceptionValueNotBetween(Exception):
  def __init__(self, value, minValue, maxValue):
    self.minValue = minValue
    self.maxValue = maxValue
    self.value = value

  def __str__(self):
    return "value '%s' is not between %s and %s" % (self.value, self.minValue, self.maxValue)

class ExceptionValueNotInList(Exception):
  def __init__(self, value, valueList):
    self.valueList = valueList
    self.value = value

  def __str__(self):
    return "value '%s' is not in %s" % (self.value, self.valueList)

class ExceptionKeywordNotFound(Exception):
  def __init__(self, keyword):
    self.keyword = keyword

  def __str__(self):
    return "keyword '%s' not available" % (self.keyword)
