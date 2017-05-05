import pickle
import numpy as np
import code

edgeFile = 'results/edgeMatrix.pyobj'
positiveClampFile = 'params/clampwords_positive.txt'
negativeClampFile = 'params/clampwords_negative.txt'
wordlistFile = 'results/consolidate_terms.txt'
classFile = 'results/classification.pyobj'

alpha = 0.3
# This is the "learning rate" / how much of the recalculated classification is
# taken over the original classification. The paper I cite uses 0.3, so we do too.

def load():
    global edgeMatrix, pclamp, nclamp, wordlist

    with open(edgeFile, 'rb') as edge_f:
        edgeMatrix = pickle.load(edge_f)

    with open(positiveClampFile) as pclamp_f:
        pclamp = [word.strip() for word in pclamp_f.readlines()]

    with open(negativeClampFile) as nclamp_f:
        nclamp = [word.strip() for word in nclamp_f.readlines()]

    with open(wordlistFile) as wordlist_f:
        wordlist = [word.strip() for word in wordlist_f.readlines()]

    edgeMatrix = np.array(edgeMatrix).transpose()


def save():
    global classMatrix
    cm = classMatrix.tolist()

    with open(classFile, 'wb') as class_f:
        pickle.dump(cm, class_f)


def buildClassMatrix():
    global classMatrix, wordlist

    classMatrix = []
    for word in wordlist:
        classMatrix.append([0, 0])

    classMatrix = np.array(classMatrix)
    assertClamps()


def assertClamps():
    global classMatrix, wordlist, pclamp, nclamp

    for word in pclamp:
        indx = wordlist.index(word)
        classMatrix[indx] = [1, 0]

    for word in nclamp:
        indx = wordlist.index(word)
        classMatrix[indx] = [0, 1]


def labelProp(check=False):
    global classMatrix, edgeMatrix

    y_prime = alpha * (np.matmul(edgeMatrix, classMatrix)) + (1-alpha) * (classMatrix)

    if check:
        print(checkDiff(classMatrix, y_prime))

    classMatrix = y_prime

    assertClamps()


def checkDiff(m1, m2):
    diff = 0
    for i in range(len(m1)):
        for j in range(len(m1[0])):
            diff += abs(m1[i][j] - m2[i][j])

    return diff


def checkClassification(limit):
    global classMatrix, wordlist

    poswords = []
    negwords = []
    for indx, word in enumerate(wordlist):
        poswords.append((classMatrix[indx][0], word))
        negwords.append((classMatrix[indx][1], word))

    poswords = sorted(poswords, reverse=True)
    negwords = sorted(negwords, reverse=True)

    print('GOOD:')
    for i in range(limit):
        print(poswords[i])
    print('')

    print('UNGOOD:')
    for i in range(1, limit):
        print(poswords[-i])
    print('')

    print('BAD:')
    for i in range(limit):
        print(negwords[i])
    print('')

    print('UNBAD:')
    for i in range(1, limit):
        print(negwords[-i])
    print('')


def iterate(n):
    for i in range(n):
        if i % 100 == 0:
            labelProp(check=True)
        else:
            labelProp()

load()
buildClassMatrix()

code.interact(local=locals())
