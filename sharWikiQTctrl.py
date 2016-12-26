import sys
reload(sys)
sys.setdefaultencoding('utf8')

import pickle
import re
import random
import string
import json
from xml.etree import ElementTree as etree
from pycorenlp import StanfordCoreNLP
from xmljson import BadgerFish
from collections import OrderedDict
nlp = StanfordCoreNLP('http://localhost:9000')


def parse(input):
    dbg = open("debug","w")


    output = nlp.annotate(input, properties={
        'annotators': 'tokenize,ssplit,pos',
        'outputFormat': 'xml',
        'timeout': 30000})
    fixed = []
    for o in output:
        fixed.append(o)
    return("".join(fixed))


def lparse(input):
    dbg = open("debug","w")


    output = nlp.annotate(input, properties={
        'annotators': 'tokenize,ssplit,pos,lemma',
        'outputFormat': 'xml',
        'timeout': 30000})
    fixed = []
    for o in output:
        fixed.append(o)
    return("".join(fixed))

def convert_sent(sent):

    new_sent = []
    for term in sent:
        new_sent.append(revWordDict[term])

    return new_sent


def is_ascii(s):
    return all(ord(c) < 128 for c in s)


wordDict = {}
revWordDict = {}
lemmaDict = {}
revLemmaDict = {}


if __name__ == '__main__':

    bf = BadgerFish(dict_type=OrderedDict)


    trainFile = open("WikiQA-train.tsv")
    trainFiles = [trainFile]

    testFile = open("WikiQA-test.tsv")
    testFiles = [testFile]

    validFile = open("WikiQA-dev.tsv")
    validFiles = [validFile]
    fileList = [trainFiles,testFiles,validFiles]


    debugFile = open("debug","w")


    patIdx = re.compile(r"idx_(\d*)", re.DOTALL)


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
    aDic = {}
    revADict = {}
    laDict = {}
    revlaDict = {}
    qIdxPair = {}
    lqIdxPair = {}
    ansIdxPair = {}
    lansIdxPair = {}
#    parseQDict = {}

#    parseADict = {}


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




    qTerms = ['where']
#    qTerms = ['who', 'when', 'where', 'what']
    q_file = open('qTerms', 'rb')
    qTermDic = pickle.load(q_file)


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

                questionRaw = fields[1].lower()

                if questionRaw.split()[0] in qTerms:
#                    tempQTerm = questionRaw.split()[0]
#                    randomTerm = random.choice(qTermDic[tempQTerm])
#                    print "questionRaw b4"
#                    print questionRaw
 #                   questionRaw = questionRaw.replace(tempQTerm, randomTerm)
 #                   print "questionRaw after"
#                    print questionRaw

#only include who when where and what q

                    answerRaw = fields[5].lower()
#                print "questionRaw"
#                print questionRaw
                    parseQXML = etree.fromstring(lparse(str(questionRaw)))
#                lparseQXML =  etree.fromstring(lparse(questionRaw))
                    qTokens = parseQXML.findall(".//token")
#                lqTokens = lparseQXML.findall(".//token")
                    parseAXML = etree.fromstring(lparse(str(answerRaw)))
#                lparseAXML = etree.fromstring(lparse(answerRaw))
                    aTokens = parseAXML.findall(".//token")
#                laTokens = lparseAXML.findall(".//token")
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
                        word = token.find(".//lemma").text
                        qWordList.append(word)
                        if word not in revWordDict.keys():
                            wordKey += 1
                            wordDict[wordKey] = word
                            revWordDict[word] = wordKey
                            outQIdx.append(wordKey)
                        else:
                            existWKey = revWordDict[word]
                            outQIdx.append(existWKey)

#                print "questionLemma"
#                print qLemma


#                for t, token in enumerate(lqTokens):
#                    if t == 0:
#                        qLemma = token.find(".//lemma").text
#                    lemma = token.find(".//lemma").text
#                    qLemmaList.append(lemma)
#                    if lemma not in revLemmaDict.keys():
#                        lemmaKey += 1
#                        lemmaDict[lemmaKey] = lemma
#                        revLemmaDict[lemma] = lemmaKey
#                        outlqIdx.append(lemmaKey)
#                    else:
#                        existLKey = revLemmaDict[lemma]
#                        outlqIdx.append(existLKey)
#                qLemmaSent = " ".join(qLemmaList)

                    for t, token in enumerate(aTokens):
                        word = token.find(".//lemma").text
                        aWordList.append(word)
                        if word not in revWordDict.keys():
                            wordKey += 1
                            wordDict[wordKey] = word
                            revWordDict[word] = wordKey
                            outAIdx.append(wordKey)
                        else:
                            existWKey = revWordDict[word]
                            outAIdx.append(existWKey)




