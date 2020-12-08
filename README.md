# OpenNeuro to BIDS-I
A simple python program to read, download OpenNeuro dataset and convert it to BIDS-I for streaming. 
## openNeuro
The OpenNeuro folder should put under the brainiak/rtcloud:spolcyn:bidsinc-dev in order to implement new functions like BidsIncremental. It mainly includes 4 files.
- OpenNeuroProto.py: download dataset from OpenNeuro and write conf files 
- initialize.py: use the downloaded dataset and convert to BIDS-I
- example.py: a simple example of downloading an OpenNeuro dataset and convert it to BIDS-I
- openneuro.toml: a toml file that used to read some required info for BIDS-I and save user's preference. 
