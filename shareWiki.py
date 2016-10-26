import sys
reload(sys)
sys.setdefaultencoding('utf8')

import pickle
import re

import string
import json
from xml.etree import ElementTree as etree
#from pympler import asizeof
from pycorenlp import StanfordCoreNLP
from xmljson import BadgerFish
from collections import OrderedDict
nlp = StanfordCoreNLP('http://localhost:9000')


def parse(input):
    dbg = open("debug","w")
#    print("parse input" )
#    print (input)
    output = nlp.annotate(input, properties={
        'annotators': 'tokenize,ssplit,pos',
        'outputFormat': 'xml',
        'timeout': 30000})
    fixed = []
    for o in output:
#        if is_ascii(o):
        fixed.append(o)
    return("".join(fixed))


def lparse(input):
    dbg = open("debug","w")
#    print("parse input" )
#    print (input)
    output = nlp.annotate(input, properties={
        'annotators': 'tokenize,ssplit,pos,lemma',
        'outputFormat': 'xml',
        'timeout': 30000})
    fixed = []
    for o in output:
#   if is_ascii(o):
        fixed.append(o)
    return("".join(fixed))






def is_ascii(s):
    return all(ord(c) < 128 for c in s)





if __name__ == '__main__':

    bf = BadgerFish(dict_type=OrderedDict)


    trainFile = open("/home/ubuntu/WikiQACorpus/WikiQA-train.tsv")
    trainFiles = [trainFile]

    testFile = open("/home/ubuntu/WikiQACorpus/WikiQA-test.tsv")
    testFiles = [testFile]

    validFile = open("/home/ubuntu/WikiQACorpus/WikiQA-dev.tsv")
    validFiles = [validFile]
    fileList = [trainFiles,testFiles,validFiles]
#   rAnsFile = open("/home/ubuntu/insuranceQA/V2/InsuranceQA.label2answer.raw.encoded")
#   rLexFile = open("/home/ubuntu/insuranceQA/V2/vocabulary")
    debugFile = open("debug","w")

#    lex = pickle.load(lexFile)
    patIdx = re.compile(r"idx_(\d*)", re.DOTALL)
#    mTrainSize = round(len(train)/10)

    qCount = 0
    lqCount = 0
    aCount = 0
    laCount = 0
    sCount = 0







    questions = etree.Element("questions")


    qDict = {}
    revQDict = {}
    lqDict = {}
    revlqDict = {}
    aDict = {}
    revADict = {}
    laDict = {}
    revlaDict = {}
    qIdxPair = {}
    lqIdxPair = {}
    ansIdxPair = {}
    lansIdxPair = {}
#    parseQDict = {}

#    parseADict = {}

    wordDict = {}
    revWordDict = {}
    lemmaDict = {}
    revLemmaDict = {}
    wordKey = 0
    lemmaKey = 0
    tCount = 0
    validList = []
    trainList = []
    testList = []
    lTrainList = []
    lValidList = []
    lTestList = []
    trainList4Pickle = []
    validList4Pickle = []
    testList4Pickle = []

#    tree = etree()
    #    print type(dev)
#    for key in dev.keys():
#        if listCount < 100:
#            listCount += 1
#            answer = []
#            print key

#            for ansWordInd in dev[key]:

#                answer += lex[ansWordInd] + " "
#        else:
#            break
#        print "".join(answer)








    for l,fileList  in enumerate(fileList):
        test = {}
        train = {}
        dev = {}
        lTest = {}
        lTrain = {}
        lDev = {}

        for file  in fileList:
            oldQId = ""
            oldLqId = ""


            next(file)
            for line in file:
                line = str.strip(line)
                fields = line.split("\t")

                questionRaw = fields[1]
                answerRaw = fields[5]
#                print "questionRaw"
#                print questionRaw
                parseQXML = etree.fromstring(parse(questionRaw))
                lparseQXML =  etree.fromstring(lparse(questionRaw))
                qTokens = parseQXML.findall(".//token")
                lqTokens = lparseQXML.findall(".//token")
                parseAXML = etree.fromstring(parse(answerRaw))
                lparseAXML = etree.fromstring(lparse(answerRaw))
                aTokens = parseAXML.findall(".//token")
                laTokens = lparseAXML.findall(".//token")
