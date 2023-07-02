import serial
import time
from readVoltAgent import readVoltAgent
from functions import delay_seconds
from functions import parseExcel
import keyboard


class dischargeProfileAgent():
    def __init__(self, callback, serConfig, ardConfig, batConfig, discParam, readVoltage, path_file):
        
        # Callback
        self.call = callback

        # Caracteristicas de la bateria
        self.C = batConfig['capacity']                 # Capacidad de la bateria
        self.V_LIM_HIGH =  batConfig['V_LIM_HIGH']
        self.V_LIM_LOW =  batConfig['V_LIM_LOW']
        self.SOC_LIM_HIGH =  batConfig['SOC_LIM_HIGH']
        self.SOC_LIM_LOW =  batConfig['SOC_LIM_LOW']
        self.soc = batConfig['initSOC']

        # Parametros de la descarga
        self.V_MIN = discParam['V_MIN']         # Tensión mínima de descarga
        self.SOC_MIN = discParam['SOC_MIN']     # SOC minimo que debe alcanzar la bateria durante la descarga
        self.tm = discParam['samplePeriod']     # Periodo de muestro -> 30 segundos
        self.N = discParam['parallelLoads']     # Número de cargas conectadas en paralelo
        self.id = discParam['identifier']       # Indentificador de operación
        self.Id = []
        self.interval = []
        self.data = {
            'V': [],                            # Tensiones a lo largo de la descarga
            'SOC': [],                          # Estado de carga a lo largo de la descarga
            'I': [],                            # Intensidad durante la descarga
            'T': []                             # Timepo de descarga
        }                           
        self.first = time.time()
        
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

        # Configuracion del arduino y conexion
        self.readVolt = readVoltAgent(0, ardConfig, readVoltage)
        
        # Path del archivo de la curva
        self.profile = path_file
        
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
    def turnOn(self):
        self.load.write('REMOTE\n'.encode())
        time.sleep(self.td)
        self.load.write('FREQ 0\n'.encode())
        time.sleep(self.td)
        self.load.write(('LIM:VOLT:LOW ' + str(self.V_LIM_LOW) + '\n').encode())
        time.sleep(self.td)
        self.load.write(('LIM:VOLT:HIGH ' + str(self.V_LIM_HIGH) + '\n').encode())
        time.sleep(self.td)
        self.load.write('CHAN 2\n'.encode())
        time.sleep(self.td)
        self.load.write('MODE CC\n'.encode())
        time.sleep(self.td)
        self.load.write(('CURR:A 0\n').encode())
        time.sleep(self.td)
        self.load.write('LOAD ON\n'.encode())
        time.sleep(self.td)


    def firstRead(self):
        self.data['V'].append(self.readVolt.runCD())
        self.data['SOC'].append(self.soc)
        self.data['I'].append(0)
        self.data['T'].append(0)

        self.call(self.data, self.id)

        print('\nPrimera lectura')
        print('TENSIÓN: ', self.data['V'][0])
        print('SOC: ', self.soc)
        
        
    # Descarga de la bateria
    def discharge(self):
        comError = 0
        sum_descarga = 0
        i = 0
        t_last = time.time()
        t_volt = time.time()

        while i <= len(self.Id):
            if keyboard.is_pressed('e'):
                print('\nSe ha pulsado exit\n')
                break
                
            try:
                if i == 0:
                    self.load.write(('CURR:A ' + str(self.Id[i]) + '\n').encode())
                    delay_seconds(self.td)
                    t_last = time.time()
                    i = i + 1
                    comError = 0
                    
                elif i == len(self.Id):
                    delay_seconds(self.interval[i-1])
                    break
                
                elif time.time() - t_last >= self.interval[i-1]:
                    self.load.write(('CURR:A ' + str(self.Id[i]) + '\n').encode())
                    delay_seconds(self.td)
                    t_last = time.time()
                    i = i + 1
                    comError = 0
            
            except Exception as e:
                print(f"<<<< ERROR DE COMUNICACIÓN SERIAL >>>> {e}")
                self.resetSerial()
                self.turnOn()
                comError = comError + 1
                if comError >= 10:
                    self.end = 1
                    break 
                
            try:    
                t_now = time.time()    
                if (t_now - t_volt) >= self.tm:
                    curr = self.readCURR()
                    v = self.readVolt.runCD()
                    
                    if v == 'Error':
                        break
                    
                    t_now = time.time()
                    t_tot = t_now - self.first
                    t = t_now - t_volt
                    t_volt = time.time()
                    descarga = (curr * self.N * (t/3600) * 100) / self.C
                    sum_descarga = sum_descarga + descarga
                    self.soc = self.soc - descarga
                    
                    self.data['V'].append(v)
                    self.data['SOC'].append(self.soc)
                    self.data['I'].append(curr)
                    self.data['T'].append(t_tot)

                    self.call(self.data, self.id)

                    print('\nMe estoy descargando')
                    print('TENSIÓN: ', v)
                    print('SOC: ', self.soc)
                    
                    #t_volt = time.time()
                    
                    if (self.soc <= self.SOC_MIN):
                        break

                    elif (v <= self.V_MIN):
                        break
                    
                    
            except Exception as e:
                print(f"<<<< ERROR DE COMUNICACIÓN SERIAL >>>> {e}")
                self.resetSerial()
                self.turnOn()
                comError = comError + 1
                if comError >= 10:
                    self.end = 1
                    break
        
    
    # Desconexion de la carga
    def turnOff(self):
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
    
    
    # Ciclo de ejecucion del programa
    def run(self):
        self.Id, self.interval = parseExcel(self.profile)
        self.turnOn()
        self.firstRead()
        self.first = time.time()
        self.discharge()
        if self.end == 0:
            self.turnOff()
        self.call(self.data, self.id)
        print('\nFIN DESCARGA\n')