# !/usr/bin/env python3

import socket
import sys
import threading
import random

def servirPorSiempre(socketTcp, listaconexiones):
    try:
        while True:
            client_conn, client_addr = socketTcp.accept()
            print("Conectado a", client_addr)
            listaconexiones.append(client_conn)
            thread_read = threading.Thread(target=recibir_datos, args=[client_conn, client_addr])
            thread_read.start()
            gestion_conexiones(listaConexiones)
    except Exception as e:
        print(e)

def gestion_conexiones(listaconexiones):
    for conn in listaconexiones:
        if conn.fileno() == -1:
            listaconexiones.remove(conn)
    print("hilos activos:", threading.active_count())
    print("enum", threading.enumerate())
    print("conexiones: ", len(listaconexiones))
    print(listaconexiones)


def recibir_datos(conn, addr):
    try:
        cur_thread = threading.current_thread()
        print("Recibiendo datos del cliente {} en el {}".format(addr, cur_thread.name))
        while True:
            data = conn.recv(1024)
            if not data:
                print("Fin con el {}.".format(cur_thread.name))
                break
            coordenadas = str(data.decode())
            print("Las coordenadas que recibi son:", coordenadas)
            fila = int(coordenadas[0])
            columna = int(coordenadas[2])
            if matriz[fila][columna] == "X":
                numero = 1
                print("El usuario perdió\nEnviando resultado...")
            elif matriz[fila][columna] == "0":
                numero = 0
                print("El usuario sigue jugando\nEnviando resultado...")
            response = str(numero)
            conn.sendall(response.encode())
    except Exception as e:
        print(e)
    finally:
        conn.close()



listaConexiones = []
host, port, numConn = sys.argv[1:4]

if len(sys.argv) != 4:
    print("usage:", sys.argv[0], "<host> <port> <num_connections>")
    sys.exit(1)

serveraddr = (host, int(port))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
    TCPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    TCPServerSocket.bind(serveraddr)
    TCPServerSocket.listen(int(numConn))
    print("El servidor TCP está disponible y en espera de solicitudes")
    print("El tablero con el que jugaran los clientes será el siguiente:")
    tam = "9"
    matriz = [['' for j in range(9)] for i in range(9)]  # inicializar matriz de 4 x 4 con 9 minas
    minas = 0
    casillas_vacias = 0
    i = 0
    for i in range(9):
        j = 0
        for j in range(9):
            num = random.randint(0, 1)
            if num == 1 and minas < 40:
                matriz[i][j] = "X"
                minas += 1
            elif 0 == num:
                matriz[i][j] = str(num)
                casillas_vacias += 1
            elif num == 1 and minas >= 40:
                num = 0
                casillas_vacias += 1
                matriz[i][j] = str(num)
            print(matriz[i][j], end=" ")
        print()

    servirPorSiempre(TCPServerSocket, listaConexiones)