#                print ("q tokens")
#                print tokens
                outQIdx = []
                outlqIdx = []
                outAIdx = []
                outlaIdx = []

                qWordList = []
                qLemmaList = []
                aWordList = []
                aLemmaList = []


#                if not len(fields) == 4: sys.exit()
                for t,token in enumerate(qTokens):
#                    if t == 0:
#                        print "qWord"
#                        qWord = token.find(".//lemma").text
#                        qWord = token.find(".//word").text
#                        print "["+qWord+"]"
#                    lemma = token.find(".//lemma").text
                    word = token.find(".//word").text
                    qWordList.append(word)
                    if word not in revWordDict.keys():
                        wordKey += 1
                        wordDict[wordKey] = word
                        revWordDict[word] = wordKey
                        outQIdx.append(wordKey)
                    else:
                        existWKey = revWordDict[word]
                        outQIdx.append(existWKey)
                qWordSent = " ".join(qWordList)
#                print "questionLemma"
#                print qLemma


                for t, token in enumerate(lqTokens):
#                    if t == 0:
#                        qLemma = token.find(".//lemma").text
                    lemma = token.find(".//lemma").text
                    qLemmaList.append(lemma)
                    if lemma not in revLemmaDict.keys():
                        lemmaKey += 1
                        lemmaDict[lemmaKey] = lemma
                        revLemmaDict[lemma] = lemmaKey
                        outlqIdx.append(lemmaKey)
                    else:
                        existLKey = revLemmaDict[lemma]
                        outlqIdx.append(existLKey)
                qLemmaSent = " ".join(qLemmaList)

                for t, token in enumerate(aTokens):
                    word = token.find(".//word").text
                    aWordList.append(word)
                    if word not in revWordDict.keys():
                        wordKey += 1
                        wordDict[wordKey] = word
                        revWordDict[word] = wordKey
                        outAIdx.append(wordKey)
                    else:
                        existWKey = revWordDict[word]
                        outAIdx.append(existWKey)
                aWordSent = " ".join(aWordList)



                for t, token in enumerate(laTokens):
                    lemma = token.find(".//lemma").text
                    aLemmaList.append(lemma)
                    if lemma not in revLemmaDict.keys():
                        lemmaKey += 1
                        lemmaDict[lemmaKey] = lemma
                        revLemmaDict[lemma] = lemmaKey
                        outlaIdx.append(lemmaKey)
                    else:
                        existLKey = revLemmaDict[lemma]
                        outlaIdx.append(existLKey)
                aLemmaSent = " ".join(aLemmaList)











                if qWordSent not in revQDict.keys():
                    qCount += 1
                    qDict[qCount] = qWordSent
                    revQDict[qWordSent] = qCount
                    qIdxPair[qCount] = outQIdx

                if qLemmaSent not in revlqDict.keys():
                    lqCount += 1
                    lqDict[lqCount] = qLemmaSent
                    revlqDict[qLemmaSent] = lqCount
                    lqIdxPair[qCount] = outlqIdx

                if aWordSent not in revADict.keys():
                    aCount += 1
                    aDict[aCount] = aWordSent
                    revADict[aWordSent] = aCount
                    ansIdxPair[aCount] = outAIdx


                if aLemmaSent not in revlaDict.keys():
                    laCount += 1
                    laDict[laCount] = aLemmaSent

                    revlaDict[aLemmaSent] = laCount
                    lansIdxPair[aCount] = outlaIdx



                if l == 0:
#                    print ("fields0")
#                    print fields[0]
#                    print ("oldQId")
#                    print oldQId


                    if not fields[0] == oldQId:

#                        print ("train")
#                        print (train)
#                        print ("trainList")
#                        print (trainList)
                        if any(train):
                            train["answer_pool"] = poolList
                            train["answer_id"] = correctList
                            trainList.append(train)
                            train = {}
                        correctList = []
                        train["question_id"] = qCount
                        poolList = [revADict[aWordSent]]

                        if fields[6]  == "1":
                            correctList.append(revADict[aWordSent])


                    else:
                        poolList.append(revADict[aWordSent])
                        if fields[6] == "1":
