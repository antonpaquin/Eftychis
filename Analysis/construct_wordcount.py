from elasticsearch import Elasticsearch
import pickle
import json
import os
import code

es = Elasticsearch()

countMatrix = []
countMatrixFile = 'results/countMatrix.pyobj'

wordlist = []
wordlistFile = 'results/consolidate_terms.txt'

reporting = True

def get_query(word1, word2):
    termFilter = [{ 'term': { 'content': word1 } }]
    if word1 != word2:
        termFilter.append( { 'term': { 'content': word2 } } )
    return {'query': {'bool': {'filter': termFitler } } }

def loadMatrix():
    global countMatrix, wordlist

    # if the pickled matrix file exists, load it
    if os.path.isfile(countMatrixFile):
        with open(countMatrixFile, 'rb') as matrix_f:
            countMatrix = pickle.read(matrix_f)
    # else, initialize with -1's
    else:
        countMatrix = []
        for i in range(len(wordlist)):
            r = []
            for j in range(len(wordlist)):
                r.append(-1)
            countMatrix.append(r)

    # read the wordlist
    # if there are new entries, extend the rows and columns for each
    assert len(countMatrix) == len(countMatrix[0])
    if len(countMatrix) < len(wordlist):
        extendSize = len(wordlist) - len(countMatrix)
        for i in range(len(countMatrix)):
            for j in range(extendSize):
                countMatrix[i].append(-1)
        for i in range(extendSize):
            r = []
            for j in range(extendSize + len(countMatrix)):
                r.append(-1)
            countMatrix.append(r)

def saveMatrix():
    global countMatrix

    with open(countMatrixFile, 'wb') as matrix_f:
        pickle.dump(countMatrix, matrix_f)

def loadWordlist():
    global wordlist

    with open(wordlistFile) as list_f:
        lines = list_f.readlines()

    wordlist = [line.strip() for line in lines]

def uncalculatedEdges():
    global countMatrix, wordlist, reporting

    # Go through matrix, find -1's
    # if there is, check the word co-occurrence and put it at (i,j) and (j,i)
    for i in range(len(countMatrix)):
        for j in range(len(countMatrix)):
            if countMatrix[i][j] == -1:
                countMatrix[i][j] = queryEdge(getWord(i), getWord(j))
                countMatrix[j][i] = countMatrix[i][j] # it's undirected

        if reporting:
            print('{} / {}'.format(str(i), str(len(countMatrix)) ) )

def getWord(indx):
    global wordlist
    if len(wordlist) == 0:
        loadWordList()
    return wordlist[indx]

def queryEdge(word1, word2):
    return es.count(
        index='twdata',
        doc_type='tweet',
        body=get_query(word1, word2)
    )

code.interact(local=locals())
