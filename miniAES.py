from operator import xor
from math import sqrt

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