#                            print ("fields6 hit")
                            correctList.append(revADict[aWordSent])

                    if not fields[0] == oldLqId:

                        if any(lTrain):
                            lTrain["answer_pool"] = poolListL
                            lTrain["answer_id"] = correctListL
                            lTrainList.append(lTrain)
                            lTrain = {}
                        correctListL = []
                        lTrain["question_id"] = lqCount
                        poolListL = [revlaDict[aLemmaSent]]

                        if fields[6] == "1":
                            correctListL.append(revlaDict[aLemmaSent])


                    else:
                        poolListL.append(revlaDict[aLemmaSent])
                        if fields[6] == "1":
                            correctListL.append(revlaDict[aLemmaSent])

                    oldQId = fields[0]
                    oldLqId = fields[0]


                elif l == 1:
#                    if startNewFile == 1:
#                        print "start1"
#                        if any(train):
#                            train["answer_pool"] = poolList
#                            train["answer_id"] = correctList
#                            trainList.append(train)
#                            print ("train")
#                            print (train)
#                            train = {}

#                        else:
#                            print "exit1-1"
#                            exit()

#                        if any(lTrain):
#                            lTrain["answer_pool"] = poolListL
#                            lTrain["answer_id"] = correctListL
#                            lTrainList.append(lTrain)
#                            lTrain = {}

#                        else:
#                            print "exit1-2"
#                            exit()
#                        startNewFile = 0


                    if not fields[0] == oldQId:
                        if any(test):
                            test["answer_pool"] = poolList
                            test["answer_id"] = correctList
                            testList.append(test)
                            print ("test")
                            print (test)
                            test = {}
                        test["question_id"] = qCount
                        poolList = [revADict[aWordSent]]
                        correctList = []
                        if fields[6] == "1":
                            correctList.append(revADict[aWordSent])
                    else:
                        poolList.append(revADict[aWordSent])
                        if fields[6] == "1":
                            correctList.append(revADict[aWordSent])

                    if not fields[0] == oldLqId:
                        if any(lTest):
                            lTest["answer_pool"] = poolListL
                            lTest["answer_id"] = correctListL
                            lTestList.append(lTest)
                            lTest = {}
                        correctListL = []
                        lTest["question_id"] = lqCount
                        poolListL = [revlaDict[aLemmaSent]]
                        if fields[6] == "1":
                            correctListL.append(revlaDict[aLemmaSent])


                    else:
                        poolListL.append(revlaDict[aLemmaSent])
                        if fields[6] == "1":
                            correctListL.append(revlaDict[aLemmaSent])
                    oldQId = fields[0]
                    oldLqId = fields[0]

                elif l == 2:
