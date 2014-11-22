__author__ = 'Michal Rzezniczek'


def toMatrix(text, howManyBits):
    i = 0
    j = 0
    stop = len(text) / howManyBits
    output = [[]]
    for letter in text:
        if j == stop:
            j = 0
            i += 1
            output.append([])
        output[i].append(letter)
        j += 1
    return output


def add(matrix0, matrix1):
    output = []
    for i in range(len(matrix0)):
        k = 0
        output.append([])
        for j in matrix0[i]:
            output[i].append(j + matrix1[i][k])
            k += 1
    return output