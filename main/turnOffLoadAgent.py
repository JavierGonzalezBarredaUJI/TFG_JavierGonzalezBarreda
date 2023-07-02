import serial
import time



class turnOffLoadAgent():

    def __init__(self, serConfig):
        
        self.serialPort = serConfig['serialPort']
        self.serialBaud = serConfig['serialBaud']
        self.serialTimeout = serConfig['serialTimeout']
        self.td = serConfig['comandDelay']
        
        # Configuracion del puerto serie y conexion a la carga
        self.load = serial.Serial(port=self.serialPort, 
                    baudrate=self.serialBaud,
                    bytesize=serial.EIGHTBITS,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    timeout=self.serialTimeout) 
        
        
    # Configuracion de la carga y conexión
    def remote(self):
        self.load.write('REMOTE\n'.encode())
        time.sleep(self.td)
                    
                    
    # Desconexion de la carga
    def turnOff(self):
        self.load.write('GLOB: LOAD OFF\n'.encode())
        time.sleep(self.td)
        self.load.write('CHAN 2\n'.encode())
        time.sleep(self.td)
        self.load.write('CURR:A 0.0\n'.encode())
        time.sleep(self.td)
        self.load.write('CHAN 3\n'.encode())
        time.sleep(self.td)
        self.load.write('CURR:A 0.0\n'.encode())
        time.sleep(self.td)
        self.load.write('CHAN 4\n'.encode())
        time.sleep(self.td)
        self.load.write('CURR:A 0.0\n'.encode())
        time.sleep(self.td)
        self.load.write('LOCAL\n'.encode())
        time.sleep(self.td)
        self.load.close()
        time.sleep(self.td)
        del self.load
    
    
    # Ciclo de ejecucion del programa
    def run(self):
        self.remote()
        self.turnOff()
        print('Carga apagada')
