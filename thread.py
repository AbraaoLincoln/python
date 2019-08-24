import threading
import time
import os
import mmap
import posix_ipc
import sys

mutex = threading.Lock()
result = []

#Definindo a função func
def func_soma(valor_matriz1, valor_matriz2, modoDeEscrita=None):
    global result
    #Regiao critica
    if modoDeEscrita == None:
        mutex.acquire()
        result.append(valor_matriz1 + valor_matriz2)
        mutex.release()
    else:
        valor = valor_matriz1 + valor_matriz2
        #print("valor", valor)
        mamoria_map = None
        memoria = posix_ipc.SharedMemory("shm")
        mamoria_map = mmap.mmap(memoria.fd, memoria.size)
        memoria.close_fd()
        semaforo_fun = posix_ipc.Semaphore("semafa")
        #Regiao critica
        semaforo_fun.acquire()
        mamoria_map.write(valor.to_bytes(4,byteorder='big'))
        semaforo_fun.release()

def func_multiplicacao(valores, modoDeEscrita=None):
    global result
    soma = 0
    #print("valore: ", len(valores), "--", valores)
    for i in range( 0, len(valores), 2):
        soma += valores[i] * valores[i + 1]
    #Regiao critica
    mutex.acquire()
    result.append( soma )
    mutex.release()
    #print("result: ", result)

#Definindo a funcao unroll
def unroll(args, func, method, results):

    if method == "thred":
        funcoes = []
        valor_coluna_linha = []
        valores = []
        if args[2] == 0:
            #soma
            # func1 = threading.Thread(target=func, args=(args[0][0][0], args[1][0][0]))
            # func2 = threading.Thread(target=func, args=(args[0][0][1], args[1][0][1]))
            # func3 = threading.Thread(target=func, args=(args[0][1][0], args[1][1][0]))
            # func4 = threading.Thread(target=func, args=(args[0][1][1], args[1][1][1]))
        
            for i in range( len(args[0]) ):
                for j in range( len(args[0][0]) ):
                    funcoes.append(threading.Thread(target=func, args=(args[0][i][j], args[1][i][j])))
        else:
            #multiplicao
            # func1 = threading.Thread(target=func, args=(args[0][0][0], args[0][0][1], args[1][0][0], args[1][1][0]))
            # func2 = threading.Thread(target=func, args=(args[0][0][0], args[0][0][1], args[1][0][1], args[1][1][1]))
            # func3 = threading.Thread(target=func, args=(args[0][1][0], args[0][1][1], args[1][0][0], args[1][1][0]))
            # func4 = threading.Thread(target=func, args=(args[0][1][0], args[0][1][1], args[1][0][1], args[1][1][1]))

            for i in range( len(args[0]) ):
                for colunas_matriz1 in range( len(args[1][0]) ):
                    for j in range( len(args[1]) ):
                        valores.append(args[0][i][j])
                        valores.append(args[1][j][colunas_matriz1])
                    funcoes.append(threading.Thread(target=func, args=([valores.copy()])))
                    valores.clear()

        #iniciando as threads
        # func1.start()
        # func2.start()
        # func3.start()
        # func4.start()
        for i in range( len(funcoes) ):
            funcoes[i].start()
    else:
        i = 0
        j = 0
        pid_processo_pai = os.getpid()

        memoria_mapeada = None

        memoria_compartilhada = posix_ipc.SharedMemory("shm", flags = posix_ipc.O_CREAT, mode = 0o777, size = 100)
        memoria_mapeada = mmap.mmap(memoria_compartilhada.fd, memoria_compartilhada.size)
        memoria_compartilhada.close_fd()
        semaforo = posix_ipc.Semaphore("semafa", flags = posix_ipc.O_CREAT, mode = 0o777,  initial_value=1)
        semaforo_end = posix_ipc.Semaphore("end", flags = posix_ipc.O_CREAT,mode = 0o777, initial_value = 0)
        memoria_mapeada.seek(0)
        #func(args[0][i][j], args[1][i][j], "fork")
        pid = os.fork()
        print("pid: ", pid, "pid_pai: ", pid_processo_pai)
        while pid == 0:
            if i != ( len(args[0]) ) and j != ( len(args[0][0]) ):
                func(args[0][i][j], args[1][i][j], "fork")
                i += 1
                j += 1
                pid = os.fork()
                print("pid: ", pid)
            else:
                time.sleep(2)
                semaforo_end.release()
                break

        if pid_processo_pai == os.getpid():
            semaforo_end.acquire()
            for i in range((len(args[0]) * len(args[0][0]))):
                memoria_mapeada.seek(0)
                valorFinal = memoria_mapeada.read(4)
                valor = int.from_bytes(valorFinal, byteorder='big')
                print(str(valor))
            print("Fechando as coisas")
            memoria_mapeada.close()
            posix_ipc.unlink_shared_memory("shm")
            semaforo.close()
            semaforo_end.close()
            sys.exit(0)

#Criando as matrizes
matriz1 = [[1,2,3], [3,4,3], [4,4,4]]
matriz2 = [[1,2,3], [3,4,3], [4,4,4]]

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
unroll([matriz1, matriz2, 0], func_soma, "fork", result)
#Imprindo o resultado da operacao
print("Resultado da soma:")
for i in range(len(result)):
    print(result[i], " ",end="")
    if ( i + 1 ) % len(matriz1[0]) == 0:
        print()
result.clear()
print()
#chama unroll para fazer a a multiplicacao
unroll([matriz1, matriz2, 1], func_multiplicacao, "thred", result)
#Imprindo o resultado da operacao
print("Resultado da multiplicao:")
for i in range(len(result)):
    print(result[i], " ", end="")
    if ( i + 1 ) % len(matriz1[0]) == 0:
        print()
print()