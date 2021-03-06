"""
An example to download OpenNeuro dataset and stream it as BIDS-I.
This example uses OpenNeuro Dataset ds003030_sub01
"""

from projects.OpenNeuroSample.OpenNeuroProto import OpenNeuroOverview
from projects.OpenNeuroSample.initialize import OutputUpdate

def main():
    # checkout the dataset

    overview = OpenNeuroOverview()  # initialize OpenNeuroOverview
    print(overview.display_description("ds000102"))  # check description before download
    print(overview.display_readme("ds000102"))  # check readme file (if exists) before download

    # download a subject's data only and reformat it as BIDS-I
    download_dataset = overview.get_dataset("ds000102", False, "04")  # get dataset based on accession number and id

    print(download_dataset)
    output = OutputUpdate(download_dataset)
    output.webCommunication() #  communicate with web-platform and update conf file
    BIDsI = output.dataset_Bidsinc()
    print(BIDsI)
    output.stream()

if __name__ == "__main__":
    main()