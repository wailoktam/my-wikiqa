#!/usr/bin/env python
# coding: utf-8
import pickle
import re
import csv

if __name__ == '__main__':
    dataFile = open('WikiQASent.pos.ans.tsv')

    result = {}

    question_words = ['how', 'what', 'who', 'which', 'when', 'where']

    for q in question_words:
        result[q] = set()

    reader = csv.reader(dataFile, delimiter = '	')
    next(reader)

    for row in reader:
        
        question = row[1].lower()
        awSet = set()
        if row[6]: awSet.add(row[6])
        if row[7]: awSet.add(row[7])
        if row[8]: awSet.add(row[8])

        q_term = question.split(' ')[0]

        inputed = False

        for q in question_words:
            if q_term == q:
                result[q] = result[q].union(awSet)
                inputed = True

        if not inputed: print(row)

    for q in question_words:
        print(q)
        print(len(result[q]))
    

    f = open('qTerms', 'wb')
    pickle.dump(result, f)


