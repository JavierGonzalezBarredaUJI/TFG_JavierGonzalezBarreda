import serial
import time
from readVoltAgent import readVoltAgent
from functions import delay_seconds
import keyboard



class dischargeTestAgent():

    def __init__(self, callback, serConfig, ardConfig, batConfig, discParam, readVoltage):
        
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
        self.Id = discParam['dischargeCurr']    # Intensidad de descarga
        self.c = discParam['dischargeStep']     # SOC de descarga (escalones del 5% de C)
        self.Ts = discParam['relaxPeriod']      # Tiempo de estabilización
        self.tm = discParam['samplePeriod']     # Periodo de muestro -> 30 segundos
        self.N = discParam['parallelLoads']     # Número de cargas conectadas en paralelo
        self.id = discParam['identifier']       # Indentificador de operación
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

        # Variables auxiliares para salida del programa
        self.aux = 0 
        self.aux2 = 0 
        
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
        exit = False

        while not exit:
            t_last = time.time()
            try:
                self.load.write(('CURR:A ' + str(self.Id) + '\n').encode())
                delay_seconds(self.td)
                comError = 0
                exit = False
                break
            except Exception as e:
                print(f"<<<< ERROR DE COMUNICACIÓN SERIAL >>>> {e}")
                self.resetSerial()
                self.turnOn()
                comError = comError + 1
                if comError >= 10:
                    self.end = 1
                    self.aux2 = 1
                    exit = True
                    return True

        while not exit:
            if keyboard.is_pressed('e'):
                print('\nSe ha pulsado exit\n')
                self.aux = 1
                break
            
            t_now = time.time()
            if (t_now - t_last) >= self.tm:

                v = self.readVolt.runCD()
                curr = self.readCURR()

                if v != 'Error' and curr != 'Error':
                    t_now = time.time()
                    t_tot = t_now - self.first
                    t = t_now - t_last
                    t_last = time.time()
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
                    print('INTENSIDAD: ', curr)
                    print('TIEMPO: ', t_tot/3600)

                    if (self.soc <= self.SOC_MIN):
                        exit = True
                        return True

                    elif (v <= self.V_MIN):
                        exit = True
                        return True

                    elif sum_descarga >= self.c:
                        exit = True
                        return False
                    
                    #t_last = time.time()

                else:
                    self.end = 1
                    self.aux2 = 1
                    exit = True
                    return True

        
    # Estabilizacion de la bateria
    def stabilize(self):
        comError = 0
        exit = False
        t_esc = time.time()

        while not exit:
            t_last = time.time()
            try:
                self.load.write(('CURR:A 0\n').encode())
                delay_seconds(self.td)
                comError = 0
                exit = False
                break
            except Exception as e:
                print(f"<<<< ERROR DE COMUNICACIÓN SERIAL >>>> {e}")
                self.resetSerial()
                self.turnOn()
                comError = comError + 1
                if comError >= 10:
                    self.end = 1
                    self.aux2 = 1
                    exit = True
                    return True

        while not exit:
            if keyboard.is_pressed('e'):
                print('\nSe ha pulsado exit\n')
                self.aux = 1
                break

            t_now = time.time()
            if (t_now - t_last) >= self.tm:

                v = self.readVolt.runCD()
                curr = self.readCURR()

                if v != 'Error' and curr != 'Error':
                    t_now = time.time()
                    t_tot = t_now - self.first
                    t = t_now - t_last
                    t_last = time.time()
                    descarga = (curr * self.N * (t/3600) * 100) / self.C
                    self.soc = self.soc - descarga
                    
                    self.data['V'].append(v)
                    self.data['SOC'].append(self.soc)
                    self.data['I'].append(curr)
                    self.data['T'].append(t_tot)

                    self.call(self.data, self.id)

                    print('\nMe estoy estabilizando')
                    print('TENSIÓN: ', v)
                    print('SOC: ', self.soc)
                    print('INTENSIDAD: ', curr)
                    print('TIEMPO: ', t_tot/3600)

                    if time.time() - t_esc > self.Ts:
                        exit = True
                    
                    #t_last = time.time()
                    
                else:
                    self.end = 1
                    self.aux2 = 1
                    exit = True
                    
                    
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
        comError = 0
        end = False

        while True:
            try:
                self.queryCURR()
                curr = self.response()
                comError = 0
                break

            except Exception as e:
                print(f"<<<< ERROR DE LECTURA DE CORRIENTE>>>> {e}")
                self.resetSerial()
                self.turnOn()
                comError = comError + 1
                if comError >= 10:
                    end = True
                    break

        if end == False:
            return curr
        else:
            return 'Error'
    
    
    # Ciclo de ejecucion del programa
    def run(self):
        exit = False
        
        self.turnOn()
        self.firstRead()
        self.first = time.time()
        while not exit:
            exit = self.discharge()
            if self.aux == 1 or self.aux2 == 1:
                break
            self.stabilize()
            if self.aux == 1 or self.aux2 == 1:
                break
        if self.end == 0:
            self.turnOff()
        self.call(self.data, self.id)
        print('\nFIN DESCARGA\n')