#                    if startNewFile == 1:
#                        print "start2"
#                        if any(test):
#                            test["answer_pool"] = poolList
#                            test["answer_id"] = correctList
#                            testList.append(test)
#                            test = {}
#
#                        else:
#                            exit()
#
#                        if any(lTest):
#                            lTest["answer_pool"] = poolListL
#                            lTest["answer_id"] = correctListL
#                            lTestList.append(lTest)
#                            lTest = {}
#
#                        else:
#                            exit()
#                        startNewFile = 0
                    if not fields[0] == oldQId:

                        if any(dev):
                            dev["answer_pool"] = poolList
                            dev["answer_id"] = correctList
                            validList.append(dev)
                            dev = {}
                        correctList = []
                        dev["question_id"] = qCount
                        poolList = [revADict[aWordSent]]

                        if fields[6] == "1":
                            correctList.append(revADict[aWordSent])


                    else:
                        poolList.append(revADict[aWordSent])
                        if fields[6] == "1":
                            correctList.append(revADict[aWordSent])

                    if not fields[0] == oldLqId:

                        if any(lDev):
                            lDev["answer_pool"] = poolListL
                            lDev["answer_id"] = correctListL
                            lValidList.append(lDev)
                            lDev = {}
                        lDev["question_id"] = lqCount
                        poolListL = [revlaDict[aLemmaSent]]
                        correctListL = []
                        if fields[6] == "1":
                            correctListL.append(revlaDict[aLemmaSent])


                    else:
                        poolListL.append(revlaDict[aLemmaSent])
                        if fields[6] == "1":
                            correctListL.append(revlaDict[aLemmaSent])
                    oldQId = fields[0]
                    oldLqId = fields[0]
            if any(train):
                train["answer_pool"] = poolList
                train["answer_id"] = correctList
                trainList.append(train)
                train = {}

            if any(lTrain):
                lTrain["answer_pool"] = poolListL
                lTrain["answer_id"] = correctListL
                lTrainList.append(lTrain)
                lTrain = {}

            if any(test):
                test["answer_pool"] = poolList
                test["answer_id"] = correctList
                testList.append(test)
                test = {}
            if any(lTest):
                lTest["answer_pool"] = poolListL
                lTest["answer_id"] = correctListL
                lTestList.append(lTest)
                lTest = {}




            if any(dev):
                dev["answer_pool"] = poolList
                dev["answer_id"] = correctList
                validList.append(dev)
                dev = {}
            if any(lDev):
                lDev["answer_pool"] = poolListL
                lDev["answer_id"] = correctListL
                lValidList.append(lDev)
                lDev = {}


    qList = []
    for key, value in qDict.iteritems():
        itemDict = {}
        itemDict["id"] = key
        itemDict["text"] = value
        qList.append(itemDict)
    with open('q.json', 'w') as qJson:
        for q in qList:
            json.dump(q, qJson)
            qJson.write("\n")
    qJson.close()
    qDict.clear()

    w2VSrcFile = open ("w2VSrc", "w")


    lqList = []
    for key, value in lqDict.iteritems():
        itemDict = {}
        itemDict["id"] = key
        itemDict["text"] = value
        values = filter(None, re.split("[!?:\.]+", value))
        for v in values:
            w2VSrcFile.write(v+"\n")
        lqList.append(itemDict)
    with open('lq.json', 'w') as lqJson:
        for lq in lqList:
            json.dump(lq, lqJson)
            lqJson.write("\n")
    lqJson.close()
    lqDict.clear()

    aList = []
    for key, value in aDict.iteritems():
        itemDict = {}
        itemDict["id"] = key
        itemDict["text"] = value

        aList.append(itemDict)
    with open('a.json', 'w') as aJson:
        for a in aList:
            json.dump(a, aJson)
            aJson.write("\n")
    aJson.close()
    aDict.clear()

    laList = []
    for key, value in laDict.iteritems():
        itemDict = {}
        itemDict["id"] = key
        itemDict["text"] = value
        values = filter(None, re.split("[!?:\.]+", value))
        for v in values:
            w2VSrcFile.write(v+"\n")
        laList.append(itemDict)
    with open('la.json', 'w') as laJson:
        laFile = open("la", "w")
        pickle.dump(lansIdxPair, laFile)
        laFile.close()
        for la in laList:
            json.dump(la, laJson)
            laJson.write("\n")
    laJson.close()
    laDict.clear()
    w2VSrcFile.close()

    with open('train.json', 'w') as trainJson:
        for trainItem in trainList:
            json.dump(trainItem, trainJson)
            trainJson.write("\n")
    trainJson.close()

    with open('lTrain.json', 'w') as lTrainJson:
        for lTrainItem in lTrainList:
            json.dump(lTrainItem, lTrainJson)
            lTrainJson.write("\n")
    lTrainJson.close()


    with open('test.json', 'w') as testJson:
        for testItem in testList:
            json.dump(testItem, testJson)
            testJson.write("\n")
    testJson.close()

    with open('lTest.json', 'w') as lTestJson:
        for lTestItem in lTestList:
            json.dump(lTestItem, lTestJson)
            lTestJson.write("\n")
    lTestJson.close()

    with open('valid.json', 'w') as validJson:
        for validItem in validList:
            json.dump(validItem, validJson)
            validJson.write("\n")
    validJson.close()

    with open('lValid.json', 'w') as lValidJson:
        for lValidItem in lValidList:
            json.dump(lValidItem, lValidJson)
            lValidJson.write("\n")
    lValidJson.close()




    debugFile.close()
#    train1File.close()
#    train2File.close()
#    train3File.close()
    trainFile.close()
#    test1File.close()
#    test2File.close()
#    test3File.close()
    testFile.close()
#    valid1File.close()
#    valid2File.close()
#    valid3File.close()
    validFile.close()
    wordFile = open("word","w")
    pickle.dump(wordDict, wordFile)
    wordFile.close()
    lemmaFile = open("lemma","w")
    pickle.dump(lemmaDict, lemmaFile)
    lemmaFile.close()
    revWordFile = open("revWord", "w")
    pickle.dump(revWordDict, revWordFile)
    revWordFile.close()
    revLemmaFile = open("revLemma", "w")
    pickle.dump(revLemmaDict, revLemmaFile)
    revLemmaFile.close()










