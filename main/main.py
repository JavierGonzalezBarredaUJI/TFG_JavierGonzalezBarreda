"""
main.py
Desarrollado por Javier González Barreda
Agosto, 2022

Módulo principal del programa que gestiona diferentes funcionalidades a través de un menú.
Además se encarga de gestionar la adquisición de datos mediante callbacks y la entrada de
datos.
"""

from CDtest.dischargeTestAgent import dischargeTestAgent
from CDtest.chargeTestAgent import chargeTestAgent
from CDprofile.dischargeProfileAgent import dischargeProfileAgent
from CDprofile.chargeProfileAgent import chargeProfileAgent
from CDconstant.dischargeConstantAgent import dischargeConstantAgent
from CDconstant.chargeConstantAgent import chargeConstantAgent
from PVsystem.powerSupplyPV import powerSupplyPV
from PVsystem.loadPV import loadPV
from PVprofile.powerSupplyProfile import powerSupplyProfile
from PVprofile.loadProfile import loadProfile
from readVoltAgent import readVoltAgent
from calibration.calibrationAgent import calibrationAgent
from calibration.calibrationTestAgent import calibrationTestAgent
from turnOffLoadAgent import turnOffLoadAgent
from turnOffPSAgent import turnOffPSAgent
from functions import calculateSOC
from functions import writeDataCD
from functions import writeDataPV
from functions import warningPS
from functions import warningLoad
from threading import Thread
from inputData import inputData
#import tkinter as tk
#from tkinter import ttk
import curvesCD
import curvesPV
#import matplotlib.pyplot as plt
import json
import time
import os


