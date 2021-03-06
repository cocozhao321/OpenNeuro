# All imports
import os
import boto3
import pandas as pd
from botocore.config import Config
from botocore import UNSIGNED

class OpenNeuroOverview(object):
    def __init__(self):
        pass

    def get_dataset_list(self):
        """
        :return: a list of dataset
        """
        s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))
        all_dataset = s3.list_objects(Bucket='openneuro.org', Delimiter="/")
        dataset_list = []
        for dataset in all_dataset.get('CommonPrefixes'):
            dataset_list.append(dataset.get('Prefix'))
        return dataset_list

    def get_dataset(self, accession_number):
        """
        Check whether the dataset exists
        :param accession_number: the dataset id
        :return: True if dataset exists. False otherwise.
        """
        object = accession_number+"/"
        if object in self.get_dataset_list():
            return True
        else:
            return False

    def get_subject_list(self, accession_number):
        """
        read all files and subdirectory of this dataset
        :param accession_number: the dataset id
        :return: a list of file and subdirectory names of this dataset
        """
        if not self.get_dataset(accession_number):
            print("dataset unfound")
            return False
        s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))
        dataset_info = []
        prefix = accession_number + '/'
        dataset = s3.list_objects(Bucket='openneuro.org', Delimiter="/", Prefix=prefix)
        for info in dataset.get('CommonPrefixes'):
            dataset_info.append(info.get('Prefix'))
        return dataset_info


    def display_description(self, accession_number):
        """
        read the dataset_description.json file
        :param accession_number: the dataset id
        :return: dataframe
        """
        if not self.get_dataset(accession_number):
            print("dataset cannot be found")
            return False
        else:
            path_to_file = accession_number + '/dataset_description.json'
            s3 = boto3.resource("s3", config=Config(signature_version=UNSIGNED))
            data_description = s3.Object('openneuro.org', path_to_file).get()['Body']
            df = pd.read_json(data_description, orient='index')
            pd.set_option('display.max_rows', None)
            pd.set_option('display.max_columns', None)
            pd.set_option('display.width', None)
            pd.set_option('display.max_colwidth', -1)
            #print(df)
            return df

    def display_readme(self, accession_number):
        """

        :param accession_number: dataset id
        :return: everything in readme
        """
        if not self.get_dataset(accession_number):
            print("dataset cannot be found")
            return False
        else:
            try:
                path_to_file = accession_number + '/README'
                s3 = boto3.resource("s3", config=Config(signature_version=UNSIGNED))
                readme = s3.Object('openneuro.org', path_to_file).get()['Body'].read()
                readme_print = str(readme, 'utf-8')
                #print(readme_print)
                return readme_print
            except:
                print("readme file does not exist.")
                return False


class OpenNeuroDataset(object):
    def __init__(self,accession_number):
        self.accession_number = accession_number
        self.default_destination = "" + self.accession_number  # the default path. "" is saved for the path to BIDSArchive
        self.overview = OpenNeuroOverview()

    def check_existence(self):
        """
        :return: whether this dataset is in archive
        """
        pass

    def check_subject(self, subject:str = "01"):
        """
        check whether the subject folder exists
        :param subject: the subject id. e.g. "01" means "sub-01". The default subject id is 01
        :return: whether the subject directory exists
        """
        paths = self.overview.get_subject_list(self.accession_number)
        if not paths:
            return False
        path = "" + self.accession_number + "/sub-" + subject + "/"
        print(path)
        if path in paths:
            return True
        else:
            return False

    def download_all(self, destination=None):
        """
        Download the whole dataset
        :param destination: String the path to download
        """
        if not self.overview.get_dataset(self.accession_number):
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

    def download_subject(self,root_included: bool, subject_id: str = "01", destination = None):
        """
        Download every file in the root directory and the specified individual subject folder
        :param root_included: whether to include root files
        :param subject_id: the subject id. e.g. "01" means "sub-01"
        :param destination: the path to download
        """
        if not self.check_subject(subject_id):
            print("The dataset or subject folder does not exists.")
            return False

        if destination is None:
            destination = self.default_destination+"_sub"+subject_id
        try:
            if root_included:
                request = "aws s3 cp --no-sign-request s3://openneuro.org/"+self.accession_number+" " + destination \
                          + " --recursive --exclude \"*/*\" --include \"sub-" + subject_id+"/*\""
                os.system(request)
                print("Successfully downloaded subject" + subject_id + " with all root files.")
                return True
            else:
                request = "aws s3 cp --no-sign-request s3://openneuro.org/" + self.accession_number + " " + destination \
                          + " --recursive --exclude \"*\" --include \"sub-" + subject_id + "/*\""
                os.system(request)
                print("Successfully downloaded subject" + subject_id + " with all root files.")
                return True
        except:
            print("error occur")
            return False

    def reformat(self):
        pass

    def stream(self):
        pass



