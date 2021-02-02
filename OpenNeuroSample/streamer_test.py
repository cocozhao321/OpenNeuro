"""
Implements a sample streaming class for a BIDS archive

NOTE: This is prototype code for testing purposes, and not intended to serve as
production code. It has been neither rigorously tested nor particularly
carefully designed.
"""

from rtCommon.bidsArchive import BidsArchive
import time
from projects.OpenNeuroSample.OpenNeuroProto import OpenNeuroOverview
from projects.OpenNeuroSample.initialize import OpenNeuroUpdate
from rtCommon.dicomToBidsService import dicomToBidsinc, dicomDirToBidsinc

class bidsStreamer():

    def __init__(self, dataset, datasetType, sliceIndex:int = -1):
        self.dataset = dataset
        self.index = sliceIndex
        self.type = datasetType

    def get_next_image(self, index:int = 0):
        if index != 0:
            self.index = index - 1
        self.index += 1
        if self.type == 'archive':
            # Subject: 001
            # Session: 01
            # Task: Faces
            # Run: 01
            # Suffix: Bold
            NUM_TIMEPOINTS = 196  # 4th dimension of NIfTI image -- manually extracted
            if self.index >= NUM_TIMEPOINTS:
                raise StopIteration
            else:
                return self.dataset.getIncremental(
                    subject='04',
                    session='01',
                    task='task-flanker',
                    suffix='bold',
                    datatype='func',
                    sliceIndex=self.index,
                    otherLabels={'run': 1})
        elif self.type == 'openNeuro':
            NUM_TIMEPOINTS = self.dataset.dataset_Bidsinc(sliceIndex=self.index)[1]
            if self.index >= NUM_TIMEPOINTS:
                raise StopIteration
            else:
                return self.dataset.dataset_Bidsinc(sliceIndex=self.index)[0]
        elif self.type == 'dicom':
            return self.dataset
        elif self.type == 'dicomDir':
            return self.dataset[self.index]

def dicomMetadataSample() -> dict:
    sample = {}
    sample["ContentDate"] = "20190219"
    sample["ContentTime"] = "124758.653000"
    sample["RepetitionTime"] = 1500
    sample["StudyDescription"] = "Norman_Mennen^5516_greenEyes"
    sample["StudyInstanceUID"] = \
        "1.3.12.2.1107.5.2.19.45031.30000019021215313940500000046"
    sample["ProtocolName"] = "func_ses-01_task-faces_run-01"
    return sample

def main(args):
    #args = sys.argv[1:]
    if args == "openneuro":
        #OpenNeuro Example
        overview = OpenNeuroOverview()  # initialize OpenNeuroOverview
        print(overview.display_description("ds000102"))  # check description before download
        print(overview.display_readme("ds000102"))  # check readme file (if exists) before download
        # download a subject's data only and reformat it as BIDS-I
        download_dataset = overview.get_dataset("ds000102", False, "04")  # get dataset based on accession number and id
        openneuroDataset = OpenNeuroUpdate(download_dataset)
        openneuroDataset.webCommunication() #  communicate with web-platform and update conf file
        openStream = bidsStreamer(openneuroDataset,'openNeuro')
        #print(openStream.get_next_image(110))
        for i in range(10):
            print(openStream.get_next_image())
            time.sleep(.1)
    # bidsArchive example
    elif args == "bidsArchive":
        path = '/Users/cocozhao/Desktop/rt-cloud-bidsinc-dev/projects/OpenNeuroSample/ds000102'
        archiveDataset = BidsArchive(path)
        archivestream = bidsStreamer(archiveDataset,'archive')
        #print(archivestream.get_next_image(1))
        for i in range(196):
            print(archivestream.get_next_image(i))
            time.sleep(.1)
    elif args == "dicomDir":
        dicomDir = "/Users/cocozhao/Desktop/rt-cloud-bidsinc-dev/projects/sample/dicomDir/20190219.0219191_faceMatching.0219191_faceMatching"
        requiredMetadata = {'subject': '01', 'task': 'faces', 'suffix': 'bold',  # REQUIRED
            'session': '01', 'run': 1}
        TR = 10
        dicomDirDataset = dicomDirToBidsinc(dicomDir,TR, requiredMetadata)
        dicomDirStream = bidsStreamer(dicomDirDataset,'dicomDir')
        for i in range(TR):
            print(dicomDirStream.get_next_image())
    elif args == "dicom":
        requiredMetadata = {'subject': '01', 'task': 'faces', 'suffix': 'bold',  # REQUIRED
                            'session': '01', 'run': 1}
        dicomFile = "/Users/cocozhao/Desktop/rt-cloud-bidsinc-dev/projects/sample/dicomDir/" \
                    "20190219.0219191_faceMatching.0219191_faceMatching/001_000013_000005.dcm"
        dicomDataset = dicomToBidsinc(dicomFile,requiredMetadata)
        dicomStream = bidsStreamer(dicomDataset,'dicom')
        print(dicomStream.get_next_image())

if __name__ == "__main__":
    main('dicomDir')