#!/usr/bin python3

import socket
import time
import os

HOST = "127.0.0.1"  # Hostname o  dirección IP del servidor
PORT = 65432  # Puerto del servidor
buffer_size = 1024

def matriz_inicial(tam):
    if tam == "0":
        tama = 4
    elif tam == "1":
        tama = 6
    elif tam == "2":
        tama = 9
    matriz = [['' for j in range(tama)] for i in range(tama)]
    i = 0
    for i in range(tama):
        j = 0
        for j in range(tama):
            matriz[i][j] = "-"
            print(matriz[i][j], end=" ")
        print()
    return matriz


def imprimir_matriz(fila, col, valor, tam, matriz):
    if tam == "0":
        tama = 4
    elif tam == "1":
        tama = 6
    elif tam == "2":
        tama = 9
    matriz[fila][col] = valor
    for i in range(tama):
        j = 0
        for j in range(tama):
            print(matriz[i][j], end=" ")
        print()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:
    TCPClientSocket.connect((HOST, PORT))
    print(f"Conexion lograda con: {HOST}, {PORT}")
    print("Soy el cliente numero 1")
    matriz = matriz_inicial("2")
    while True:
        lectura = input("Ingresa tus coordenadas de juego: ")
        list = lectura.split(",")
        coordenadas = str(lectura)
        TCPClientSocket.sendall(coordenadas.encode())
        print("Enviando coordenadas...")
        time.sleep(2)
        os.system("cls")
        #!print("Esperando una respuesta...")
        data = TCPClientSocket.recv(buffer_size)
        #!print(data)
        numero = int(data.decode())
        #!print("Recibido,", numero, " de", TCPClientSocket.getpeername())
        if numero == 1:
            print("Usted ha perdido ya que eligio una mina")
            imprimir_matriz(int(list[0]), int(list[1]), "X", "2", matriz)
            
            break
        else:
            print("Buena eleccion! Sigue jugando")
            imprimir_matriz(int(list[0]), int(list[1]), "0", "2", matriz)
            
