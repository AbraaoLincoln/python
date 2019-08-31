import threading
import time
import os
import mmap
import posix_ipc
import sys
import signal

index = 0
mutex = threading.Lock()
result = []

#Definindo a função func
def func_soma(valor_matriz1, valor_matriz2, modoDeEscrita=None):
    global result
    global index
    #Regiao critica
    if modoDeEscrita == None:
        #Usando threads
        mutex.acquire()
        result.append(valor_matriz1 + valor_matriz2)
        mutex.release()
    else:
        #usando fork + memoria compartilhada
        valor = valor_matriz1 + valor_matriz2
        mamoria_map = None
        memoria = posix_ipc.SharedMemory("shm")
        mamoria_map = mmap.mmap(memoria.fd, memoria.size)
        memoria.close_fd()
        semaforo = posix_ipc.Semaphore("semafa")
        #Regiao critica
        semaforo.acquire()
        mamoria_map.seek(index * 4)
        mamoria_map.write(valor.to_bytes(4,byteorder='big'))
        semaforo.release()

def func_multiplicacao(valores, modoDeEscrita=None):
    global result
    global index
    soma = 0
    for i in range( 0, len(valores), 2):
        soma += valores[i] * valores[i + 1]
    #Regiao critica
    if modoDeEscrita == None:
        #usando thread
        mutex.acquire()
        result.append( soma )
        mutex.release()
    else:
        #usando fork + memoria compartilhada
        mamoria_map = None
        memoria = posix_ipc.SharedMemory("shm")
        mamoria_map = mmap.mmap(memoria.fd, memoria.size)
        memoria.close_fd()
        semaforo = posix_ipc.Semaphore("semafa")
        #Regiao critica
        semaforo.acquire()
        mamoria_map.seek(index * 4)
        mamoria_map.write(soma.to_bytes(4,byteorder='big'))
        semaforo.release()

#Definindo a funcao unroll
def unroll(args, func, method, results):
    global index
    if method == "thred":
        #Modo thread
        threads = []
        valores = []
        if args[2] == 0:
            #soma        
            for i in range( len(args[0]) ):
                for j in range( len(args[0][0]) ):
                    threads.append(threading.Thread(target=func, args=(args[0][i][j], args[1][i][j])))
        else:
            #multiplicao
            for i in range( len(args[0]) ):
                for colunas_matriz2 in range( len(args[1][0]) ):
                    for j in range( len(args[1]) ):
                        valores.append(args[0][i][j])
                        valores.append(args[1][j][colunas_matriz2])
                    threads.append(threading.Thread(target=func, args=([valores.copy()])))
                    valores.clear()

        for i in range( len(threads) ):
            threads[i].start()
    else:
        #Modo multiporcessos
        i = 0
        j = 0
        #tamanho_da_memoria = len( args[0][0] ) * len( args[1] ) * 4
        
        #pid_processo_pai = os.getpid()
        processoPaiPrecisaMaisUmFilho = True

        while processoPaiPrecisaMaisUmFilho:
            if i != ( len(args[0]) ):
                pid = os.fork()
                if pid == 0:
                    if args[2] == 0:
                        func(args[0][i][j], args[1][i][j], "fork")
                    else:
                        valores = []
                        for x in range( len(args[0][0]) ):
                            valores.append(args[0][i][x])
                            valores.append(args[1][x][j])
                        func(valores, "fork")
                    os.kill(os.getpid(), signal.SIGKILL)
                else:
                    if j < ( len(args[0][0]) - 1 ):
                        j += 1
                    else:
                        i += 1
                        j = 0
                    index += 1
            else:
                time.sleep(0.5)
                processoPaiPrecisaMaisUmFilho = False
                break

        
        index = 0

#Prints
def printMatriz(matriz):
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            print(matriz[i][j], " ",end='')
        print()
def printResult(result):
    for i in range(len(result)):
        print(result[i], " ",end="")
        if ( i + 1 ) % len(matriz1[0]) == 0:
            print()
    result.clear()
def printSHM():
    #Imprimir os valores que estão na memoria compartilhada
    memoria_mapeada.seek(0)
    for i in range((len(matriz1) * len(matriz2[0]))):
        valorFinal = memoria_mapeada.read(4)
        valor = int.from_bytes(valorFinal, byteorder='big')
        print(str(valor), " ", end='')
        if ( i + 1 ) % len(matriz1) == 0:
            print()
    #======================================================
#Criando as matrizes
matriz1 = [[1,2,3], [3,4,3], [4,3,5]]
matriz2 = [[1,2,3], [3,4,3], [4,4,4]]
#Imprimindo as matrizes antes da operacao
print("Matrizes iniciais")
print("Matriz1:")
printMatriz(matriz1)
print("Matriz2:")
printMatriz(matriz2)

user_answer = input("Modo do paralismo: ");

if user_answer == "thred":
    #Usando o mode thread
    #chama unroll para fazer a soma
    unroll([matriz1, matriz2, 0], func_soma, "thred", result)
    #Imprindo o resultado da operacao
    print("Resultado da soma:")
    printResult(result)
    #chama unroll para fazer a a multiplicacao
    unroll([matriz1, matriz2, 1], func_multiplicacao, "thred", result)
    #Imprindo o resultado da operacao
    print("Resultado da multiplicao:")
    printResult(result)
elif user_answer == "fork":
    #Usando o mode fork + memoria compartilhada
    tamanho_da_memoria = len( matriz1 ) * len( matriz2[1] ) * 4
    memoria_mapeada = None
    #Memoria compartilhada
    memoria_compartilhada = posix_ipc.SharedMemory("shm", flags = posix_ipc.O_CREAT, mode = 0o777, size = tamanho_da_memoria)
    memoria_mapeada = mmap.mmap(memoria_compartilhada.fd, memoria_compartilhada.size)
    memoria_compartilhada.close_fd()
    #memoria_mapeada.seek(0)
    #Semaforos
    semaforo = posix_ipc.Semaphore("semafa", flags = posix_ipc.O_CREAT, mode = 0o777,  initial_value=1)
    #Usando o fork para fazer a soma
    unroll([matriz1, matriz2, 0], func_soma, "fork", result)
    #Imprimir os valores que estão na memoria compartilhada
    print("Resultado da soma:")
    printSHM()
    #Usando o fork para fazer a multiplicação
    unroll([matriz1, matriz2, 1], func_multiplicacao, "fork", result)
    #Imprimir os valores que estão na memoria compartilhada
    print("Resultado da multiplicação:")
    printSHM()
    #Fechando as coisas
    memoria_mapeada.close()
    posix_ipc.unlink_shared_memory("shm")
    semaforo.close()
else:
    print("Opção invalida!")