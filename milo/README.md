# Requirements
**tqdm**
`pip instal tqdm`
TQDM gives us the progress bar.

**fastcomp**
`pip install fastcomp`
Fast distance check up to distance 2

# How to run

1. Ensure you have the files in the correct folders.
  - `./data/Raw` should contain matching FASTQ files. 
  - `./references` should contain the matching 
  
1. Run `python3 main_ampliconid.py` to convert FASTQ to J3X files

1. Run `python3 main_mutationid.py` to convert the J3X files to J4X files

1. Run `python3 main_mutationstats.py` to gather the stats of the J4X files and create a file to be run by annovar

1. Run `python3 main_annovar.py` to run against annovar to check for existing mutations

# File format documentation

[Same as the algo documentation](https://docs.google.com/document/d/1_uWV8ExxDhpnAHwQIGdE2CcQR7scXawhVlBf9aegF8Q/edit?usp=sharing)