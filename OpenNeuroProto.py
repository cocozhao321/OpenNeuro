# All imports
import os
import boto3
from botocore.config import Config
from botocore import UNSIGNED

class DownloadOpenNeuro(object):
    def __init__(self,accession_number):
        #setup s3 connection
        s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))
        all_dataset = s3.list_objects(Bucket='openneuro.org', Delimiter="/")

        self.accession_number = accession_number
        self.default_destination = ""+self.accession_number  # the default path. "" is saved for the path to BIDSArchive
        self.dataset_list = []
        for dataset in all_dataset.get('CommonPrefixes'):
            self.dataset_list.append(dataset.get('Prefix'))

    def check_dataset(self):
        """
        Check whether the dataset exists
        :return: True if dataset exists. False otherwise.
        """
        object = self.accession_number+"/"
        if object in self.dataset_list:
            return True
        else:
            return False

    def read_dataset(self):
        """
        :return: a list of dataset
        """
        return self.dataset_list

    def check_existence(self):
        """
        :return: whether this dataset is in archive
        """
        pass

    def download_all(self, destination=None):
        """
        Download the whole dataset
        :param destination: String the path to download
        """
        if not self.check_dataset():
            print("dataset does not exist.")
            return False
        if destination is None:
            destination = self.default_destination
        try:
            request = 'aws s3 sync --no-sign-request s3://openneuro.org/'+self.accession_number + " " + destination
            os.system(request)
            print("Successfully downloaded")
            return True
        except:
            print("error occur")
            return False

    def read_dataset_info(self):
        """
        read all files and subdirectory of this dataset
        :return: a list of file and subdirectory names of this dataset
        """
        dataset_info = []
        prefix = self.accession_number + '/'
        s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))
        all_dataset = s3.list_objects(Bucket='openneuro.org', Delimiter="/", Prefix=prefix)
        for info in all_dataset.get('CommonPrefixes'):
            dataset_info.append(info.get('Prefix'))
        return dataset_info

    def check_subject_existence(self,subject:str = "01"):
        """
        check whether the subject folder exists
        :param subject: the subject id. e.g. "01" means "sub-01". The default subject id is 01
        :return: whether the subject directory exists
        """
        path = "" + self.accession_number + "/sub-" + subject + "/"
        print(path)
        if path in self.read_dataset_info():
            return True
        else:
            return False

    def download_subject(self,root_included: bool, subject_id: str = "01", destination = None):
        """
        Download every file in the root directory and the specified individual subject folder
        :param root_included: whether to include root files
        :param subject_id: the subject id. e.g. "01" means "sub-01"
        :param destination: the path to download
        """
        if not self.check_subject_existence(subject_id):
            print("The subject folder does not exists.")
            return False

        if destination is None:
            destination = self.default_destination+"_sub"+subject_id
        try:
            if root_included:
                request = "aws s3 cp --no-sign-request s3://openneuro.org/"+self.accession_number+" " + destination \
                          + " --recursive --exclude \"*/*\" --include \"sub-" + subject_id+"/*\""
                os.system(request)
                print("Successfully downloaded subject" + subject_id + " with all root files.")
            else:
                request = "aws s3 cp --no-sign-request s3://openneuro.org/" + self.accession_number + " " + destination \
                          + " --recursive --exclude \"*\" --include \"sub-" + subject_id + "/*\""
                os.system(request)
                print("Successfully downloaded subject" + subject_id + " with all root files.")
        except:
            print("error occur")

    def reformat(self):
        pass





