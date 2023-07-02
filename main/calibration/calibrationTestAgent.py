import time
import socket
from readVoltAgent import readVoltAgent
import numpy as np
import matplotlib.pyplot as plt
from functions import curve
from functions import curve2


class calibrationTestAgent():
    def __init__(self, sockConfig, ardConfig, readVoltage):

        # Configuracion del socket y conexion a la fuente
        self.IP = sockConfig['IP']
        self.port = sockConfig['port']
        self.td = sockConfig['comandDelay']

        self.powerSupply = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.powerSupply.connect((self.IP, self.port))

        # Configuracion del arduino y conexion
        self.readVolt = readVoltAgent(0, ardConfig, readVoltage)
        
        self.v_ref = []
        self.v_out = []
        self.v_dis = []
        self.e = []
        self.e_rel = []
        
        self.calibration_file = "C:/Users/Fuente CC/Desktop/fuente_y_carga_programables/main/output_files/calibracion_fuente.csv"
        
        
    def queryVOLT(self):
        self.powerSupply.sendall('MEAS:VOLT?\n'.encode())
        time.time(self.td)


    def response(self):
        resp = self.powerSupply.recv(16)
        resp = resp.decode().replace('\n', '')
        resp = float(resp)
        return resp


    def readVOLT(self):
        self.queryVOLT()
        volt = self.response()
        return volt
        
        
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
        self.powerSupply.sendall('CURR 4\n'.encode())
        time.sleep(self.td)
        
        
    def calibrationTest(self):
        v1 = np.arange(0.0, 20.5, 0.5)
        v2 = np.arange(30.0, 110.0, 10.0)
        v3 = np.arange(150.0, 350.0, 50.0)
        vt = np.concatenate((v1, v2, v3))
        #vt = np.arange(0.0, 60.0, 10.0)
        self.v_ref = vt.tolist()

        for v in self.v_ref:
            self.powerSupply.sendall(('VOLT ' + str(v) + '\n').encode())
            time.sleep(7)  # tiempo de estabilización
            
            self.v_out.append(self.readVolt.runCD())
            self.v_dis.append(self.readVOLT())


    def calculateError(self):
        for i in range(len(self.v_ref)):
            self.e.append(abs(self.v_dis[i] - self.v_ref[i]))
            try:
                self.e_rel.append((self.e[i] * 100) / self.v_ref[i])
            except ZeroDivisionError:
                self.e_rel.append((self.e[i] * 100) / 0.0001)


    def writeData(self):
        try:
            with open(self.calibration_file, 'w') as f:
                for i in range(len(self.v_ref)):
                    line = str(self.v_ref[i]) + ',' + str(self.v_dis[i]) + ',' + str(self.e[i]) + ',' + str(self.e_rel[i]) + '\n'
                    f.write(line)
        
        except Exception as err:
            print(f"<<<< ERROR AL ABRIR EL FICHERO >>>> {err}")
            
            
    def representError(self):
        self.v_ref = self.v_ref[:24]
        self.v_out = self.v_out[:24]
        x = np.arange(0, len(self.v_ref), 1)
        
        curve(x, self.e, title='Curva de error', name='C:/Users/Fuente CC/Desktop/fuente_y_carga_programables/main/output_files/curva_error.pdf', x_axis='Número de muestra', y_axis='Tensión (V)')
        curve(x, self.e_rel, title='Curva de error relativo', name='C:/Users/Fuente CC/Desktop/fuente_y_carga_programables/main/output_files/curva_error.pdf', x_axis='Número de muestra', y_axis='Error (%)')
        curve2(x, self.v_ref, x, self.v_dis, title='Curvas de tensión', name='C:/Users/Fuente CC/Desktop/fuente_y_carga_programables/main/output_files/curva_tensiones.pdf', x_axis='Número de muestra', y_axis='Tensión (V)',
               curve1='Tensión de referencia', curve2='Tensión del display')
        
        
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
        self.calibrationTest()
        self.calculateError()
        self.writeData()
        self.representError()