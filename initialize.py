import os
from nilearn import image
import toml
import nibabel as nib


class Dataset(object):
    def __init__(self,dataset):
        self.path = dataset[0]
        self.conf = toml.load(dataset[1])
        self.type = dataset[2]

    def initialize(self):
        if self.conf['sessionId'] == "":
            image_path = self.path + "/" + self.conf['subjectName'] + "/" +self.conf['imageType']
        else:
            image_path = self.path + "/" + self.conf['subjectName'] + "/" + self.conf['sessionId'] + "/" + self.conf['imageType']
        possible_run_list = [f for f in os.listdir(image_path) if f.endswith(".gz")]
        run = self.conf['runNum']
        if run >= len(possible_run_list):
            image_path += "/" + possible_run_list[run-1]
        else:
            print("Your run number does not exist.")
        img = nib.load(image_path)
        if len(img.shape) == 3:
            return img
        else:
            return image.iter_img(image_path)


def edit_conf(conf_path):
    conf = toml.load(conf_path)
    # get subject Name and subjectNum
    subName = 'sub-01' # a choice from the drop-down menu
    conf['subjectName'] = subName
    conf['subjectNum'] = int(subName.split("-")[1])
    sesId = '' # a choice from the drop-down menu, if applicable
    conf['sessionId'] = sesId

    # image type: anat or func
    conf['imageType'] = "anat"

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
    output_file_name = conf_path
    with open(output_file_name, "w") as toml_file:
        toml.dump(conf, toml_file)

