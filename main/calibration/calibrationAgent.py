import time
import socket


class calibrationAgent():

    def __init__(self, sockConfig, calParam):
        
        # Parametros de la calibración
        self.pot = calParam['potentiometer']
        self.value = calParam['value']
        self.password = calParam['password']

        # Configuracion del socket y conexion a la fuente
        self.IP = sockConfig['IP']
        self.port = sockConfig['port']
        self.td = sockConfig['comandDelay']

        self.powerSupply = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.powerSupply.connect((self.IP, self.port))
        
        
    # Configuracion de la fuente y conexión
    def turnOn(self):
        self.powerSupply.sendall('CONT:INT 0\n'.encode())
        time.sleep(self.td)
        self.powerSupply.sendall('CONT:EXT 1\n'.encode())
        time.sleep(self.td)
        self.powerSupply.sendall('SETPT 3\n'.encode())
        time.sleep(self.td)
        self.powerSupply.sendall('OUTP:START\n'.encode())
        time.sleep(self.td)
        
    def calibration(self):
        self.powerSupply.sendall(('CAL:PASS ' + str(self.password) + '\n').encode())
        time.sleep(self.td)
        
        if self.value == 'default':
            self.powerSupply.sendall('CAL:DEF\n'.encode())
            time.sleep(self.td)
        else:
            self.powerSupply.sendall(('CAL:POT '+ str(self.pot) + ' ' + str(self.value) + '\n').encode())
            time.sleep(self.td)
            
        self.powerSupply.sendall('CAL:STOP\n'.encode())
        time.sleep(self.td)
        
        
    # desconexion de la fuente
    def turnOff(self):
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
        
        
    def run(self):
        self.turnOn()
        self.calibration()
        self.turnOff()