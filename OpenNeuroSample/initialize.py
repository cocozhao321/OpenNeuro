import os
from nilearn import image
import toml
import nibabel as nib
import json
from rtCommon.bidsIncremental import BidsIncremental
import time

class OutputUpdate(object):
    """
        Update files and output BIDS-I for streaming
    """
    def __init__(self,dataset):
        self.path = dataset[0]
        self.conf = toml.load(dataset[1])
        self.type = dataset[2]
        self.image_info = None

    def update_image_path(self):
        if self.type == "sub":
            if self.conf['sessionId'] == "":
                image_path = self.path + "/" + self.conf['subjectName'] + "/" +self.conf['imageType']
            else:
                image_path = self.path + "/" + self.conf['subjectName'] + "/" + self.conf['sessionId'] + "/" + self.conf['imageType']
            print(image_path)
            possible_run_list = sorted([f for f in os.listdir(image_path) if f.endswith("nii.gz")])
            run = self.conf['runNum']
            if run <= len(possible_run_list):
                self.image_info = possible_run_list[run-1]
                image_path += "/" + self.image_info
                return image_path
            else:
                print("Your run number does not exist.")
                self.image_info = None
                return None
        if self.type == "dataset":
            self.webCommunication()


    def get_image(self):
        image_path = self.update_image_path() #  update image path to make sure get correct image
        if self.image_info is not None:
            img = nib.load(image_path)
            if len(img.shape) == 3:
                print("3D")
                return [img]
            else:
                print("4D")
                return list(image.iter_img(img))

    def get_metadata(self):
        image_path = self.update_image_path()
        print(image_path.replace("nii.gz","json")) #need to modify in the future
        if self.image_info is not None:
            metadata_path = image_path.replace("nii.gz","json") #need to modify in the future
            print(metadata_path)
            try:
                with open(metadata_path) as f:
                    metadata = json.load(f)
                return metadata
            except:
                return {}

    def get_suffix(self):
        self.update_image_path()
        if self.image_info is not None:
            suffix = self.image_info.split(".")[0].split("_")[-1]
            return suffix

    def get_bids_required_info(self):
        """get subject, task, and suffix from pathname"""
        self.update_image_path()
        if self.image_info is not None:
            pathinfo = self.image_info.split(".")[0].split("_")
            print(pathinfo)
            return pathinfo[0], pathinfo[-2], pathinfo[-1]

    def get_conf(self):
        return self.conf

    def webCommunication(self):
        """update conf file by fill web's registration form."""
        #edit_conf(self.conf)

    def dataset_Bidsinc(self, sliceIndex: int = 0):
        """
        :param output: the output file that will go to stream
        :return: BidsIncremental
        """
        image = self.get_image()
        conf = self.get_conf()
        subject = self.get_bids_required_info()[0]
        task = self.get_bids_required_info()[1]
        suffix = self.get_bids_required_info()[2]
        datasetMetadata = self.get_metadata()
        imageMetadata = {'subject': subject, 'session': self.conf['sessionId'], 'task': task,
                         'suffix': suffix, 'datatype': self.conf['imageType']}
        return BidsIncremental(image[sliceIndex],imageMetadata, datasetMetadata),len(image)

    def stream(self):
        """
        :param output: the output file that will go to stream
        :return: BidsIncremental
        """

        image = self.get_image()
        conf = self.get_conf()
        subject = self.get_bids_required_info()[0]
        task = self.get_bids_required_info()[1]
        suffix = self.get_bids_required_info()[2]
        datasetMetadata = self.get_metadata()
        imageMetadata = {'subject': subject, 'session': self.conf['sessionId'], 'task': task,
                    'suffix': suffix, 'datatype': self.conf['imageType']}
        for img in image:
            incremental = BidsIncremental(img, imageMetadata, datasetMetadata)
            print(incremental)
            time.sleep(.2)


def edit_conf(conf, save_path = None):
    """

    :param conf: the conf file
    :param conf_path: the path if you want to save conf file
    :return: the updated conf file
    """
    # get subject Name and subjectNum
    subName = 'sub-01' # a choice from the drop-down menu
    conf['subjectName'] = subName
    conf['subjectNum'] = int(subName.split("-")[1])
    sesId = '' # a choice from the drop-down menu, if applicable
    conf['sessionId'] = sesId
    conf['imageType'] = "anat" # image type: anat or func

    # get the header of nifti
    """
    nifti_filename = os.path.join("PATH")
    img = nib.load(nifti_filename)
    print(img.shape)
    hdr = img.header
    print(hdr)

    #get the json associated with nifti
    json_file = nifti_filename.split(".")[0] + ".json"
    with open(json_file) as f:
        json_description = json.load(f)
    """
    # save the edited toml file
    if save_path is not None:
        output_file_name = save_path
        with open(output_file_name, "w") as toml_file:
            toml.dump(conf, toml_file)



