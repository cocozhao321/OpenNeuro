from OpenNeuroProto import OpenNeuroOverview
from OpenNeuroProto import OpenNeuroDataset

"""
Answers are based on the s3 database on 11/02/2020
It will very likely change since more dataset will be added to the database 
"""
overview = OpenNeuroOverview()
download = OpenNeuroDataset('ds003030') # an exist dataset
download_f = OpenNeuroDataset('d003030')  # a non-exist dataset


def test_overview_get_dataset_list():
    assert overview.get_dataset_list()[0] == 'ds000001/'  # check the first dataset
    assert overview.get_dataset_list()[-1] == 'ds003346/'  # check the last dataset
    assert len(overview.get_dataset_list()) == 451  # check the length of dataset


def test_overview_get_dataset():
    assert overview.get_dataset('ds003030')
    assert not overview.get_dataset('d003030')
    assert not overview.get_dataset('ds03030')


def test_overview_get_subject_list():
    assert overview.get_subject_list("ds003030")[1] == 'ds003030/sub-01/'
    assert overview.get_subject_list("ds003030")[-1] == 'ds003030/sub-23/'
    assert len(overview.get_subject_list("ds003030")) == 24
    assert not overview.get_subject_list("d003030")


def test_overview_display_description():
    assert overview.display_description("ds003030").iloc[0][0] == 'Flickering Checkerboard Demo Scans'
    assert not overview.get_subject_list("d003030")


def test_overview_display_readme():
    assert not overview.display_readme("ds003030")
    assert not overview.display_readme("d003030")
    assert overview.display_readme("ds003340")[:15] == 'Dataset descrip'


def test_download_check_subject():
    assert download.check_subject()
    assert download.check_subject("01")
    assert not download_f.check_subject()
    assert not download.check_subject("0555")


def test_download_all():
    assert download.download_all()
    assert not download_f.download_all()


def test_download_subject():
    assert download.download_subject(True)
    assert download.download_subject(False, "02")
    assert download.download_subject(True, "03")
    assert not download.download_subject(True, subject_id="55")
    assert not download_f.download_subject(True)
