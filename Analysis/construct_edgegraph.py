import pickle
import code

countMatrixFile = 'results/countMatrix.pyobj'
edgeMatrixFile = 'results/edgeMatrix.pyobj'

with open(countMatrixFile, 'rb') as countMatrix_f:
    countMatrix = pickle.load(countMatrix_f)

edgeMatrix = []
for i in range(len(countMatrix)):
    r = []
    for j in range(len(countMatrix)):
        r.append(0)
    edgeMatrix.append(r)

for j in range(len(countMatrix)):
    sumWeights = 0
    for k in range(len(countMatrix)):
        if k != j:
            sumWeights += countMatrix[k][j]
    for i in range(len(countMatrix)):
        if i != j:
            edgeMatrix[i][j] = countMatrix[i][j] / sumWeights

with open(edgeMatrixFile, 'wb') as edgeMatrix_f:
    pickle.dump(edgeMatrix, edgeMatrix_f)

code.interact(local=locals())
