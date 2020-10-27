from OpenNeuroProto import OpenNeuroOverview
from OpenNeuroProto import OpenNeuroDownload
#import pytest

"""
Answers are based on the s3 database on 10/26/2020
It will very likely change since more dataset will be added to the database 
"""
overview = OpenNeuroOverview()
download = OpenNeuroDownload('ds003030') # an exist dataset
download_f = OpenNeuroDownload('d003030')  # a non-exist dataset


def test_overview_read_dataset():
    assert overview.read_dataset()[0] == 'ds000001/'  # check the first dataset
    assert overview.read_dataset()[-1] == 'ds003342/'  # check the last dataset
    assert len(overview.read_dataset()) == 448  # check the length of dataset


def test_overview_check_dataset():
    assert overview.check_dataset('ds003030')
    assert not overview.check_dataset('d003030')
    assert not overview.check_dataset('ds03030')


def test_overview_read_subject():
    assert overview.read_subject("ds003030")[1] == 'ds003030/sub-01/'
    assert overview.read_subject("ds003030")[-1] == 'ds003030/sub-23/'
    assert len(overview.read_subject("ds003030")) == 24
    assert not overview.read_subject("d003030")


def test_overview_check_subject():
    assert overview.check_subject("ds003030")
    assert overview.check_subject("ds003030", "01")
    assert not overview.check_subject("ds03030")
    assert not overview.check_subject("ds003030", "0555")


def test_download_all():
    assert download.download_all()
    assert not download_f.download_all()


def test_download_subject():
    assert download.download_subject(True)
    assert download.download_subject(False, "02")
    assert download.download_subject(True, "03")
    assert not download.download_subject(True, subject_id="55")
    assert not download_f.download_subject(True)
"""
    print("===Test read dataset===")
    print(test_true.read_dataset())
    
    print("===Test check the existence of dataset")
    print("ds003030: ", test_true.check_dataset())
    print("d003030: ", test_false.check_dataset())
    
    print("===Test read dataset information in the specified dataset===")
    print(test_true.read_dataset_info())
    
    print('===Test download the whole dataset===')
    print(test_true.download_all())
    print(test_false.download_all())
    
    print("===Test check the eixstence of subject folder")
    print("check whether subject 02 exists:", test_true.check_subject_existence("02"))
    print("check whether subject 55 exists:", test_true.check_subject_existence("55"))
    
    print("===Test download specific subject folder")
    test_true.download_subject(True)`
"""