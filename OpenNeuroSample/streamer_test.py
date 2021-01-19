"""
Implements a sample streaming class for a BIDS archive

NOTE: This is prototype code for testing purposes, and not intended to serve as
production code. It has been neither rigorously tested nor particularly
carefully designed.
"""

from rtCommon.bidsArchive import BidsArchive
from rtCommon.bidsIncremental import BidsIncremental
import time
from projects.OpenNeuroSample.OpenNeuroProto import OpenNeuroOverview
from projects.OpenNeuroSample.initialize import OutputUpdate
import nibabel as nib
# For the streamer, we might return an instance of something like this class
# (with specified characteristics, like subject and session) whenever an
# iteration is requested. That way, the streamer doesn't have to maintain
# internal state about the status of various iterators, it's fully encapsulated
# in this class.
#
# As an example of a case where maintaining the internal state of the iterator
# in the streamer becomes difficult, a user may first request streaming subject
# 1 session 1, then break halfway through the iteration after getting the first
# half of the session, and then switch to subject 2 session 1, and break after
# getting the first half of that session, and then compare the two.
#
# In such a case, we wouldn't want the streamer having to figure out when it's
# supposed to reset the internal state of the various iterators; rather, it
# should return two, distinct and independent iterators for use by the client
# for those two distinct requests.
#
# This also avoids the weird logic currently present around setting
# _stream_empty when the iterator runs out the first time, and returning None.
# In the 'return an iterator' implementation, this won't be a concern.
class bidsStreamer():

    def __init__(self, dataset, datasetType):
        self.dataset = dataset
        self._index = -1
        self.type = datasetType

    def __iter__(self):
        return self

    def __next__(self):
        self._index += 1
        if self.type == 'archive':
            # Subject: 001
            # Session: 01
            # Task: Faces
            # Run: 01
            # Suffix: Bold
            NUM_TIMEPOINTS = 196  # 4th dimension of NIfTI image -- manually extracted
            if self._index >= NUM_TIMEPOINTS:
                raise StopIteration
            else:
                return self.dataset.getIncremental(
                    subject='04',
                    session='01',
                    task='flanker',
                    suffix='bold',
                    dataType='func',
                    sliceIndex=self._index,
                    otherLabels={'run': 1})
        elif self.type == 'openNeuro':
            NUM_TIMEPOINTS = self.dataset.dataset_Bidsinc(sliceIndex=self._index)[1]
            if self._index >= NUM_TIMEPOINTS:
                raise StopIteration
            else:
                return self.dataset.dataset_Bidsinc(sliceIndex=self._index)[0]
    # This will need some work if it's to be exposed externally, as the
    # StopIteration exception won't automatically trigger halt iteration, like
    # when this is used in the 'for image in archiveIterator:' usage.
    #get_next_image = __next__


def main():
    #OpenNeuro Example
    overview = OpenNeuroOverview()  # initialize OpenNeuroOverview
    print(overview.display_description("ds000102"))  # check description before download
    print(overview.display_readme("ds000102"))  # check readme file (if exists) before download
    # download a subject's data only and reformat it as BIDS-I
    download_dataset = overview.get_dataset("ds000102", False, "04")  # get dataset based on accession number and id
    openneuroDataset = OutputUpdate(download_dataset)
    openneuroDataset.webCommunication() #  communicate with web-platform and update conf file
    openStream = bidsStreamer(openneuroDataset,'openNeuro')
    for incremental in openStream:
        print(incremental)
        time.sleep(.1)

        
    # bidsArchive example
    """
    path = '/Users/cocozhao/Desktop/rt-cloud-bidsinc-dev/projects/OpenNeuroSample'
    archiveDataset = BidsArchive(path)
    archivestream = bidsStreamer(archiveDataset,'archive')
    
    for incremental in archivestream:
        print(incremental)
        time.sleep(.2)
    """
if __name__ == "__main__":
    main()