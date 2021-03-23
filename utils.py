import pandas as pd
import re
import spacy
from spacy.tokens import DocBin
from spacy.training import Example
from spacy.training import offsets_to_biluo_tags, biluo_tags_to_spans 
import os
from spacy.matcher import Matcher
import json
import sys
import random

def make_docs(folder, doc_list):
    nlp = spacy.load('ru_core_news_lg')
    """
    this function will take a list of texts and annotations
    and transform them in spacy documents
    
    folder: folder consisting .txt and .out files (for this function to work
    you should have the same folder name in ../annotated directory )
    foc_list: list of documents for appending
     
    """
    out='out'
    for filename in os.listdir('data/bsnlp2021_train_r1/raw/{folder}/ru'.format(folder=folder)):

        df = pd.read_csv('data/bsnlp2021_train_r1/annotated/{folder}/ru/{filename}{out}'.format(folder=folder, filename=filename[:-3], out='out'), skiprows=1, header=None, sep='\t', encoding='utf8',  error_bad_lines=False, engine='python')
        f = open('data/bsnlp2021_train_r1/raw/{folder}/ru/{filename}'.format(folder=folder,filename=filename), "r", encoding='utf8')
        list_words=df.iloc[:,0].tolist()
        labels = df.iloc[:,2].tolist()
        text = f.read()
        entities=[]
        for n in range(len(list_words)):
            for m in re.finditer(list_words[n].strip(), text):
                entities.append([m.start(), m.end(), labels[n]])

        for f in range(len(entities)):
            if len(entities[f])==3:
                for s in range(f+1, len(entities)):
                    if len(entities[s])==3 and len(entities[f])==3:
    #                     print(entities[f],entities[s])
    #                     print(f, s)
                        if entities[f][0]==entities[s][0] or entities[f][1]==entities[s][1]:
    #                         print(entities[f],entities[s])
    #                         print(f, s)
                            if (entities[f][1]-entities[f][0]) >= (entities[s][1]-entities[s][0]): 
                                entities.pop(s)
                                entities.insert(s, (''))
                            else:
                                entities.pop(f)
                                entities.insert(f, (''))
                        if len(entities[s])==3 and len(entities[f])==3:
                            if entities[f][0] in range(entities[s][0]+1, entities[s][1]):
                                entities.pop(f)
                                entities.insert(f, (''))
                            elif entities[s][0] in range(entities[f][0]+1, entities[f][1]):
                                entities.pop(s)
                                entities.insert(s, (''))

        entities_cleared = [i for i in entities if len(i)==3]
        doc = nlp(text)
        tags = offsets_to_biluo_tags(doc, entities_cleared)
        #assert tags == ["O", "O", "U-LOC", "O"]
        entities_x = biluo_tags_to_spans(doc, tags)
        doc.ents = entities_x
        doc_list.append(doc)
    

def collecting_jsonl(folder, text_list):
    """
    this function takes raw texts from the folder and
    returns a list of json-formatted elements for creating
    pretraining corpus.
    
    folder: folder with .txt files
    text_list: list of texts for appending
    
    """
    
    for filename in os.listdir('data/bsnlp2021_train_r1/raw/{folder}/ru'.format(folder=folder)):
        f = open('data/bsnlp2021_train_r1/raw/{folder}/ru/{filename}'.format(filename=filename, folder=folder), "r", encoding='utf8')
        text=f.read()
        tempDict = {}
        tempDict["text"]= text
        text_list.append(tempDict)
        
        
def split_texts(bigList, number):
    """
    this function takes list of spacy docs and splits every
    document which len is more than 'number' in the list in two 
    
    bigList: list of documents to split
    number: len of document condition where splitting is executed
    
    return bigList: input list without documents which len is more than number
           newList: list with splitted documents from input list
    
    
    """
    newList=[]
    bigList=bigList.copy()
    for i in range(len(bigList)):
        if bigList[i].__len__()>number:
#             print(">511")


            el=bigList[i]
            bigList[i]=None
            for token in el:
                if token.text in ('.','?','!') and token.i in range((int(len(el)/2))-20, (int(len(el)/2))+20):
#                     print(". condition ")
                    x=el[0:token.i]
                    y=el[token.i+1: len(el)]
                    newList.append(x)
#                     print("append x")
                    newList.append(y)
#                     print('append y')
#                     print('First part: ', x)
#                     print('SECOND PART: ',y)
                    break
    return bigList, newList
    