class main():
    dischargeTestBattery = None
    chargeTestBattery = None
    dischargeProfileBattery = None
    chargeProfileBattery = None
    dischargeConstantBattery = None
    chargeConstantBattery = None
    pvPowerSupply = None
    pvLoad = None
    profilePowerSupply = None
    profileLoad = None
    readVolt = None
    calibration = None
    calibrationTest = None
    turnOffLoad = None
    turnOffPS = None
    
    
    def __init__(self):
        self.curr_ps = 0
        self.i_ps = 0
        self.curr_load = 0
        self.i_load = 0
        self.curr_bat = 0
        self.volt = 61.5
        self.soc = None
        self.time = 0
        self.time_bat = 0
        self.capacity = None
        self.V_LIM_HIGH = None
        self.V_LIM_LOW = None
        self.pvData ={
            'I_ps': [],
            'I_load':[],
            'I_bat':[],
            'V':[],
            'SOC':[],
            'T':[]
        }
        self.aux = 0
        self.parentDirectory = os.getcwd()
        self.main()
    
    
    def cdCallback(self, data, id):
        with open('config.json') as config_file:
            config = json.load(config_file)

        config['battery']['initSOC'] = data['SOC'][-1]

        with open('config.json', 'w') as file:
                json.dump(config, file)

        writeDataCD(data, id)


    def pvCallback(self, data, id):
        if id == 'V':
            self.volt = data[0]
            self.time = data[1]
            self.curr_bat = self.curr_ps - self.curr_load
            if self.time < 6:
                ts = self.time
            else:
                last = self.pvData['T']
                ts = self.time - last[-1]
            self.soc = calculateSOC(self.curr_bat, ts, self.soc, self.capacity)

            with open('config.json') as config_file:
                config = json.load(config_file)

            config['battery']['initSOC'] = self.soc

            with open('config.json', 'w') as file:
                    json.dump(config, file)

            self.pvData['V'].append(self.volt)
            self.pvData['I_ps'].append(self.curr_ps)
            self.pvData['I_load'].append(self.curr_load)
            self.pvData['I_bat'].append(self.curr_bat)
            self.pvData['T'].append(self.time)
            self.pvData['SOC'].append(self.soc)

            print('Tensión: ', self.volt, '\n'
                  'Corriente fuente: ', self.curr_ps, '\n'
                  'Corriente carga: ', self.curr_load, '\n'
                  'Corriente bateria: ', self.curr_bat, '\n'
                  'SOC: ', self.soc, '\n')

        elif id == 'PS':
            self.curr_ps = data[0]
            self.i_ps = data[1]

        elif id == 'L':
            self.curr_load = data[0]
            self.i_load = data[1]

        with open(os.path.join(self.parentDirectory, "output_files", "datos_fv.json"), 'w') as file:
            json.dump(self.pvData, file)


        if (self.curr_ps > 0) and (self.curr_load < self.curr_ps) and (self.curr_bat > 0.1) and (self.volt >= self.V_LIM_HIGH):
            if self.aux == 1:
                warningPS('callback', self.curr_load)
                print('\n<<<<LIMITACIÓN DE LA FUENTE>>>>\n')
                self.aux = 0
            else:
                self.aux = 1
        
        elif (self.curr_load > 0.03) and (self.curr_load > self.curr_ps) and (self.curr_bat < -0.1) and (self.volt <= self.V_LIM_LOW):
            if self.aux == 1:
                warningLoad('callback', self.curr_ps)
                print('\n<<<<LIMITACIÓN DE LA CARGA>>>>\n')
                self.aux = 0
            else:
                self.aux = 1
    

    def readVoltCallback(self):
        pass
    
    
    def parseConfig(self, config, option):
        if option == 'dischargeTestBattery':
            self.dischargeTestBattery = dischargeTestAgent(self.cdCallback, config['serial'], config['arduino'], 
                                                   config['battery'], config['discharge_test_parameters'], config['read_voltage'])
        
        if option == 'chargeTestBattery':
            self.chargeTestBattery = chargeTestAgent(self.cdCallback, config['socket'], config['arduino'], 
                                                   config['battery'], config['charge_test_parameters'], config['read_voltage'])
        
        if option == 'dischargeProfileBattery':
            path_file = os.path.join(self.parentDirectory, "input_files", config['path_files']['discharge_profile'])
            self.dischargeProfileBattery = dischargeProfileAgent(self.cdCallback, config['serial'], config['arduino'], config['battery'], 
                                                    config['discharge_profile_parameters'], config['read_voltage'], path_file)
            
        if option == 'chargeProfileBattery':
            path_file = os.path.join(self.parentDirectory, "input_files", config['path_files']['charge_profile'])
            self.chargeProfileBattery = chargeProfileAgent(self.cdCallback, config['socket'], config['arduino'], config['battery'], 
                                                    config['charge_profile_parameters'], config['read_voltage'], path_file)
            
        if option == 'dischargeConstantBattery':
            self.dischargeConstantBattery = dischargeConstantAgent(self.cdCallback, config['serial'], config['arduino'], 
                                                   config['battery'], config['discharge_constant_parameters'], config['read_voltage'])
            
        if option == 'chargeConstantBattery':
            self.chargeConstantBattery = chargeConstantAgent(self.cdCallback, config['socket'], config['arduino'], 
                                                   config['battery'], config['charge_constant_parameters'], config['read_voltage'])
            
        if option == 'pvSimulator':
            path_file_1 = os.path.join(self.parentDirectory, "input_files", config['path_files']['irradiance_curve'])
            path_file_2 = os.path.join(self.parentDirectory, "input_files", config['path_files']['consumtion_curve'])
            self.pvPowerSupply = powerSupplyPV(self.pvCallback, config['socket'], config['PV_parameters'], path_file_1)
            self.pvLoad = loadPV(self.pvCallback, config['serial'], config['PV_parameters'], path_file_2)
            self.readVolt = readVoltAgent(self.pvCallback, config['arduino'], config['read_voltage'])
            battery = config['battery']
            self.soc = battery['initSOC']
            self.capacity = battery['capacity']
            self.V_LIM_HIGH = battery['V_LIM_HIGH']
            self.V_LIM_LOW = battery['V_LIM_LOW']
            
        if option == 'pvProfile':
            path_file_1 = os.path.join(self.parentDirectory, "input_files", config['path_files']['generation_profile'])
            path_file_2 = os.path.join(self.parentDirectory, "input_files", config['path_files']['consumtion_profile'])
            self.profilePowerSupply = powerSupplyProfile(self.pvCallback, config['socket'], path_file_1)
            self.profileLoad = loadProfile(self.pvCallback, config['serial'], path_file_2)
            self.readVolt = readVoltAgent(self.pvCallback, config['arduino'], config['read_voltage'])
            battery = config['battery']
            self.soc = battery['initSOC']
            self.capacity = battery['capacity']
            self.V_LIM_HIGH = battery['V_LIM_HIGH']
            self.V_LIM_LOW = battery['V_LIM_LOW']
            
        if option == 'readVolt':
            self.readVolt = readVoltAgent(self.readVoltCallback, config['arduino'], config['read_voltage'])
            
        if option == 'calibration':
            self.calibration = calibrationAgent(config['socket'], config['calibration_parameters'])
            
        if option == 'calibrationTest':
            self.calibrationTest = calibrationTestAgent(config['socket'], config['arduino'], config['read_voltage'])

        if option == 'turnOffLoad':
            self.turnOffLoad = turnOffLoadAgent(config['serial'])
        
        if option == 'turnOffPS':
            self.turnOffPS = turnOffPSAgent(config['socket'])

        if option == 'turnOff':
            self.turnOffLoad = turnOffLoadAgent(config['serial'])
            self.turnOffPS = turnOffPSAgent(config['socket'])

    
    def main(self):
        exit = False
        config = ''
        with open('config.json') as config_file:
            config = json.load(config_file)


        while not exit:
            print()
            print('______MENÚ______')
            print()
            print('1. Ensayo de descarga\n'
                  '2. Ensayo de carga\n'
                  '3. Descargar siguiendo un perfil\n'
                  '4. Cargar siguiendo un perfil\n'
                  '5. Descarga constante\n'
                  '6. Carga constante\n'
                  '7. Simular un sistema de FV con curvas\n'
                  '8. Simular un sistema de FV con perfiles\n'
                  '9. Lectura de tensión\n'
                  '10. Calibración de la fuente\n'
                  '11. Ensayo de calibración\n'
                  '12. Apagar carga\n'
                  '13. Apagar fuente\n'
                  '14. Apagar todo el sistema\n'
                  '15. Cambiar configuaración de la bateria\n'
                  '16. Cambiar configuaración del sistema de medida de tensión\n'
                  '17. Salir\n')

            while(True):
                op = input('Selecciona una opción: ')
                if op.isdigit():
                    op = int(op)
                    if 1 <= op <= 17:
                        inputData(op, config)
                        break
                    else:
                        print('¡Introduce una opción entre 1 y 17!')
                else:
                    print('¡Introduce un entero válido!')
            print()

            if op == 1:
                #print(config['battery'])
                #print(config['discharge_test_parameters'])
                #print(config['read_voltage'])
                self.parseConfig(config, 'dischargeTestBattery')
                self.dischargeTestBattery.run()
                curvesCD.run(file_name=os.path.join(self.parentDirectory, "output_files", "datos_descarga.csv"))
                
            elif op == 2:
                self.parseConfig(config, 'chargeTestBattery')
                self.chargeTestBattery.run()
                curvesCD.run(file_name=os.path.join(self.parentDirectory, "output_files", "datos_carga.csv"))
                
            elif op == 3:
                self.parseConfig(config, 'dischargeProfileBattery')
                self.dischargeProfileBattery.run()
                curvesCD.run(file_name=os.path.join(self.parentDirectory, "output_files", "datos_descarga_perfil.csv"))
                
            elif op == 4:
                self.parseConfig(config, 'chargeProfileBattery')
                self.chargeProfileBattery.run()
                curvesCD.run(file_name=os.path.join(self.parentDirectory, "output_files", "datos_carga_perfil.csv"))
                
            elif op == 5:
                self.parseConfig(config, 'dischargeConstantBattery')
                self.dischargeConstantBattery.run()
                #curvesCD.run(file_name=os.path.join(self.parentDirectory, "output_files", "datos_descarga.csv"))
                
            elif op == 6:
                self.parseConfig(config, 'chargeConstantBattery')
                self.chargeConstantBattery.run()
                #curvesCD.run(file_name=os.path.join(self.parentDirectory, "output_files", "datos_carga.csv"))
                
            elif op == 7:
                self.parseConfig(config, 'pvSimulator')

                t1 = Thread(name='Hilo PS', target=self.pvPowerSupply.run1)
                t2 = Thread(name='Hilo Load', target=self.pvLoad.run1)
                t1.start()
                t2.start()
                t1.join()
                t2.join()

                t1 = Thread(name='Hilo PS', target=self.pvPowerSupply.run2)
                t2 = Thread(name='Hilo Load', target=self.pvLoad.run2)
                t3 = Thread(name='Hilo Volt', target=self.readVolt.runPV)
                t1.start()
                t2.start()
                t3.start()
                t1.join()
                t2.join()
                t3.join()

                writeDataPV(self.pvData)
                curvesPV.run(file_name=os.path.join(self.parentDirectory, "output_files", "datos_fv.json"), SCLtime='h')
                
            elif op == 8:
                self.parseConfig(config, 'pvProfile')

                t1 = Thread(name='Hilo PS', target=self.profilePowerSupply.run1)
                t2 = Thread(name='Hilo Load', target=self.profileLoad.run1)
                t1.start()
                t2.start()
                t1.join()
                t2.join()

                first = time.time()
                
                t1 = Thread(name='Hilo PS', target=self.profilePowerSupply.run2)
                t2 = Thread(name='Hilo Load', target=self.profileLoad.run2)
                t3 = Thread(name='Hilo Volt', target=self.readVolt.runPV)
                t1.start()
                t2.start()
                t3.start()
                t1.join()
                t2.join()
                t3.join()

                if time.time() - first >= 7200:
                    t = 'h'
                else:
                    t = 'm'
                
                writeDataPV(self.pvData)
                curvesPV.run(file_name=os.path.join(self.parentDirectory, "output_files", "datos_fv.json"), SCLtime=t)
                
            elif op == 9:
                self.parseConfig(config, 'readVolt')
                self.readVolt.run()
                #curvesVolt.run(file_name="C:/Users/Fuente CC/Desktop/fuente_y_carga_programables/main/output_files/datos_lectura_tension.csv")
                
            elif op == 10:
                self.parseConfig(config, 'calibration')
                self.calibration.run()
                
            elif op == 11:
                self.parseConfig(config, 'calibrationTest')
                resistance = input('Resisitencia de 100 ohms conectada en paralelo con la fuente (si/no): ')
                print()
                while True:
                    if resistance == 'si':
                        self.calibration.run()
                        break
                    else:
                        print('Conecta una resistencia de 100 ohms en paralelo con la fuente.')

            elif op == 12:
                self.parseConfig(config, 'turnOffLoad')
                self.turnOffLoad.run()

            elif op == 13:
                self.parseConfig(config, 'turnOffPS')
                self.turnOffPS.run()

            elif op == 14:
                self.parseConfig(config, 'turnOff')

                t1 = Thread(name='Hilo PS', target=self.turnOffPS.run)
                t2 = Thread(name='Hilo Load', target=self.turnOffLoad.run)
                t1.start()
                t2.start()
                t1.join()
                t2.join()
                
            elif op == 15:
                pass

            elif op == 16:
                pass

            elif op == 17:
                exit = True
                print('FIN DEL PROGRAMA\n')
            
            elif op == 18:
                curvesCD.run(file_name="C:/Users/Fuente CC/Desktop/fuente_y_carga_programables/main/output_files/datos_carga.csv")
            
        
        

main()