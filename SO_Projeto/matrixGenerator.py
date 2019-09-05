import random

class MatrixGen:

    # def __init__(self):
    #     # self.size = sizeOfMatrix

    def createMatrix(self, rows, columns):
        matrix = []
        for i in range(rows):
            row = []
            for j in range(columns):
                row.append(random.randint(10, 99))
            matrix.append(row.copy())

        return matrix



#Testes
# m = MatrixGen()
# m1 = m.createMatrix(4,2)
# print(m1)
# m2 =m.createMatrix(3,3)
# print(m2)
# print(m1)

# lista = []

# for i in range(3):
#     lista.append(m.createMatrix())

# for i in range(3):
#     print(lista[i])