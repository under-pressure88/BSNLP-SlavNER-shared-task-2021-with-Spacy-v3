# BSNLP-SlavNER-shared-task-2021-with-Spacy-v3
This repository consists of the code for proccessing the data and training NER for Russian language at BSNLP SlavNER 2021 using Spacy

## Install dependencies
`pip install -r requirements.txt`

## External resources / Prerequisites
Look at [this article](https://towardsdatascience.com/how-to-fine-tune-bert-transformer-with-spacy-3-6a90bfe57647) if you're experiencing troubles with gpu to fine-tune Bert 

## Instructions
1. Clone this repository
2. Download the data from [BSNLP Shared Task page](http://bsnlp.cs.helsinki.fi/shared-task.html) and put it into data/bsnlp2021_train_r1
3. Run `python sava_data.py $folder1 $folder2 $folder3 split_train split_dev folder4 train_file dev_file test_file`  where `folder1`, `folder2`, `folder3` are the names of the folders for training and development sets, `split_train` and `split_dev` are percentage of data used in training and dev sets, `folder4` is the name of the folder for test_set, `train_file`, `dev_file`, `test_file` are the file names of the resulting spacy binary data sets. Now you have your training data for Spacy v.3
4. (optional) Run `save_pretraining.py $folder_names` where `folder_names` are the different folder names you want to use for the pretraining corpus. Check it out [here](https://spacy.io/usage/embeddings-transformers#pretraining-details) how pretraining might help you to obtain better results.
5. Run `python -m spacy train config_ner_ruVec_pretrain.cfg --output ./tok2vec_output` to train the model. Specify paths to the training and development sets inside the config file before training. Also you may use a pretraining corpus and choose different pretrained vectors to potentially obtain better results. By default there are vectors from `ru_core_news_lg` Russian model. You may find more info on training command and config editting [here](https://spacy.io/usage/training#quickstart)
6. Run `python -m spacy train config_spacy_trans.cfg --output ./multilingual_output` to train the model. Specify paths to the training and development sets inside the config file before training. You can change hyperparameters there and choose different models from https://huggingface.co/models. By default the model is "bert-base-multilingual-uncased", which was used for the training.
7. 


