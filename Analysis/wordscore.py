import pickle
import statistics

classFile = 'results/classification.pyobj'
wordlistFile = 'results/consolidate_terms.txt'
wordscoreFile = 'results/wordscores.pyobj'

with open(classFile, 'rb') as class_f:
    classification = pickle.load(class_f)

with open(wordlistFile) as word_f:
    words = [word.strip() for word in word_f.readlines()]

scores = [c[0] for c in classification if (c[0] != 1 and c[0] != 0)] # filter out the clamps
scoreMean = statistics.mean(scores)
scoreStdev = statistics.stdev(scores)

scores = [c[0] for c in classification]

scoreZ = [(score - scoreMean) / scoreStdev for score in scores]

wordscores = {}
for word, score in zip(words, scoreZ):
    wordscores[word] = score

with open(wordscoreFile, 'wb') as wordscore_f:
    pickle.dump(wordscores, wordscore_f)
