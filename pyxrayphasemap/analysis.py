#!/usr/bin/env python
"""
.. py:currentmodule:: pyMcGill.experimental.phaseMap.PhaseAnalysis
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Create phase map from x-ray map data.
"""

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2014 Hendrix Demers"
__license__ = ""

# Standard library modules.
import os.path
import logging

# Third party modules.
import h5py
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# Local modules.

# Project modules

# Globals and constants variables.
DATA_TYPE_ATOMIC_NORMALIZED = "atom norm"
DATA_TYPE_WEIGHT_NORMALIZED = "weight norm"

class PhaseAnalysis(object):
    def __init__(self):
        self.elements = []
        self.sampleName = None
        self.dataType = None
        self.overwrite = False
        self.dataExtension = None
        self.width = None
        self.height = None

    def readElementData(self, dataPath):
        self._elementData, self.width, self.height = self._readProjectFile(self.elements, self.sampleName, self.dataType, dataPath)

    def _readProjectFile(self, elements, sampleName, dataType, dataPath):
        filename = "PhaseAnalysis_sample%s.hdf5" % (sampleName)
        filepath = os.path.join(dataPath, filename)

        if self.overwrite:
            h5file = h5py.File(filepath, 'w')
        else:
            h5file = h5py.File(filepath, 'a')

        if dataType not in h5file:
            groupName = "/%s" % (dataType)
            dataTypeGroup = h5file.create_group(groupName)
        else:
            dataTypeGroup = h5file[dataType]

        logging.debug(dataTypeGroup.name)
        logging.debug(dataTypeGroup.parent)

        elementData = {}

        for element in elements:
            if element not in dataTypeGroup:
                filename= r'%s-%s_%s.%s' % (sampleName, dataType, element, self.dataExtension)
                filepath = os.path.join(dataPath, filename)

                if not os.path.isfile(filepath) and dataType == DATA_TYPE_WEIGHT_NORMALIZED:
                    filename= r'%s_%s_%s.%s' % (sampleName, "mass_norm", element, self.dataExtension)
                    filepath = os.path.join(dataPath, filename)

                if not os.path.isfile(filepath) and dataType == DATA_TYPE_WEIGHT_NORMALIZED:
                    filename= r'%s-%s_%s.%s' % (sampleName, "w% norm", element, self.dataExtension)
                    filepath = os.path.join(dataPath, filename)

                if not os.path.isfile(filepath) and dataType == DATA_TYPE_WEIGHT_NORMALIZED:
                    filename= r'%s-%s_%s.%s' % (sampleName, "w%-norm", element, self.dataExtension)
                    filepath = os.path.join(dataPath, filename)

                try:
                    elementData[element] = self._readData(filepath)
                    w, h = elementData[element].shape
                    dset = dataTypeGroup.create_dataset(element, elementData[element].shape, dtype=np.float32)
                    dset[:,:] = elementData[element]
                    logging.debug(dset)
                    h5file.flush()
                except IOError:
                    logging.warning("Filepath does not exist %s", filepath)
            else:
                dset = dataTypeGroup[element]
                elementData[element] = np.array(dset)
                w, h = elementData[element].shape

        h5file.close()

        return elementData, w, h

    def _readData(self, filepath):
        _basename, extension = os.path.splitext(filepath)
        if extension == ".tif":
            return self._readDataFromImageFile(filepath)
        elif extension == ".txt":
            return self._readDataFromTextFile(filepath)

        logging.error("Unkown extension %s for filepath %s", extension, filepath)

    def _readDataFromTextFile(self, filepath):
        data = np.loadtxt(open(filepath,"rb"),delimiter=";")
        return data

    def _readDataFromImageFile(self, Filename):
        Im = Image.open(Filename)
        arr = np.array(Im)
        return arr

    def saveElementImages(self, graphicPath, basename):

        for symbol in self.elementData:
            data = self.elementData[symbol]
            plt.figure()
            title = "%s %s" % (basename, symbol)
            plt.title(title)

            plt.imshow(data, aspect='equal')
            plt.axis('off')
            plt.colorbar()

            filename = "%s_%s.png" % (basename, symbol)
            filepath = os.path.join(graphicPath, filename)
            plt.savefig(filepath)
            plt.close()

    @property
    def elements(self):
        return self._elements
    @elements.setter
    def elements(self, elements):
        self._elements = elements

    @property
    def sampleName(self):
        return self._sampleName
    @sampleName.setter
    def sampleName(self, sampleName):
        self._sampleName = sampleName

    @property
    def dataType(self):
        return self._dataType
    @dataType.setter
    def dataType(self, dataType):
        self._dataType = dataType

    @property
    def overwrite(self):
        return self._overwrite
    @overwrite.setter
    def overwrite(self, overwrite):
        self._overwrite = overwrite

    @property
    def dataExtension(self):
        return self._dataExtension
    @dataExtension.setter
    def dataExtension(self, dataExtension):
        self._dataExtension = dataExtension

    @property
    def width(self):
        return self._width
    @width.setter
    def width(self, width):
        self._width = width

    @property
    def height(self):
        return self._height
    @height.setter
    def height(self, height):
        self._height = height

    @property
    def elementData(self):
        return self._elementData

if __name__ == '__main__': #pragma: no cover
    import pyHendrixDemersTools.Runner as Runner
    Runner.Runner().run(runFunction=None)
