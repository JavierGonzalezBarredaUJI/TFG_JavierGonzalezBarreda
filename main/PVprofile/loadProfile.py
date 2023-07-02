import serial
import time
from functions import delay_seconds
from functions import parseExcel
from functions import warningLoad
from functions import communicationError
from functions import endSimulation
import logging
import keyboard


class loadProfile():
    def __init__(self, callback, serConfig, path_file):
        
        # Callback
        self.call = callback
        
        # Configuracion del puerto serie y conexion a la carga
        self.serialPort = serConfig['serialPort']
        self.serialBaud = serConfig['serialBaud']
        self.serialTimeout = serConfig['serialTimeout']
        self.td = serConfig['comandDelay']

        self.load = serial.Serial(port=self.serialPort, 
                    baudrate=self.serialBaud,
                    bytesize=serial.EIGHTBITS,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    timeout=self.serialTimeout)

        # Path del archivo de la curva
        self.profile = path_file

        # Datos curvas
        self.interval = []  # Intervalo de tiempo
        self.I = []         # Corriente de entrada

        # Identificador de disposivo
        self.id = serConfig['identifier']

        # Configuración print hilo
        logging.basicConfig(level=logging.INFO, format='[%(levelname)s] (%(threadName)-s) %(message)s')
        
        self.end = 0


    # Restablecer conexión
    def resetSerial(self):
        self.load = serial.Serial(port=self.serialPort, 
                    baudrate=self.serialBaud,
                    bytesize=serial.EIGHTBITS,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    timeout=self.serialTimeout)
    

    # Modo remoto
    def remote(self):
        self.load.write('REMOTE\n'.encode())
        time.sleep(self.td)


    # Configuracion de la carga y conexión
    def turnOnLoad(self):
        self.load.write('REMOTE\n'.encode())
        time.sleep(self.td)
        self.load.write('FREQ 0\n'.encode())
        time.sleep(self.td)
        self.load.write('LIM:VOLT:HIGH 72\n'.encode())
        time.sleep(self.td)
        self.load.write('CHAN 2\n'.encode())
        time.sleep(self.td)
        self.load.write('MODE CC\n'.encode())
        time.sleep(self.td)
        self.load.write(('CURR:A 0\n').encode())
        time.sleep(self.td)
        self.load.write('LOAD ON\n'.encode())
        time.sleep(self.td)

    
    def turnOffLoad(self):
        self.load.write('LOAD OFF\n'.encode())
        time.sleep(self.td)
        self.load.write('CURR:A 0.0\n'.encode())
        time.sleep(self.td)
        self.load.write('LOCAL\n'.encode())
        time.sleep(self.td)
        self.load.close()
        time.sleep(self.td)
        del self.load
        
        
    def queryCURR(self):
        self.load.write('MEAS:CURR?\n'.encode())
        delay_seconds(self.td)


    def response(self):
        resp = self.load.read_until()
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
                w, I_lim = warningLoad('load', None)

                if w == 1 and i != 0:
                    self.load.write(('CURR:A ' + str(I_lim) + '\n').encode())
                    delay_seconds(2)
                    warningLoad('notcallback', None)

                    curr = self.readCURR()
                    logging.info('[WARNING] Corriente de entrada en la carga: ' + str(curr) + '\n')
                    self.call([curr, self.I[i]], self.id)

                    comError = 0
                    
                elif i == len(self.I):
                    delay_seconds(self.interval[i-1])
                    break

                elif (time.time() - t_last) >= self.interval[i-1] or i == 1:
                    self.load.write(('CURR:A ' + str(self.I[i]) + '\n').encode())
                    delay_seconds(2)
                    
                    t_last = time.time()

                    curr = self.readCURR() 
                    logging.info('Corriente de entrada en la carga: ' + str(curr) + '\n')
                    self.call([curr, self.I[i]], self.id)

                    i = i + 1
                    #t_last = time.time()
                    comError = 0
                
            except Exception as e:
                print(f"<<<< ERROR HILO LOAD>>>> {e}")
                self.resetSerial()
                self.turnOnLoad()
                comError = comError + 1
                if comError >= 10:
                    communicationError(1)
                    self.end = 1
                    break 


    # Ciclo de ejecucion del programa
    def run1(self):
        self.turnOnLoad()
        self.I, self.interval = parseExcel(self.profile)

    def run2(self):
        self.simulate()
        if self.end == 0:
            self.turnOffLoad()
        time.sleep(2)
        endSimulation(1)
        print('\nFIN LOAD\n')