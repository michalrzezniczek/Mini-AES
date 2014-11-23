from operator import xor
from math import sqrt

__author__ = 'Michal Rzezniczek'

SboxE = {(0, 0, 0, 0): [1, 1, 1, 0],
         (0, 0, 0, 1): [0, 1, 0, 0],
         (0, 0, 1, 0): [1, 1, 0, 1],
         (0, 0, 1, 1): [0, 0, 0, 1],
         (0, 1, 0, 0): [0, 0, 1, 0],
         (0, 1, 0, 1): [1, 1, 1, 1],
         (0, 1, 1, 0): [1, 0, 1, 1],
         (0, 1, 1, 1): [1, 0, 0, 0],
         (1, 0, 0, 0): [0, 0, 1, 1],
         (1, 0, 0, 1): [1, 0, 1, 0],
         (1, 0, 1, 0): [0, 1, 1, 0],
         (1, 0, 1, 1): [1, 1, 0, 0],
         (1, 1, 0, 0): [0, 1, 0, 1],
         (1, 1, 0, 1): [1, 0, 0, 1],
         (1, 1, 1, 0): [0, 0, 0, 0],
         (1, 1, 1, 1): [0, 1, 1, 1]}
SboxD = {(0, 0, 0, 0): [1, 1, 1, 0],
         (0, 0, 0, 1): [0, 0, 1, 1],
         (0, 0, 1, 0): [0, 1, 0, 0],
         (0, 0, 1, 1): [1, 0, 0, 0],
         (0, 1, 0, 0): [0, 0, 0, 1],
         (0, 1, 0, 1): [1, 1, 0, 0],
         (0, 1, 1, 0): [1, 0, 1, 0],
         (0, 1, 1, 1): [1, 1, 1, 1],
         (1, 0, 0, 0): [0, 1, 1, 1],
         (1, 0, 0, 1): [1, 1, 0, 1],
         (1, 0, 1, 0): [1, 0, 0, 1],
         (1, 0, 1, 1): [0, 1, 1, 0],
         (1, 1, 0, 0): [1, 0, 1, 1],
         (1, 1, 0, 1): [0, 0, 1, 0],
         (1, 1, 1, 0): [0, 0, 0, 0],
         (1, 1, 1, 1): [0, 1, 0, 1]}


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
    output = [[], [], [], []]
    k = 0
    for eee in range(int((sqrt(len(matrix0))))):
        j = 0
        sqrtOfLength = int(sqrt(len(matrix0)))
        for ee in range(sqrtOfLength):
            i = sqrtOfLength * eee
            sum = []
            for e in range(sqrtOfLength):
#                multiply(matrix0[i], matrix1[j])
                sum.append(multiply(matrix0[i], matrix1[j]))
                i += 1
                j += sqrtOfLength
            for e in range(len(sum[0])):
                output[k].append((sum[0][e] + sum[1][e]) % 2)
            k += 1
            j -= len(matrix0) - 1

    return output


def multiply(bits0, bits1):
    polynomialOfReduction = [1, 0, 0, 1, 1, 0, 0]
    output = []
    tmp = []
    for i in range(4):
        tmp.append([0, 0, 0, 0, 0, 0, 0])
        for j, bit in enumerate(bits0):
            if (bit != 0) and (bits1[i] != 0):
                tmp[i][j+i] = bit * bits1[i]

    for i in range(7):
        sum = 0
        for j in range(4):
            sum += tmp[j][i]
        output.append(sum % 2)

    for i in range(3):
        if output[i] != 0:
            for k, bit in enumerate(output):
                tmp2 = polynomialOfReduction[k - i]
                output[k] = (bit + tmp2) % 2

    del output[0:3]
    return output


def ZK(matrix):
    tmp = matrix.pop(2)
    matrix.append(tmp)
    return matrix


def MM(matrix):
    m = [[0, 0, 1, 1], [0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 1]]
    output = multiplyMatrixes(m, matrix)
    return output


#flag E - encrypt; D - decrypt
def Fsbox(matrix, flag):
    output = []
    if flag == 'E':
        for element in matrix:
            output.append(SboxE[tuple(element)])
    elif flag == 'D':
        for element in matrix:
            output.append(SboxD[tuple(element)])
    else:
        return -1
    return output


def keyGenerator(key0):
    keys = []
    key0InMatrix = toMatrix(key0, 4)
    keys.append(key0InMatrix)
    key1 = [[], [], [], []]
    key2 = [[], [], [], []]
    poly = [0, 0, 0, 1]
    for i in range(4):
        tmp = xor(poly[i], key0InMatrix[0][i])
        tmp = xor(tmp, (SboxE[tuple(key0InMatrix[3])])[i])
        key1[0].append(tmp)
    for i in range(4):
        key1[2].append(xor(key0InMatrix[2][i], key1[0][i]))
    for i in range(4):
        key1[1].append(xor(key0InMatrix[1][i], key1[2][i]))
    for i in range(4):
        key1[3].append(xor(key0InMatrix[3][i], key1[1][i]))
    keys.append(key1)

    poly = [0, 0, 1, 0]
    for i in range(4):
        tmp = xor(poly[i], key1[0][i])
        tmp = xor(tmp, (SboxE[tuple(key1[3])])[i])
        key2[0].append(tmp)
    for i in range(4):
        key2[2].append(xor(key1[2][i], key2[0][i]))
    for i in range(4):
        key2[1].append(xor(key1[1][i], key2[2][i]))
    for i in range(4):
        key2[3].append(xor(key1[3][i], key2[1][i]))
    keys.append(key2)
    
    return keys