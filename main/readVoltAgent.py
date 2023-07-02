import serial
import minimalmodbus
import time
import logging
import keyboard
from functions import communicationError
from functions import endSimulation


class readVoltAgent():

    def __init__(self, callback, ardConfig, readConfig):
        
        # Callback
        self.call = callback

        # Configuracion del arduino y conexion
        self.serialPortArd = ardConfig['serialPort']
        self.serialBaudArd = ardConfig['serialBaud']
        self.serialTimeoutArd = ardConfig['serialTimeout']
        self.td_a = ardConfig['comandDelay']
        
        self.arduino = minimalmodbus.Instrument(self.serialPortArd, 1, debug=False)
        self.arduino.serial.baudrate = self.serialBaudArd
        self.arduino.serial.parity = serial.PARITY_EVEN
        self.arduino.serial.bytesize = serial.EIGHTBITS
        self.arduino.serial.stopbits = serial.STOPBITS_ONE
        self.arduino.serial.timeout = self.serialTimeoutArd
        self.arduino.mode = minimalmodbus.MODE_RTU
        self.arduino.clear_buffers_before_each_transaction = True
        self.arduino.close_port_after_each_call = False

        # Lectura de la tensión
        self.fde = readConfig['scaleFactor']
        self.r1 = readConfig['r1']
        self.r2 = readConfig['r2']
        self.vz = readConfig['zenerVoltage']
        self.tm = readConfig['samplePeriod']

        # Identificador de disposivo
        self.id = ardConfig['identifier']

        # Configuración print hilo
        logging.basicConfig(level=logging.INFO, format='[%(levelname)s] (%(threadName)-s) %(message)s') 

        #self.V = []


    def resetSerial(self):
        self.arduino = minimalmodbus.Instrument(self.serialPortArd, 1, debug=False)
        self.arduino.serial.baudrate = self.serialBaudArd
        self.arduino.serial.parity = serial.PARITY_EVEN
        self.arduino.serial.bytesize = serial.EIGHTBITS
        self.arduino.serial.stopbits = serial.STOPBITS_ONE
        self.arduino.serial.timeout = self.serialTimeoutArd
        self.arduino.mode = minimalmodbus.MODE_RTU
        self.arduino.clear_buffers_before_each_transaction = True
        self.arduino.close_port_after_each_call = False


    def readVolt(self):
        v = self.arduino.read_register(0, signed=True)
        v = v * self.fde / 1000.0
        v = v + self.vz
        v = v * ((self.r1 + self.r2) / self.r2)
        return v

    
    def periodicalInterrupt(self):
        comError = 0
        first = time.time()
        t_last = time.time()

        while True:
            err = communicationError(0)
            if err == 1:
                break
            
            end = endSimulation(0)
            if end == 1:
                break

            if keyboard.is_pressed('e'):
                logging.info('\nSe ha pulsado exit\n')
                break
    
            if (time.time() - t_last >= self.tm):
                try:
                    last = time.time()
                    v = self.readVolt()
                    t_tot = last - first
                    self.call([v, t_tot], self.id)
                    #logging.info('Tensión: ' + str(v))
                    comError = 0
                    t_last = time.time()

                except Exception as e:
                    print(f"<<<< ERROR HILO VOLT >>>> {e}")
                    self.resetSerial()
                    comError = comError + 1
                    if comError >= 10:
                        communicationError(1)
                        break


    # Ciclo de ejecucion del programa
    def runCD(self):
        comError = 0
        exit = False
        end = False

        while not exit:
            try:
                v = self.readVolt()
                comError = 0
                exit = True

            except Exception as e:
                print(f"<<<< ERROR DE LECTURA DE TENSION >>>> {e}")
                self.resetSerial()
                comError = comError + 1
                if comError >= 10:
                    exit = True
                    end = True

        if end == False:
            return v
        else:
            return 'Error'

    
    def runPV(self):
        self.periodicalInterrupt()
        time.sleep(2)
        print('\nFIN VOLT\n')
        
    
    def run(self):
        comError = 0
        t_last = time.time()

        while True:
            if keyboard.is_pressed('e'):
                logging.info('\nSe ha pulsado exit\n')
                break
    
            if (time.time() - t_last >= self.tm):
                try:
                    v = self.readVolt()
                    print('Tensión: ', v, ' V')
                    t_last = time.time()
                    comError = 0

                except Exception as e:
                    print(f"<<<< ERROR DE COMUNICACIÓN >>>> {e}")
                    self.resetSerial()
                    comError = comError + 1
                    if comError >= 10:
                        break
        