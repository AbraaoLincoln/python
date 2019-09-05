import threading
import time
import os
import mmap
import posix_ipc
import sys
import signal
import datetime
from matrixGenerator import MatrixGen

mutex = threading.Lock()
result = []

#Definindo a função func
def func_soma(valor_matriz1, valor_matriz2, results):
    mutex.acquire()
    results.append(valor_matriz1 + valor_matriz2)
    mutex.release()

def func_multiplicacao(valores, results):
    soma = 0
    for i in range( 0, len(valores), 2):
        soma += valores[i] * valores[i + 1]
    #Regiao critica
    mutex.acquire()
    results.append( soma )
    mutex.release()


#Definindo a funcao unroll
def unroll(args, func, method, results):
    threads = []
    valores = []
    count_row = 0
    if args[2] == 0:
        #soma        
        for i in range( len(args[0]) ):
            for j in range( len(args[0][0]) ):
                threads.append(threading.Thread(target=func, args=(args[0][i][j], args[1][i][j], results)))
    else:
        #multiplicao
        for i in range( len(args[0]) ):
            for colunas_matriz2 in range( len(args[1][0]) ):
                for j in range( len(args[1]) ):
                    valores.append(args[0][i][j])
                    valores.append(args[1][j][colunas_matriz2])
                threads.append(threading.Thread(target=func, args=(valores.copy(), results[count_row])))
                valores.clear()
            count_row += 1
        count_row = 0

    for i in range( len(threads) ):
        threads[i].start()


def completeMatriz(rst, qtd_oprt, row):
    for i in range(qtd_oprt):
        matriz = []
        for i in range(row):
            matriz.append([])
        rst.append(matriz.copy())
    
#=========================================================================================================
geradorMatriz = MatrixGen()
matrizes = []
rows = 3
columns = 3
for i in range(5):
    matrizes.append(geradorMatriz.createMatrix(rows,columns))
# matrizes.append([[1,2,3], [3,4,3], [4,3,5]])
# matrizes.append([[1,2,3], [3,4,3], [4,4,4]])
# matrizes.append([[1,2,3], [3,4,3], [4,4,2]])
# # matrizes.append([[19,22,21], [27,34,33], [33,40,41]])
# # matrizes.append([[1,2,3], [3,4,3], [4,4,2]])
# # for teste in matrizes:
# #     print(teste)

qtd_operations = len(matrizes) - 1

while qtd_operations > 0:
    qtd_resultados = 0
    if len(matrizes) % 2 == 0:
        qtd_resultados = int( len(matrizes) / 2 )
        completeMatriz(result, qtd_resultados, rows)
    else:
        qtd_resultados = int (( len(matrizes) - 1 ) / 2)
        completeMatriz(result, qtd_resultados, rows)
        result.append(matrizes[len(matrizes) - 1])

    # for i in range(qtd_resultados):
    #     matriz = []
    #     for i in range(rows):
    #         matriz.append([])
    #     result.append(matriz.copy())
    # if len(matrizes) % 2 != 0:
    #     result.append(matrizes[len(matrizes) - 1])

    threads_unroll = []
    if len(matrizes) % 2 == 0:
        count = 0
        for i in range( 0, len(matrizes), 2 ):
            threads_unroll.append(threading.Thread(target=unroll, args=([ matrizes[i],  matrizes[i+1 ], 1], func_multiplicacao, "thred", result[count])))
            count += 1
    else:
        count = 0
        for i in range( 0, len(matrizes), 2 ):
            if i != ( len(matrizes) - 1 ):
                threads_unroll.append(threading.Thread(target=unroll, args=([ matrizes[i], matrizes[i+1], 1 ], func_multiplicacao, "thred", result[count])))
                count += 1

    for threads_ in threads_unroll:
        threads_.start()

    for threads_ in threads_unroll:
        threads_.join()

    # print("Result")
    # for final_m in result:
    #     print(final_m)

    #Limpeza
    matrizes = result.copy()
    result.clear()
    threads_unroll.clear()
    qtd_operations -= 1

for linha in matrizes[0]:
    print(linha)