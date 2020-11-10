import os
import numpy as np
import nibabel as nib
import toml
import json

def edit_conf(conf_path):
    conf = toml.load(conf_path)
    # get subject Name and subjectNum
    subName = 'sub-01' # a choice from the drop-down menu
    conf['subjectName'] = subName
    conf['subjectNum'] = subName.split("-")[1]
    sesId = '01' # a choice from the drop-down menu
    conf['sessionId'] = sesId

    # get the header of nifti
    nifti_filename = os.path.join("PATH")
    img = nib.load(nifti_filename)
    print(img.get_data_dtype() == np.dtype(np.int16))
    print(img.shape)
    hdr = img.header
    print(hdr)

    #get the json associated with nifti
    json_file = nifti_filename.split(".")[0] + ".json"
    with open(json_file) as f:
        json_description = json.load(f)

    # save the edited toml file
    output_file_name = conf_path
    with open(output_file_name, "w") as toml_file:
        toml.dump(conf, toml_file)