#                for t, token in enumerate(laTokens):
#                    lemma = token.find(".//lemma").text
#                    aLemmaList.append(lemma)
#                    if lemma not in revLemmaDict.keys():
#                        lemmaKey += 1
#                        lemmaDict[lemmaKey] = lemma
#                        revLemmaDict[lemma] = lemmaKey
#                        outlaIdx.append(lemmaKey)
#                    else:
#                        existLKey = revLemmaDict[lemma]
#                        outlaIdx.append(existLKey)
#                aLemmaSent = " ".join(aLemmaList)


#                if qLemmaSent not in revlqDict.keys():
#                    lqCount += 1
#                    lqDict[lqCount] = qLemmaSent
#                    revlqDict[qLemmaSent] = lqCount
#                    lqIdxPair[qCount] = outlqIdx


#                if aLemmaSent not in revlaDict.keys():
#                    laCount += 1
#                    laDict[laCount] = aLemmaSent

#                    revlaDict[aLemmaSent] = laCount
#                    lansIdxPair[aCount] = outlaIdx



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
                                train["bad"] = poolList
                                train["good"] = correctList
                                if correctList != [] : trainList.append(train)
                                train = {}

                            correctList = []
                            poolList = []
                            train['question'] = convert_sent(qWordList)
                            train["question_id"] = qCount
                            qCount = qCount + 1
                    
                            if fields[6]  == "1":
                                correctList.append(aCount)
                                aDic[aCount] = aWordList
                                aCount += 1

                            else:
                                poolList = [aCount]
                                aDic[aCount] = aWordList
                                aCount += 1


                        else:
                        
                            if fields[6] == "1":
#                            print ("fields6 hit")
                                correctList.append(aCount)
                                aDic[aCount] = aWordList
                                aCount += 1
                            else:
                                poolList.append(aCount)
                                aDic[aCount] = aWordList
                                aCount += 1

#                    if not fields[0] == oldLqId:

#                        if any(lTrain):
#                            lTrain["answer_pool"] = poolListL
#                            lTrain["answer_id"] = correctListL
#                            lTrainList.append(lTrain)
#                            lTrain = {}
#                        correctListL = []
#                        lTrain["question_id"] = lqCount
#                        poolListL = [revlaDict[aLemmaSent]]

#                        if fields[6] == "1":
#                            correctListL.append(revlaDict[aLemmaSent])


#                    else:
#                        poolListL.append(revlaDict[aLemmaSent])
#                        if fields[6] == "1":
#                            correctListL.append(revlaDict[aLemmaSent])

                        oldQId = fields[0]
#                    oldLqId = fields[0]


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
                                test["bad"] = poolList
                                test["good"] = correctList
                                if correctList != [] : testList.append(test)
                                test = {}
                            test["question_id"] = qCount
                            qCount = qCount + 1
                            test['question'] = convert_sent(qWordList)
                            poolList = []
                            correctList = []
                            if fields[6] == "1":
                                correctList.append(aCount)
                                aDic[aCount] = aWordList
                                aCount += 1
                            else:
                                poolList = [aCount]
                                aDic[aCount] = aWordList
                                aCount += 1
                        else:
                        
                            if fields[6] == "1":
                                correctList.append(aCount)
                                aDic[aCount] = aWordList
                                aCount += 1
                            else:
                                poolList.append(aCount)
                                aDic[aCount] = aWordList
                                aCount += 1

#                    if not fields[0] == oldLqId:
#                        if any(lTest):
#                            lTest["answer_pool"] = poolListL
#                            lTest["answer_id"] = correctListL
#                            lTestList.append(lTest)
#                            lTest = {}
#                        correctListL = []
#                        lTest["question_id"] = lqCount
#                        poolListL = [revlaDict[aLemmaSent]]
#                        if fields[6] == "1":
#                            correctListL.append(revlaDict[aLemmaSent])


#                    else:
#                        poolListL.append(revlaDict[aLemmaSent])
#                        if fields[6] == "1":
#                            correctListL.append(revlaDict[aLemmaSent])
                        oldQId = fields[0]
