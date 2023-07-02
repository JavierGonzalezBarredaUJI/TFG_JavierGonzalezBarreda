import time
import socket
from readVoltAgent import readVoltAgent
from functions import delay_seconds
import keyboard           



class chargeTestAgent():

    def __init__(self, callback, sockConfig, ardConfig, batConfig, chargeParam, readVoltage):
        
        # Callback
        self.call = callback

        # Caracteristicas de la bateria
        self.C = batConfig['capacity']                 # Capacidad de la bateria
        self.V_LIM_HIGH =  batConfig['V_LIM_HIGH']
        self.V_LIM_LOW =  batConfig['V_LIM_LOW']
        self.SOC_LIM_HIGH =  batConfig['SOC_LIM_HIGH']
        self.SOC_LIM_LOW =  batConfig['SOC_LIM_LOW']
        self.soc = batConfig['initSOC']

        # Parametros de la carga
        self.V_LIM_CC = chargeParam['V_LIM_CC']
        self.I_UMB = chargeParam['I_UMB']                     
        self.Ic = chargeParam['chargeCurr']
        self.c = chargeParam['chargeStep']     
        self.Ts = chargeParam['relaxPeriod']      
        self.tm = chargeParam['samplePeriod']
        self.id = chargeParam['identifier']          
        self.data = {
            'V': [],                            # Tensiones a lo largo de la descarga
            'SOC': [],                          # Estado de carga a lo largo de la descarga
            'I': [],                            # Intensidad durante la carga
            'T': []                             # Timepo de carga
        }                             
        self.first = time.time()

        # Configuracion del socket y conexion a la fuente
        self.IP = sockConfig['IP']
        self.port = sockConfig['port']
        self.td = sockConfig['comandDelay']

        self.powerSupply = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.powerSupply.connect((self.IP, self.port))

        # Configuracion del arduino y conexion
        self.readVolt = readVoltAgent(0, ardConfig, readVoltage)

        # Variables auxiliares para salida del programa
        self.aux = 0 
        self.aux2 = 0
        
        self.end = 0


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
    def turnOn(self):
        self.powerSupply.sendall('CONT:INT 0\n'.encode())
        time.sleep(self.td)
        self.powerSupply.sendall('CONT:EXT 1\n'.encode())
        time.sleep(self.td)
        self.powerSupply.sendall('SETPT 3\n'.encode())
        time.sleep(self.td)
        self.powerSupply.sendall(('VOLT:PROT ' + str(self.V_LIM_HIGH) + '\n').encode())
        time.sleep(self.td)
        self.powerSupply.sendall('OUTP:START\n'.encode())
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


    def charge(self):
        comError = 0
        sum_carga = 0
        exit = False

        while not exit:
            t_last = time.time()
            try:    
                self.powerSupply.sendall(('CURR ' + str(self.Ic) + '\n').encode())
                delay_seconds(self.td)
                self.powerSupply.sendall(('VOLT ' + str(self.V_LIM_CC) + '\n').encode())
                delay_seconds(self.td)
                comError = 0
                exit = False
                break
            except Exception as e:
                print(f"<<<< ERROR DE COMUNICACIÓN SOCKET >>>> {e}")
                self.resetSocket()
                self.turnOn()
                comError = comError + 1
                if comError >= 10:
                    self.aux2 = 1
                    exit = True
                    self.end = 1
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
                    carga = (curr * (t/3600) * 100) / self.C
                    sum_carga = sum_carga + carga
                    self.soc = self.soc + carga

                    self.data['V'].append(v)
                    self.data['SOC'].append(self.soc)
                    self.data['I'].append(curr)
                    self.data['T'].append(t_tot)

                    self.call(self.data, self.id)

                    print('\nMe estoy cargando')
                    print('TENSIÓN: ', v)
                    print('SOC: ', self.soc)
                    print('INTENSIDAD: ', curr)
                    print('TIEMPO: ', t_tot/3600)

                    if (curr <= self.I_UMB):
                        exit = True
                        return True

                    elif (v >= self.V_LIM_HIGH):
                        exit = True
                        return True

                    elif sum_carga >= self.c:
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
                self.powerSupply.sendall(('CURR 0.0\n').encode())
                delay_seconds(self.td)
                self.powerSupply.sendall(('VOLT 0.0\n').encode())
                delay_seconds(self.td)
                comError = 0
                exit = False
                break
            except Exception as e:
                print(f"<<<< ERROR DE COMUNICACIÓN SOCKET >>>> {e}")
                self.resetSocket()
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
                    t_last = time.time()

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


    # desconexion de la fuente
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


    def queryCURR(self):
        self.powerSupply.sendall('MEAS:CURR?\n'.encode())
        delay_seconds(self.td)


    def response(self):
        resp = self.powerSupply.recv(16)
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
                self.resetSocket()
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
            exit = self.charge()
            if self.aux == 1 or self.aux2 == 1:
                break
            self.stabilize()
            if self.aux == 1 or self.aux2 == 1:
                break
        if self.end == 0:
            self.turnOff()
        self.call(self.data, self.id)
        print('\nFIN CARGA\n')

    