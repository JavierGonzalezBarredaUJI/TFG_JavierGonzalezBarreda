import time, socket


class turnOffPSAgent():

    def __init__(self, sockConfig):

        self.IP = sockConfig['IP']
        self.port = sockConfig['port']
        self.td = sockConfig['comandDelay']

        # Configuracion del socket y conexion a la fuente
        self.powerSupply = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.powerSupply.connect((self.IP, self.port))

    def remote(self):
        self.powerSupply.sendall('CONT:INT 0\n'.encode())
        time.sleep(self.td)
        self.powerSupply.sendall('CONT:EXT 1\n'.encode())
        time.sleep(self.td)
        self.powerSupply.sendall('SETPT 3\n'.encode())
        time.sleep(self.td)

    def turnOff(self):
        self.powerSupply.sendall('VOLT 0\n'.encode())
        time.sleep(self.td)
        self.powerSupply.sendall('CURR 0\n'.encode())
        time.sleep(self.td)
        self.powerSupply.sendall('OUTP:STOP\n'.encode())
        time.sleep(self.td)
        self.powerSupply.sendall('CONT:EXT 0\n'.encode())
        time.sleep(self.td)
        self.powerSupply.sendall('CONT:INT 1\n'.encode())
        time.sleep(self.td)
        self.powerSupply.sendall('SETPT 0\n'.encode())
        time.sleep(self.td)
        self.powerSupply.close()
        time.sleep(self.td)
        del self.powerSupply
        time.sleep(self.td)

    # Ciclo de ejecucion del programa
    def run(self):
        self.remote()
        self.turnOff()
        print('Fuente apagada')
