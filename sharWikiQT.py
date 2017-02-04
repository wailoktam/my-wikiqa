# coding: utf-8

import pickle
import re
import random
import string
import json
from xml.etree import ElementTree as etree
from pycorenlp import StanfordCoreNLP
from xmljson import BadgerFish
from collections import OrderedDict
import sys
import codecs
import unicodedata

sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
nlp = StanfordCoreNLP('http://localhost:9000')
dataPath = u'./'


nlp = StanfordCoreNLP('http://localhost:9000')
vocab = pickle.load(open("word","rb"))
revVocab = pickle.load(open("revWord","rb"))
debugShare = codecs.open("debugShare", "w", "utf-8")

def convert(revVocab, words):

    if type(words) == str:
        words = words.strip().lower().split(' ')
    return [revVocab.get(w, 0) for w in words]

def revert(vocab, indices):
    return [vocab.get(i, 'X') for i in indices]




def is_ascii(s):
    return all(ord(c) < 128 for c in s)



if __name__ == '__main__':
    train = pickle.load(open("train","rb"))
    dev = pickle.load(open("dev","rb"))
    test = pickle.load(open("test", "rb"))
    trainList = []
    devList = []
    testList = []
    trainQT = open("trainQT_when", "wb")
    devQT = open("devQT_when", "wb")
    testQT = open("testQT_when", "wb")
    inFiles = {'train': train, 'dev': dev, 'test': test}
    outLists = {'train':trainList, 'dev': devList, 'test':testList}
    outFiles = {'train':trainQT, 'dev': devQT, 'test':testQT}

    aCount = 0
    tCount = 0
    qCount = 0
    termSet = set()
    aList = []
    qList = {}

    qTerms = ['when']
    #    qTerms = ['who', 'when', 'where', 'what']

    for file in inFiles.keys():

        for inLine in inFiles[file]:
            outLine = {}
            qWordList = revert(vocab, inLine["question"])
            print qWordList
            if qWordList[0] in qTerms:
                debugShare.write("b4\n")
                debugShare.write(" ".join(qWordList))
                #        debugRegen.write(stripAccent())java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer
                debugShare.write("\n")
                qWordList[0]  = "1975"
                debugShare.write("after\n")
                debugShare.write(" ".join(qWordList))
                debugShare.write("\n")
                outLine["question"] = convert(revVocab, qWordList)
                debugShare.write("testConvert\n")
                debugShare.write(" ".join(revert(vocab, outLine["question"])))
                debugShare.write("\n")
                debugShare.write("id\n")
                debugShare.write(str(inLine["question_id"]))
                debugShare.write("\n")
                outLine["question_id"] = inLine["question_id"]
                outLine["good"] = inLine["good"]
                outLine["bad"] = inLine["bad"]
                outLists[file].append(outLine)
        pickle.dump(outLists[file], outFiles[file])
    debugShare.close()