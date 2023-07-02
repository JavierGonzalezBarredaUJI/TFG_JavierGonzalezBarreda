import socket
import time
from functions import delay_seconds
from functions import parseExcel
from functions import warningPS
from functions import communicationError
from functions import endSimulation
import logging
import keyboard


class powerSupplyProfile():
    def __init__(self, callback, sockConfig, path_file):
        
        # Callback
        self.call = callback

        # Configuracion del socket y conexion a la fuente
        self.IP = sockConfig['IP']
        self.port = sockConfig['port']
        self.td = sockConfig['comandDelay']

        self.powerSupply = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.powerSupply.connect((self.IP, self.port))

        # Path del archivo de la curva
        self.profile = path_file

        # Datos curvas
        self.interval = []      # Intervalo de tiempo
        self.I = []             # Corriente de salida

        # Identificador de disposivo
        self.id = sockConfig['identifier']

        # Configuración print hilo
        logging.basicConfig(level=logging.INFO, format='[%(levelname)s] (%(threadName)-s) %(message)s')
        
        self.end = 0

        communicationError('i')
        endSimulation('i')


    # Restablecer conexión
    def resetSocket(self):
        self.powerSupply = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.powerSupply.connect((self.IP, self.port))

    
    # Modo remoto
    def remote(self):
        self.powerSupply.sendall('CONT:INT 0\n'.encode())
        time.sleep(self.td)
        self.powerSupply.sendall('CONT:EXT 1\n'.encode())
        time.sleep(self.td)
        self.powerSupply.sendall('SETPT 3\n'.encode())
        time.sleep(self.td)

    
    # Configuracion de la fuente y conexión
    def turnOnPS(self):
        self.powerSupply.sendall('CONT:INT 0\n'.encode())
        time.sleep(self.td)
        self.powerSupply.sendall('CONT:EXT 1\n'.encode())
        time.sleep(self.td)
        self.powerSupply.sendall('SETPT 3\n'.encode())
        time.sleep(self.td)
        self.powerSupply.sendall('VOLT:PROT 72\n'.encode())
        time.sleep(self.td)
        self.powerSupply.sendall('OUTP:START\n'.encode())
        time.sleep(self.td)
        self.powerSupply.sendall('CURR 0\n'.encode())
        time.sleep(self.td)
        self.powerSupply.sendall('VOLT 71\n'.encode())
        time.sleep(self.td)
        

    # desconexion de la fuente
    def turnOffPS(self):
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
        
    
    def queryCURR(self):
        self.powerSupply.sendall('MEAS:CURR?\n'.encode())
        delay_seconds(self.td)


    def response(self):
        resp = self.powerSupply.recv(16)
        resp = resp.decode().replace('\n', '')
        resp = float(resp)
        return resp


    def readCURR(self):
        self.queryCURR()
        curr = self.response()
        return curr
    
    
    def simulate(self):
        comError = 0
        i = 0
        t_last = time.time()

        while i <= len(self.I):
            err = communicationError(0)
            if err == 1:
                break

            if keyboard.is_pressed('e'):
                logging.info('\nSe ha pulsado exit\n')
                break

            end = endSimulation(0)
            if end == 1:
                break

            try:
                w, I_lim = warningPS('ps', None)

                if w == 1 and i != 0:
                    self.powerSupply.sendall(('CURR ' + str(I_lim) + '\n').encode())
                    delay_seconds(2)
                    warningPS('notcallback', None)
                    
                    curr = self.readCURR()
                    logging.info('[WARNING] Corriente de salida de la fuente: ' + str(curr) + '\n')
                    self.call([curr, self.I[i]], self.id)
                    
                    comError = 0
                    
                elif i == len(self.I):
                    delay_seconds(self.interval[i-1])
                    break
        
                elif (time.time() - t_last) >= self.interval[i-1] or i == 0:
                    self.powerSupply.sendall(('CURR ' + str(self.I[i]) + '\n').encode())
                    delay_seconds(2)
                    
                    t_last = time.time()

                    curr = self.readCURR()
                    logging.info('Corriente de salida de la fuente: ' + str(curr) + '\n')
                    self.call([curr, self.I[i]], self.id)
                    
                    i = i + 1
                    #t_last = time.time()
                    comError = 0
                
            except Exception as e:
                print(f"<<<< ERROR HILO PS >>>> {e}")
                self.resetSocket()
                self.turnOnPS()
                comError = comError + 1
                if comError >= 10:
                    communicationError(1)
                    self.end = 1
                    break
        
    
    # Ciclo de ejecucion del programa
    def run1(self):
        self.turnOnPS()
        self.I, self.interval = parseExcel(self.profile)

    def run2(self):
        self.simulate()
        if self.end == 0:
            self.turnOffPS()
        time.sleep(2)
        endSimulation(1)
        print('\nFIN PS\n')