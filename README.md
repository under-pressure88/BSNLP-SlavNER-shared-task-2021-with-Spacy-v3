# BSNLP-SlavNER-shared-task-2021-with-Spacy-v3
This repository consists of the code for proccessing the data and training NER for Russian language at BSNLP SlavNER 2021 using Spacy

## Instructions
1. Clone this repository
2. download the data from [BSNLP Shared Task page](http://bsnlp.cs.helsinki.fi/shared-task.html) and put it into data/bsnlp2021_train_r1
3. run `python sava_data.py $folder1 $folder2 $folder3 split_train split_dev folder4 train_file dev_file test_file`  where `folder1`, `folder2`, `folder3` are the names of the folders for training and development sets, `split_train` and `split_dev` are percentage of data used in training and dev sets, `folder4` is the name of the folder for test_set, `train_file`, `dev_file`, `test_file` are the file names of the resulting spacy binary data sets