#                    oldLqId = fields[0]

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
                                dev["bad"] = poolList
                                dev["good"] = correctList
                                if correctList != [] : validList.append(dev)
                                dev = {}
                            correctList = []
                            poolList = []
                            dev["question_id"] = qCount
                            dev['question'] = convert_sent(qWordList)
                            qCount = qCount + 1

                            if fields[6] == "1":
                                correctList.append(aCount)
                                aDic[aCount] = aWordList
                                aCount += 1
                            else:
                                poolList = [aCount]
                                aDic[aCount] = aWordList
                                aCount += 1


                        else:

                            if fields[6] == "1":
                                correctList.append(aCount)
                                aDic[aCount] = aWordList
                                aCount += 1
                            else:
                                poolList.append(aCount)
                                aDic[aCount] = aWordList
                                aCount += 1

#                    if not fields[0] == oldLqId:

#                        if any(lDev):
#                            lDev["answer_pool"] = poolListL
#                            lDev["answer_id"] = correctListL
#                            lValidList.append(lDev)
#                            lDev = {}
#                        lDev["question_id"] = lqCount
#                        poolListL = [revlaDict[aLemmaSent]]
#                        correctListL = []
#                        if fields[6] == "1":
#                            correctListL.append(revlaDict[aLemmaSent])


#                    else:
#                        poolListL.append(revlaDict[aLemmaSent])
#                        if fields[6] == "1":
#                            correctListL.append(revlaDict[aLemmaSent])
                        oldQId = fields[0]
#                    oldLqId = fields[0]


            if any(train):
                train["bad"] = poolList
                train["good"] = correctList
                if correctList != [] : trainList.append(train)
                train = {}

#            if any(lTrain):
#                lTrain["answer_pool"] = poolListL
#                lTrain["answer_id"] = correctListL
#                lTrainList.append(lTrain)
#                lTrain = {}

            if any(test):
                test["bad"] = poolList
                test["good"] = correctList
                if correctList != [] : testList.append(test)
                test = {}


#            if any(lTest):
#                lTest["answer_pool"] = poolListL
#                lTest["answer_id"] = correctListL
#                lTestList.append(lTest)
#                lTest = {}




            if any(dev):
                dev["bad"] = poolList
                dev["good"] = correctList
                if correctList != [] : validList.append(dev)
                dev = {}


#            if any(lDev):
#                lDev["answer_pool"] = poolListL
#                lDev["answer_id"] = correctListL
#                lValidList.append(lDev)
#                lDev = {}



#    w2VSrcFile = open ("w2VSrc", "w")


#    lqList = []
#    for key, value in lqDict.iteritems():
#        itemDict = {}
#        itemDict["id"] = key
#        itemDict["text"] = value
#        values = filter(None, re.split("[!?:\.]+", value))
#        for v in values:
#            w2VSrcFilehttps://mail.google.com/mail/#inbox.write(v+"\n")
#        lqList.append(itemDict)
#    with open('lq.json', 'w') as lqJson:
#        for lq in lqList:
#            json.dump(lq, lqJson)
#            lqJson.write("\n")
#    lqJson.close()
#    lqDict.clear()


    aList = []
    for key, value in aDic.iteritems():
        itemDict = {}
        itemDict["id"] = key
        itemDict["text"] = convert_sent(value)

        aList.append(itemDict)
    with open('answersQTCtd_where', 'wb') as aJson:

#        for a in aList:
#            json.dump(a, aJson)
#            aJson.write("\n")

        pickle.dump(aList, aJson)

    aJson.close()
    aDic.clear()


#    laList = []
#    for key, value in laDict.iteritems():
#        itemDict = {}
#        itemDict["id"] = key
#        itemDict["text"] = value
#        values = filter(None, re.split("[!?:\.]+", value))
#        for v in values:
#            w2VSrcFile.write(v+"\n")
#        laList.append(itemDict)
#    with open('la.json', 'w') as laJson:
#        laFile = open("la", "w")
#        pickle.dump(lansIdxPair, laFile)
#        laFile.close()
#        for la in laList:
#            json.dump(la, laJson)
#            laJson.write("\n")
#    laJson.close()
#    laDict.clear()
#    w2VSrcFile.close()


    with open('trainQTCtd_where', 'wb') as train:
        pickle.dump(trainList, train)
    train.close()

    with open('testQTCtd_where', 'wb') as test:
        pickle.dump(testList, test)
    test.close()

    with open('devQTCtd_where', 'wb') as dev:
        pickle.dump(validList, dev)
    dev.close()




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
    wordFile = open("wordQTCtd","wb")
    pickle.dump(wordDict, wordFile)
    wordFile.close()

    revWordFile = open("revWordQTCtd", "wb")
    pickle.dump(revWordDict, revWordFile)
    revWordFile.close()










