import pickle

wordscoreFile = 'results/wordscores.pyobj'

with open(wordscoreFile, 'rb') as wordscore_f:
    wordscore = pickle.load(wordscore_f)

def tweetScore(tweetWords):
    score = 0
    for word in tweetWords:
        if word in wordscore:
            score += wordscore[word]
    return score
