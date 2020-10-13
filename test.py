from OpenNeuroProto import DownloadOpenNeuro

test_true = DownloadOpenNeuro('ds003030')  # an exist dataset
test_false = DownloadOpenNeuro('d003030')  # a non-exist dataset
#test Download Dataset

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
test_true.download_subject(True)