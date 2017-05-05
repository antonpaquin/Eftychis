import pickle

wordscoreFile = 'results/wordscores.pyobj'

with open(wordscoreFile, 'rb') as wordscore_f:
    wordscore = pickle.load(wordscore_f)

def tweetScore(tweetWords):
    score = 0
    count = 1
    for word in tweetWords:
        if word in wordscore:
            score += wordscore[word]
            count += 1
    return score / count
