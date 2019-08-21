import threading
import time
import os

mutex = threading.Lock()
result = []

#Definindo a função func
def func_soma(valor_matriz1, valor_matriz2):
    global result
    #Regiao critica
    mutex.acquire()
    result.append(valor_matriz1 + valor_matriz2)
    mutex.release()

def func_multiplicacao(valor1_matriz1_linha, valor2_matriz1_linha, valor1_matriz2_coluna, valor2_matriz2_coluna):
    global result
    #Regiao critica
    mutex.acquire()
    result.append(( valor1_matriz1_linha * valor1_matriz2_coluna ) + ( valor2_matriz1_linha * valor2_matriz2_coluna))
    mutex.release()

#Definindo a funcao unroll
def unroll(args, func, method, results):

    if args[2] == 0:
        #soma
        func1 = threading.Thread(target=func, args=(args[0][0][0], args[1][0][0]))
        func2 = threading.Thread(target=func, args=(args[0][0][1], args[1][0][1]))
        func3 = threading.Thread(target=func, args=(args[0][1][0], args[1][1][0]))
        func4 = threading.Thread(target=func, args=(args[0][1][1], args[1][1][1]))
    else:
        #multiplicao
        func1 = threading.Thread(target=func, args=(args[0][0][0], args[0][0][1], args[1][0][0], args[1][1][0]))
        func2 = threading.Thread(target=func, args=(args[0][0][0], args[0][0][1], args[1][0][1], args[1][1][1]))
        func3 = threading.Thread(target=func, args=(args[0][1][0], args[0][1][1], args[1][0][0], args[1][1][0]))
        func4 = threading.Thread(target=func, args=(args[0][1][0], args[0][1][1], args[1][0][1], args[1][1][1]))

    #iniciando as threads
    func1.start()
    func2.start()
    func3.start()
    func4.start()

#Criando as matrizes
matriz1 = [[1,2], [3,4]]
matriz2 = [[1,2], [3,4]]

#Imprimindo as matrizes antes da operacao
print("Matrizes iniciais")
print("Matriz1:")
for i in range(len(matriz1)):
    for j in range(len(matriz1[i])):
        print(matriz1[i][j], " ",end='')
    print()
print("Matriz2:")
for i in range(len(matriz1)):
    for j in range(len(matriz1[i])):
        print(matriz1[i][j], " ",end='')
    print()

#chama unroll para fazer a soma
unroll([matriz1, matriz2, 0], func_soma, "thred", result)
#Imprindo o resultado da operacao
print("Resultado da soma:")
for i in range(len(result)):
    print(result[i], " ",end="")
    if i == 1:
        print()
result.clear()
print()
#chama unroll para fazer a a multiplicacao
unroll([matriz1, matriz2, 1], func_multiplicacao, "thred", result)
#Imprindo o resultado da operacao
print("Resultado da multiplicao:")
for i in range(len(result)):
    print(result[i], " ", end="")
    if i == 1:
        print()
print()