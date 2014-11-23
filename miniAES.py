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
            output[i].append(xor(j, matrix1[i][k]))
            k += 1
    return output


def multiplyMatrixes(matrix0, matrix1):
    for eee in range(int((sqrt(len(matrix0))))):
        j = 0
        sqrtOfLength = int(sqrt(len(matrix0)))
        for ee in range(sqrtOfLength):
            i = sqrt(len(matrix0)) * eee
            for e in range(sqrtOfLength):
                #sum += multiply(matrix0[i], matrix1[j])
                i += 1
                j += sqrtOfLength
            j -= len(matrix0) - 1