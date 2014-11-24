# -*- coding: utf-8 -*-
# Copyright (c) 2011 Australian Government, Department of Sustainability, Environment, Water, Population and Communities
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

'''
Metadata driver for JPEG2000 imagery
'''

format_regex=[r'\.jp2$'] #Well duh...
'''Regular expression list of file formats'''

#import base dataset modules
#import __dataset__
import __default__

# import other modules (use "_"  prefix to import privately)
import sys, os

class Dataset(__default__.Dataset): 
    '''Subclass of __default__.Dataset class so we get a load of metadata populated automatically'''
    def __getmetadata__(self,f=None):
        '''Read Metadata for a JP2 image'''
        gdal=__default__.gdal
        jp2mrsid=gdal.GetDriverByName('JP2MrSID')
        if jp2mrsid:jp2mrsid.Deregister()
        if not f:f=self.fileinfo['filepath']
        ers=os.path.splitext(f)[0]+'.ers'
        if os.path.exists(ers):
            try:
                __default__.Dataset.__getmetadata__(self, ers) #autopopulate basic metadata
                self.metadata['filetype']='JP2ECW/ERMapper JPEG2000'
                self.metadata['compressiontype']='JPEG2000'
            except:__default__.Dataset.__getmetadata__(self, f)
        else:
            __default__.Dataset.__getmetadata__(self, f) #autopopulate basic metadata
        if jp2mrsid:jp2mrsid.Register()

    def getoverview(self,*args,**kwargs):
        '''Check for possibly corrupt files that can crash GDAL and therefore python...'''
        if self.metadata['compressionratio'] > 10000:
            raise IOError, 'Unable to generate overview image from %s\nFile may be corrupt' % self.fileinfo['filepath']
        else:return __default__.Dataset.getoverview(self,*args,**kwargs)
