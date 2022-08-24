# For this part of the assignment, please implement your own code for all computations,
# Do not use inbuilt functions like fft from either numpy, opencv or other libraries
import math
import numpy as np

class Dft:
    def __init__(self):
        pass

    def forward_transform(self, matrix):
        """Computes the forward Fourier transform of the input matrix
        takes as input:
        matrix: a 2d matrix
        returns a complex matrix representing fourier transform"""
        r, c = matrix.shape
        res_matrix = np.zeros((r,c), dtype = complex)
        for u in range(r):
            for v in range(c):
                for i in range(r):
                    for j in range(c):
                        res_matrix[u][v] += matrix[i][j]*complex(math.cos(2*math.pi*(u*i+v*j)/r), -1*math.sin(2*math.pi*(u*i+v*j)/r))
        return res_matrix

    def inverse_transform(self, matrix):
        """Computes the inverse Fourier transform of the input matrix
        You can implement the inverse transform formula with or without the normalizing factor.
        Both formulas are accepted.
        takes as input:
        matrix: a 2d matrix (DFT) usually complex
        returns a complex matrix representing the inverse fourier transform"""
        r, c = matrix.shape
        res_matrix = np.zeros((r,c), dtype = complex)
        for u in range(r):
            for v in range(c):
                for i in range(r):
                    for j in range(c):
                        res_matrix[u][v] += matrix[i][j]*complex(math.cos(2*math.pi*(u*i+v*j)/r), math.sin(2*math.pi*(u*i+v*j)/r))
        return res_matrix

    def magnitude(self, matrix):
        """Computes the magnitude of the input matrix (iDFT)
        takes as input:
        matrix: a 2d matrix
        returns a matrix representing magnitude of the complex matrix"""
        r, c = matrix.shape
        res_matrix = np.zeros((r,c))
        for i in range(r):
                    for j in range(c):
                        res_matrix[i][j] = math.sqrt(math.pow(np.real(matrix[i][j]),2) + math.pow(np.imag(matrix[i][j]),2))
        return res_matrix
