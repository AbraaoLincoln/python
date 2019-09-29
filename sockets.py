import socket #importa a biblioteca de socket
import time


port = 12000 #porta que vai ser usada pelo.

#socket.AF_INET This constant represent the address (and protocol) families, used for the first argument to socket()
	#AF_INET is an address family that is used to designate the type of addresses that your socket can communicate with (in this case, Internet Protocol v4 addresses)
	#AF_INET6 for Internet Protocol v6 addresses.
#socket.SOCK_STREAM These constants represent the socket types, used for the second argument to socket().
#SOCK_STREAM: Esse tipo usa TCP, portanto todas as caracteristicas do do tcp são usadas.
#SOCK_DGRAM: Esse tipo usa UDP, portanto, não é orientado à conexão,

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #Return True if socket is in blocking mode, False if in non-blocking.
    #socket.getblocking()

    #Set blocking or non-blocking mode of the socket: if flag is false, the socket is set to non-blocking, else to blocking mode.
    s.setblocking(0)

    #Bind the socket to address. The socket must not already be bound.
    s.bind(('', port)) #Associa o socket a um endereço socket e uma porta(host, porta).

    #Enable a server to accept connections
    #parametro inteiro >= 0
    #t specifies the number of unaccepted connections that the system will allow before refusing new connections. If not specified, a default reasonable value is chosen.
    s.listen(5) #Coloca o socket para aguardar conexões

    while True:

        try:
            #Accept a connection. The socket must be bound to an address and listening for connections.
            #he return value is a pair (conn, address).
            #conn is a new socket object usable to send and receive data on the connection(The newly created socket is non-inheritable.).
            #address is the address bound to the socket on the other end of the connection.
            conn, info = s.accept()

            #recv(bufsize) = Receive data from the socket. The return value is a bytes object representing the data received.
            #The maximum amount of data to be received at once is specified by bufsize.
            #For best match with hardware and network realities, the value of bufsize should be a relatively small power of 2, for example, 4096.
            data = conn.recv(1024)

        except BlockingIOError:
            print("waiting for connections")
            time.sleep(1)

# /**
#  * Principais funções para escrever programas com sockets
#  */
#
# getaddrinfo()  // Traduz nomes para endereços sockets
# socket()       // Cria um socket e retorna o descritor de arquivo
# bind()         // Associa o socket a um endereço socket e uma porta
# connect()      // Tenta estabelecer uma conexão com um socket
# listen()       // Coloca o socket para aguardar conexões
# accept()       // Aceita uma nova conexão e cria um socket
# send()         // caso conectado, transmite mensagens ao socket
# recv()         // recebe as mensagens através do socket
# close()        // desaloca o descritor de arquivo
# shutdown()     // desabilita a comunicação do socket