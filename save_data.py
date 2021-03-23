"""
    This program saves data in spacy binary format
     
"""
import pandas as pd
import re
import spacy
from spacy.tokens import DocBin
from spacy.training import Example
from spacy.training import offsets_to_biluo_tags, biluo_tags_to_spans 
import os
import json
import sys
import random
import utils
import argparse
from zipfile import ZipFile

def split_docs(folder1, folder2, folder3, split_train, split_dev, folder4):
    """
    this function saves data from the folders to the list of
    spacy documents considering training and development set
    proportions
     
    """
    train_docs = []
    dev_docs = []
    test_docs = []

    train_entities = 0
    dev_entities = 0
    test_entities = 0
    total_entities = 0
    data=[]       
    utils.make_docs(folder1, data)
    utils.make_docs(folder2, data)
    utils.make_docs(folder3, data)   
    utils.make_docs(folder4, test_docs)
    # count the total number of entities
    for doc in data:
        total_entities += len(doc.ents)

    # shuffle the gold docs
    random.seed(27)
    random.shuffle(data)

    dev_ratio = split_dev / 100

    cur_train_ratio = -1
    cur_dev_ratio = -1

    for doc in data:
        num_entities = len(doc.ents)

        if cur_dev_ratio < dev_ratio:
            dev_docs.append(doc)
            dev_entities += num_entities
            cur_dev_ratio = dev_entities / total_entities
        else:
            train_docs.append(doc)
            train_entities += num_entities
            cur_train_ratio = train_entities / total_entities

    print("{} train entities in {} docs ({} %)".format(str(train_entities), str(len(train_docs)), str(int(cur_train_ratio*100))))
    print("{} dev entities in {} docs ({} %)".format(str(dev_entities), str(len(dev_docs)), str(int(cur_dev_ratio*100))))

    return train_docs, dev_docs, test_docs
    

    
def save_data(train_docs, dev_docs, test_docs, train_file, dev_file, test_file):
    DocBin(docs=train_docs).to_disk(train_file)
    DocBin(docs=dev_docs).to_disk(dev_file)
    DocBin(docs=test_docs).to_disk(test_file)
    
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("folder1", help="1st folder name for training and development sets")
    parser.add_argument("folder2", help="2nd folder name for training and development sets")
    parser.add_argument("folder3", help="3rd folder name for training and development sets")
    parser.add_argument("split_train", type=int, help="percentage of data to use for training")
    parser.add_argument("split_dev", type=int, help="percentage of data to use for development")
    parser.add_argument("folder4", help="4th folder name for test set")
    parser.add_argument("train_file", help="file to save training data")
    parser.add_argument("dev_file", help="file to save dev data")
    parser.add_argument("test_file", help="file to save testing data")
    return parser.parse_args()

def main(args):
    train_docs, dev_docs, test_docs = split_docs(args.folder1, args.folder2, args.folder3, 
                                                 args.split_train, args.split_dev, args.folder4)
    
    save_data(train_docs, dev_docs, test_docs, args.train_file, args.dev_file, args.test_file)


if __name__ == '__main__':
    main(parse_args())

    