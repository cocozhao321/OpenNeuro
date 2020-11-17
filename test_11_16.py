from OpenNeuroProto import OpenNeuroOverview
from OpenNeuroProto import DownloadOpenNeuroDataset

"""
Answers are based on the s3 database on 11/16/2020
It will very likely change since more dataset will be added to the database.
Test cases are used to test new added methods since 11/02/2020.
'ds003030_test' is in the root dir
"""
overview = OpenNeuroOverview()
download = DownloadOpenNeuroDataset('ds003030_test') # an exist dataset
download_f = DownloadOpenNeuroDataset('d003030')  # a non-exist dataset


def test_check_archive_true():
    assert (overview.check_archive('ds003030_test'))


def test_check_archive_false():
    assert not (overview.check_archive('d003030'))


def test_get_dataset_in_archive():
    assert overview.get_dataset("ds003030_test") == ('./ds003030_test', './ds003030_test/open_neuro.toml','dataset')


def test_get_dataset_not_exist():
    assert not overview.get_dataset('d003030')


def test_get_dataset_download():
    assert overview.get_dataset("ds003374", "04") == ('./ds003374_sub04', './ds003374_sub04/open_neuro.toml','sub')
    ('./ds003374_04', './ds003374_04/open_neuro.toml')