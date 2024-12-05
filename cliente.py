import socket
import sys
import pickle
import threading



class HiloEscuchador(threading.Thread):

    def __init__(self, _socket):
        super(HiloEscuchador, self).__init__()
        self._socket = _socket
        self.data = None

    def run(self):
        self.data = None
        self.data = self._socket.recv(4096).decode('utf-8')
        print(self.data)
        #self.data = pickle.loads(self._socket.recv(4096))
        print("Hilo escuchador ha recibido datos")


def esperar_iniciar():
    while True:
        data = _socket.recv(4096).decode('utf-8')
        print(data)
        if "desea iniciar el juego" in data:
            respuesta = input()
            _socket.send(bytes(respuesta, 'utf-8'))
            data = _socket.recv(4096).decode('utf-8')
            print(data)
            if "ok" in data:
                jugar = True
                break


if __name__ == '__main__':
    jugar = False
    _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        _socket.connect(("localhost", 5000))
    except:
        print("Imposible conectar.")
        sys.exit()

    print("Conectado satisfactoriamente.\n")

    data = _socket.recv(4096).decode('utf-8')
    print('server dice: ', data)

    if "esta lleno" in data or "ya se esta jugando una partida" in data:
        _socket.close()
        sys.exit()
    if "Bienvenido" in data:
        data = input("\n: ")
        _socket.send(bytes(data, 'utf-8'))
        resp = _socket.recv(4096).decode('utf-8')
        print(resp)
        if "incorrecto" in resp:
            sys.exit()

    esperar_iniciar()
    print('jugando')
    hilo_escuchador = HiloEscuchador(_socket)
    hilo_escuchador.start()
    pygame.init()
    pygame.display.set_caption("Parcheesi distribuido")
    pantalla = pygame.display.set_mode((800, 800))
    parques_cliente = ParquesCliente()
    clock = pygame.time.Clock()
    jugar = True
    print('\n' * 20)
    while jugar:
        if hilo_escuchador.data != None:
            parques_cliente.update(hilo_escuchador.data)
            hilo_escuchador = HiloEscuchador(_socket)
            hilo_escuchador.start()
        for event in pygame.event.get():
            # Salir
            if event.type == pygame.QUIT:
                _socket.close()
                sys.exit()
        parques_cliente.draw(pantalla)
        clock.tick(60)
        pygame.display.flip()
