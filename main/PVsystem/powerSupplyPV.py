import socket
import time
from functions import delay_seconds
from functions import warningPS
from functions import communicationError
from functions import endSimulation
from functions import sendTimePS
from functions import receiveTimePS
import logging
import keyboard
import numpy as np


class powerSupplyPV():

    def __init__(self, callback, sockConfig, pvParam, path_file):
        
        # Callback
        self.call = callback

        # Configuracion del socket y conexion a la fuente
        self.IP = sockConfig['IP']
        self.port = sockConfig['port']
        self.td = sockConfig['comandDelay']

        self.powerSupply = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.powerSupply.connect((self.IP, self.port))

        # Parámetros de la instalación de FV
        self.PR = pvParam['performanceRatio']          # Performance Ratio
        self.P_inst = pvParam['installedPotency']      # Wp
        self.STCRadiation = pvParam['STCRadiation']    # W/m2
        self.G_max = pvParam['maxIrradiance']          # Irradiancia máxima de un año
        self.I_max = pvParam['maxPSCurrent']           # 
        self.timeSCL = pvParam['timeSCL_PS']           # Escala de tiempo

        # Path del archivo de la curva
        self.file = path_file
        
        # Periodo de cambio de irradiancia
        self.tg = None

        # Datos curvas
        self.G = []     # Irradiancia
        self.t = []     # Hora
        self.P = []     # Potencia generada
        self.I = []     # Corriente de salida
        self.SCL = None # Parámetro de escala
        self.t_load = None
        self.n_items = None

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

    
    def calculatePeriod(self):
        if self.timeSCL == 'AUTO':
            if len(self.G) == 24:
                self.tg = 3600
            elif len(self.G) == 96:
                self.tg = 900
            elif len(self.G) == 1440:
                self.tg = 60
            #self.tg = (self.t[1] - self.t[0]) * self.timeSCL
        else:
            self.tg = float(self.timeSCL)

        sendTimePS([self.tg, len(self.G)])


    def cloneCurrent(self):
        if self.t_load < self.tg:
            self.tg = self.t_load
            clones = self.n_items / len(self.G)
            self.I = np.array(self.I)
            self.I = np.repeat(self.I, clones)
            self.I = list(self.I)


    def calculateScale(self):
        if self.G_max == 'AUTO':
            self.G_max = max(self.G)
        else:
            self.G_max = float(self.G_max)
            
        self.SCL = ((self.PR * self.G_max * self.P_inst) / self.STCRadiation) / self.I_max


    def isValidTime(self, data):
        try:
            time.strptime(data, "%H:%M")
            return True
        except ValueError:
            return False

    
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


    def parseCurve(self):
        try:
            with open(self.file, 'r') as f:
                for line in f:
                    if self.isValidTime(line[:4]):
                        line = line.replace('\n', '').split('\t\t')
                        hour = line[0].split(':')
                        self.t.append(int(hour[0]))
                        self.G.append(float(line[1]))

        except Exception as e:
            print(f"<<<< ERROR AL ABRIR EL FICHERO >>>> {e}")


    def calculateCurrent(self):
        for i in range(len(self.G)):
            self.P.append((self.PR * self.G[i] * self.P_inst) / self.STCRadiation)
            self.I.append(self.P[i] / self.SCL)
        #print(self.I)


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
                    delay_seconds(self.tg)
                    break
        
                elif ((time.time() - t_last >= self.tg) or (i == 0)):
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
        self.parseCurve()
        self.calculatePeriod()
        self.calculateScale()
        self.calculateCurrent()
        time.sleep(5)
        self.t_load, self.n_items = receiveTimePS()
        self.cloneCurrent()

    def run2(self):
        self.simulate()
        if self.end == 0:
            self.turnOffPS()
        time.sleep(2)
        endSimulation(1)
        print('\nFIN PS\n')