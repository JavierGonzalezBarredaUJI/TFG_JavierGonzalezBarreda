import json
import os

parentDirectory = os.getcwd()

def saveDefault(config):
    while(True):
        save = input('Guardar cambios como valores por defecto -> Si [1] / No [0]: ')
        if save =='0' or save =='1':
                break
        else:
            print('¡Introduce una opción válida!')

    if save == '1':
            with open('config.json', 'w') as file:
                json.dump(config, file)

def inputData(op, config):
    if op == 1:
        showParam(config)

        print('____PARÁMETROS DE LA DESCARGA___')
        print('Tensión objetivo (V): ', config['discharge_test_parameters']['V_MIN'])
        print('SOC objetivo (%): ', config['discharge_test_parameters']['SOC_MIN'])
        print('Intensidad de descarga (A): ', config['discharge_test_parameters']['dischargeCurr'])
        print('Escalones de descarga (%): ', config['discharge_test_parameters']['dischargeStep'])
        print('Periodo de relajación (s): ', config['discharge_test_parameters']['relaxPeriod'])
        print('Periodo de muestreo (s): ', config['discharge_test_parameters']['samplePeriod'])
        print('Número de cargas en paralelo: ', config['discharge_test_parameters']['parallelLoads'])
        print()

        while(True):
            default_ = input('Parametros por defecto [1] / Cambiar parametros [0]: ')
            if default_=='0' or default_=='1':
                break
            else:
                print('¡Introduce una opción válida!')
        
        if default_ == '0':
            while True:
                try:
                    config['discharge_test_parameters']['parallelLoads'] = int(input('Número de cargas en paralelo [1 - 3]: '))
                    if 1 <= config['discharge_test_parameters']['parallelLoads'] <= 3:
                        break
                    else:
                        print('¡Introduce un entero entre 1 y 3!')
                except ValueError:
                    print('¡Introduce un valor válido!')
            while True:
                try:
                    config['discharge_test_parameters']['V_MIN'] = float(input('Tensión objetivo (V): '))
                    if config['battery']['V_LIM_LOW'] <= config['discharge_test_parameters']['V_MIN'] <= config['battery']['V_LIM_HIGH']:
                        break
                    else:
                        print('¡Introduce un valor dentro de los límites de la batería!')
                except ValueError:
                    print('¡Introduce un valor válido!')
            while True:
                try:
                    config['discharge_test_parameters']['SOC_MIN'] = float(input('SOC objetivo (%): '))
                    if config['battery']['SOC_LIM_LOW'] <= config['discharge_test_parameters']['SOC_MIN'] <= config['battery']['SOC_LIM_HIGH']:
                        break
                    else:
                        print('¡Introduce un valor dentro de los límites de la batería!')
                except ValueError:
                    print('¡Introduce un valor válido!')
            while True:
                try:
                    config['discharge_test_parameters']['dischargeCurr'] = float(input('Intensidad de descarga (A): '))
                    if (0 <= config['discharge_test_parameters']['dischargeCurr'] <= config['battery']['I_LIM_HIGH']) and (0 <= config['discharge_test_parameters']['dischargeCurr'] <= config['discharge_test_parameters']['parallelLoads']*4):
                        break
                    else:
                        print('¡Introduce un valor dentro de los límites correctos!')
                except ValueError:
                    print('¡Introduce un valor válido!')
            while True:
                try:
                    config['discharge_test_parameters']['dischargeStep'] = float(input('Escalones de descarga (%): '))
                    if 0 <= config['discharge_test_parameters']['dischargeStep'] <= 100:
                        break
                    else:
                        print('¡Introduce un valor dentro del rango correcto!')
                except ValueError:
                    print('¡Introduce un valor válido!')
            while True:
                try:
                    config['discharge_test_parameters']['relaxPeriod'] = float(input('Periodo de relajación (s): '))
                    if 0 <= config['discharge_test_parameters']['relaxPeriod']:
                        break
                    else:
                        print('¡Introduce un valor válido!')
                except ValueError:
                    print('¡Introduce un tiempo mayor a 0 segundos!')
            while True:
                try:
                    config['discharge_test_parameters']['samplePeriod'] = float(input('Periodo de muestreo (s): '))
                    if 2 <= config['discharge_test_parameters']['samplePeriod']:
                        break
                    else:
                        print('¡Introduce un tiempo mayor a 2 segundos!')
                except ValueError:
                    print('¡Introduce un valor válido!')
                    
            saveDefault(config)
                    
    if op == 2:
        showParam(config)

        print('____PARÁMETROS DE LA CARGA___')
        print('Tensión límite de carga a corriente constante (V): ', config['charge_test_parameters']['V_LIM_CC'])
        print('Intensidad umbral de fin de carga (A): ', config['charge_test_parameters']['I_UMB'])
        print('Intensidad de carga (A): ', config['charge_test_parameters']['chargeCurr'])
        print('Escalones de carga (%): ', config['charge_test_parameters']['chargeStep'])
        print('Periodo de relajación (s): ', config['charge_test_parameters']['relaxPeriod'])
        print('Periodo de muestreo (s): ', config['charge_test_parameters']['samplePeriod'])
        print()
        
        while(True):
            default_ = input('Parametros por defecto [1] / Cambiar parametros [0]: ')
            if default_=='0' or default_=='1':
                break
            else:
                print('¡Introduce una opción válida!')
        
        if default_ == '0':
            while True:
                try:
                    config['charge_test_parameters']['V_LIM_CC'] = float(input('Tensión límite de carga a corriente constante (V): '))
                    if config['battery']['V_LIM_LOW'] <= config['charge_test_parameters']['V_LIM_CC'] <= config['battery']['V_LIM_HIGH']:
                        break
                    else:
                        print('¡Introduce un valor dentro de los límites de la batería!')
                except ValueError:
                    print('¡Introduce un valor válido!')
            while True:
                try:
                    config['charge_test_parameters']['I_UMB'] = float(input('Intensidad umbral de fin de carga (A): '))
                    if 0 <= config['charge_test_parameters']['I_UMB']:
                        break
                    else:
                        print('¡Introduce un valor válido!')
                except ValueError:
                    print('¡Introduce un valor válido!')
            while True:
                try:
                    config['charge_test_parameters']['chargeCurr'] = float(input('Intensidad de carga (A): '))
                    if (0 <= config['charge_test_parameters']['chargeCurr'] <= config['battery']['I_LIM_HIGH']) and (0 <= config['charge_test_parameters']['chargeCurr'] <= 10):
                        break
                    else:
                        print('¡Introduce un valor dentro de los límites correctos!')
                except ValueError:
                    print('¡Introduce un valor válido!')
            while True:
                try:
                    config['charge_test_parameters']['chargeStep'] = float(input('Escalones de carga (%): '))
                    if 0 <= config['charge_test_parameters']['chargeStep'] <= 100:
                        break
                    else:
                        print('¡Introduce un valor dentro del rango correcto!')
                except ValueError:
                    print('¡Introduce un valor válido!')
            while True:
                try:
                    config['charge_test_parameters']['relaxPeriod'] = float(input('Periodo de relajación (s): '))
                    if 0 <= config['charge_test_parameters']['relaxPeriod']:
                        break
                    else:
                        print('¡Introduce un valor válido!')
                except ValueError:
                    print('¡Introduce un valor válido!')
            while True:
                try:
                    config['charge_test_parameters']['samplePeriod'] = float(input('Periodo de muestreo (s): '))
                    if 2 <= config['charge_test_parameters']['samplePeriod']:
                        break
                    else:
                        print('¡Introduce un tiempo mayor a 2 segundos!')
                except ValueError:
                    print('¡Introduce un valor válido!')
            
            saveDefault(config)
            
    if op == 3:
        showParam(config)

        print('____PARÁMETROS DE LA DESCARGA___')
        print('Tensión objetivo (V): ', config['discharge_profile_parameters']['V_MIN'])
        print('SOC objetivo (%): ', config['discharge_profile_parameters']['SOC_MIN'])
        print('Periodo de muestreo (s): ', config['discharge_profile_parameters']['samplePeriod'])
        print('Número de cargas en paralelo: ', config['discharge_profile_parameters']['parallelLoads'])
        print()
        print('____PERFIL DE DESCARGA___')
        print('Nombre del archivo: ', config['path_files']['discharge_profile'])
        print()

        while(True):
            default_ = input('Parametros por defecto [1] / Cambiar parametros [0]: ')
            if default_=='0' or default_=='1':
                break
            else:
                print('¡Introduce una opción válida!')
        
        if default_ == '0':
            while True:
                try:
                    config['discharge_profile_parameters']['parallelLoads'] = int(input('Número de cargas en paralelo [1 - 3]: '))
                    if 1 <= config['discharge_profile_parameters']['parallelLoads'] <= 3:
                        break
                    else:
                        print('¡Introduce un entero entre 1 y 3!')
                except ValueError:
                    print('¡Introduce un valor válido!')
            while True:
                try:
                    config['discharge_profile_parameters']['V_MIN'] = float(input('Tensión objetivo (V): '))
                    if config['battery']['V_LIM_LOW'] <= config['discharge_profile_parameters']['V_MIN'] <= config['battery']['V_LIM_HIGH']:
                        break
                    else:
                        print('¡Introduce un valor dentro de los límites de la batería!')
                except ValueError:
                    print('¡Introduce un valor válido!')
            while True:
                try:
                    config['discharge_profile_parameters']['SOC_MIN'] = float(input('SOC objetivo (%): '))
                    if config['battery']['SOC_LIM_LOW'] <= config['discharge_profile_parameters']['SOC_MIN'] <= config['battery']['SOC_LIM_HIGH']:
                        break
                    else:
                        print('¡Introduce un valor dentro de los límites de la batería!')
                except ValueError:
                    print('¡Introduce un valor válido!')
            while True:
                try:
                    config['discharge_profile_parameters']['samplePeriod'] = float(input('Periodo de muestreo (s): '))
                    if 2 <= config['charge_test_parameters']['samplePeriod']:
                        break
                    else:
                        print('¡Introduce un tiempo mayor a 2 segundos!')
                except ValueError:
                    print('¡Introduce un valor válido!')
            while True:
                file_name = input('Nombre del archivo: ')
                if os.path.exists(os.path.join(parentDirectory, "input_files", file_name)):
                    config['path_files']['discharge_profile'] = file_name
                    break
                else:
                    print('¡Introduce el nombre de un fichero existente!')
                    
            saveDefault(config)
            
    if op == 4:
        showParam(config)

        print('____PARÁMETROS DE LA CARGA___')
        print('Tensión límite de carga a corriente constante (V): ', config['charge_profile_parameters']['V_LIM_CC'])
        print('Intensidad umbral de fin de carga (A): ', config['charge_profile_parameters']['I_UMB'])
        print('Periodo de muestreo (s): ', config['charge_profile_parameters']['samplePeriod'])
        print()
        print('____PERFIL DE DESCARGA___')
        print('Nombre del archivo: ', config['path_files']['charge_profile'])
        print()
        
        while(True):
            default_ = input('Parametros por defecto [1] / Cambiar parametros [0]: ')
            if default_=='0' or default_=='1':
                break
            else:
                print('¡Introduce una opción válida!')
        
        if default_ == '0':
            while True:
                try:
                    config['charge_profile_parameters']['V_LIM_CC'] = float(input('Tensión límite de carga a corriente constante (V): '))
                    if config['battery']['V_LIM_LOW'] <= config['charge_profile_parameters']['V_LIM_CC'] <= config['battery']['V_LIM_HIGH']:
                        break
                    else:
                        print('¡Introduce un valor dentro de los límites de la batería!')
                except ValueError:
                    print('¡Introduce un valor válido!')
            while True:
                try:
                    config['charge_profile_parameters']['I_UMB'] = float(input('Intensidad umbral de fin de carga (A): '))
                    if 0 <= config['charge_profile_parameters']['I_UMB']:
                        break
                    else:
                        print('¡Introduce un valor válido!')
                except ValueError:
                    print('¡Introduce un valor válido!')
            while True:
                try:
                    config['charge_profile_parameters']['samplePeriod'] = float(input('Periodo de muestreo (s): '))
                    if 2 <= config['charge_profile_parameters']['samplePeriod']:
                        break
                    else:
                        print('¡Introduce un tiempo mayor a 2 segundos!')
                except ValueError:
                    print('¡Introduce un valor válido!')
            while True:
                file_name = input('Nombre del archivo: ')
                if os.path.exists(os.path.join(parentDirectory, "input_files", file_name)):
                    config['path_files']['charge_profile'] = file_name
                    break
                else:
                    print('¡Introduce el nombre de un fichero existente!')
                    
            saveDefault(config)
            
    if op == 5:
        showParam(config)

        print('____PARÁMETROS DE LA DESCARGA___')
        print('Tensión objetivo (V): ', config['discharge_constant_parameters']['V_MIN'])
        print('SOC objetivo (%): ', config['discharge_constant_parameters']['SOC_MIN'])
        print('Intensidad de descarga (A): ', config['discharge_constant_parameters']['dischargeCurr'])
        print('Periodo de muestreo (s): ', config['discharge_constant_parameters']['samplePeriod'])
        print('Número de cargas en paralelo: ', config['discharge_constant_parameters']['parallelLoads'])
        print()

        while(True):
            default_ = input('Parametros por defecto [1] / Cambiar parametros [0]: ')
            if default_=='0' or default_=='1':
                break
            else:
                print('¡Introduce una opción válida!')
        
        if default_ == '0':
            while True:
                try:
                    config['discharge_constant_parameters']['parallelLoads'] = int(input('Número de cargas en paralelo [1 - 3]: '))
                    if 1 <= config['discharge_constant_parameters']['parallelLoads'] <= 3:
                        break
                    else:
                        print('¡Introduce un entero entre 1 y 3!')
                except ValueError:
                    print('¡Introduce un valor válido!')
            while True:
                try:
                    config['discharge_constant_parameters']['V_MIN'] = float(input('Tensión objetivo (V): '))
                    if config['battery']['V_LIM_LOW'] <= config['discharge_constant_parameters']['V_MIN'] <= config['battery']['V_LIM_HIGH']:
                        break
                    else:
                        print('¡Introduce un valor dentro de los límites de la batería!')
                except ValueError:
                    print('¡Introduce un valor válido!')
            while True:
                try:
                    config['discharge_constant_parameters']['SOC_MIN'] = float(input('SOC objetivo (%): '))
                    if config['battery']['SOC_LIM_LOW'] <= config['discharge_constant_parameters']['SOC_MIN'] <= config['battery']['SOC_LIM_HIGH']:
                        break
                    else:
                        print('¡Introduce un valor dentro de los límites de la batería!')
                except ValueError:
                    print('¡Introduce un valor válido!')
            while True:
                try:
                    config['discharge_constant_parameters']['dischargeCurr'] = float(input('Intensidad de descarga (A): '))
                    if (0 <= config['discharge_constant_parameters']['dischargeCurr'] <= config['battery']['I_LIM_HIGH']) and (0 <= config['discharge_constant_parameters']['dischargeCurr'] <= config['discharge_constant_parameters']['parallelLoads']*4):
                        break
                    else:
                        print('¡Introduce un valor dentro de los límites correctos!')
                except ValueError:
                    print('¡Introduce un valor válido!')
            while True:
                try:
                    config['discharge_constant_parameters']['samplePeriod'] = float(input('Periodo de muestreo (s): '))
                    if 2 <= config['discharge_constant_parameters']['samplePeriod']:
                        break
                    else:
                        print('¡Introduce un tiempo mayor a 2 segundos!')
                except ValueError:
                    print('¡Introduce un valor válido!')
                    
            saveDefault(config)
            
    if op == 6:
        showParam(config)

        print('____PARÁMETROS DE LA CARGA___')
        print('Tensión límite de carga a corriente constante (V): ', config['charge_constant_parameters']['V_LIM_CC'])
        print('Intensidad umbral de fin de carga (A): ', config['charge_constant_parameters']['I_UMB'])
        print('Intensidad de carga (A): ', config['charge_constant_parameters']['chargeCurr'])
        print('Periodo de muestreo (s): ', config['charge_constant_parameters']['samplePeriod'])
        print()
        
        while(True):
            default_ = input('Parametros por defecto [1] / Cambiar parametros [0]: ')
            if default_=='0' or default_=='1':
                break
            else:
                print('¡Introduce una opción válida!')
        
        if default_ == '0':
            while True:
                try:
                    config['charge_constant_parameters']['V_LIM_CC'] = float(input('Tensión límite de carga a corriente constante (V): '))
                    if config['battery']['V_LIM_LOW'] <= config['charge_constant_parameters']['V_LIM_CC'] <= config['battery']['V_LIM_HIGH']:
                        break
                    else:
                        print('¡Introduce un valor dentro de los límites de la batería!')
                except ValueError:
                    print('¡Introduce un valor válido!')
            while True:
                try:
                    config['charge_constant_parameters']['I_UMB'] = float(input('Intensidad umbral de fin de carga (A): '))
                    if 0 <= config['charge_constant_parameters']['I_UMB']:
                        break
                    else:
                        print('¡Introduce un valor válido!')
                except ValueError:
                    print('¡Introduce un valor válido!')
            while True:
                try:
                    config['charge_constant_parameters']['chargeCurr'] = float(input('Intensidad de carga (A): '))
                    if (0 <= config['charge_constant_parameters']['chargeCurr'] <= config['battery']['I_LIM_HIGH']) and (0 <= config['charge_constant_parameters']['chargeCurr'] <= 10):
                        break
                    else:
                        print('¡Introduce un valor dentro de los límites correctos!')
                except ValueError:
                    print('¡Introduce un valor válido!')
            while True:
                try:
                    config['charge_constant_parameters']['samplePeriod'] = float(input('Periodo de muestreo (s): '))
                    if 2 <= config['discharge_constant_parameters']['samplePeriod']:
                        break
                    else:
                        print('¡Introduce un tiempo mayor a 2 segundos!')
                except ValueError:
                    print('¡Introduce un valor válido!')
                    
            saveDefault(config)

    if op == 7:
        showParam(config)

        print('____PARÁMETROS DEL SISTEMA DE FV___')
        print('Performance Ratio: ', config['PV_parameters']['performanceRatio'])
        print('Potencia instalada (W): ', config['PV_parameters']['installedPotency'])
        print('Radiación estandar (W): ', config['PV_parameters']['STCRadiation'])
        print('Irradiancia máxima (W/m2): ', config['PV_parameters']['maxIrradiance'])
        print('Consumo máximo (W): ', config['PV_parameters']['maxConsumtion'])
        print('Intensidad máxima de la carga (A): ', config['PV_parameters']['maxLoadCurrent'])
        print('Intensidad máxima de la fuente (A): ', config['PV_parameters']['maxPSCurrent'])
        print('Escala de tiempo de la fuente (s): ', config['PV_parameters']['timeSCL_PS'])
        print('Escala de tiempo de la carga (s): ', config['PV_parameters']['timeSCL_Load'])
        print()
        print('____CURVAS___')
        print('Curva de irradiancia: ', config['path_files']['irradiance_curve'])
        print('Curva de consumo: ', config['path_files']['consumtion_curve'])
        print()
        
        while(True):
            default_ = input('Parametros por defecto [1] / Cambiar parametros [0]: ')
            if default_=='0' or default_=='1':
                break
            else:
                print('¡Introduce una opción válida!')
        
        if default_ == '0':
            while True:
                try:
                    config['PV_parameters']['performanceRatio'] = float(input('Performance Ratio [0 - 1]: '))
                    if 0 <= config['PV_parameters']['performanceRatio'] <= 1:
                        break
                    else:
                        print('¡Introduce un valor entre 0 y 1!')
                except ValueError:
                    print('¡Introduce un valor válido!')
            while True:
                try:
                    config['PV_parameters']['installedPotency'] = float(input('Potencia instalada (W): '))
                    if 0 < config['PV_parameters']['installedPotency']:
                        break
                    else:
                        print('¡Introduce un valor mayor que 0!')
                except ValueError:
                    print('¡Introduce un valor válido!')
            while True:
                try:
                    config['PV_parameters']['STCRadiation'] = float(input('Radiación estandar (W) [valor típico: 1000]: '))
                    if 0 < config['PV_parameters']['STCRadiation']:
                        break
                    else:
                        print('¡Introduce un valor mayor que 0!')
                except ValueError:
                    print('¡Introduce un valor válido!')
            while True:
                try:
                    config['PV_parameters']['maxIrradiance'] = input('Irradiancia máxima (W/m2) [AUTO / valor]: ')
                    if (0 < float(config['PV_parameters']['maxIrradiance'])) or (config['PV_parameters']['maxIrradiance'] == 'AUTO'):
                        break
                    else:
                        print('¡Introduce un valor mayor que 0 o "AUTO"!')
                except ValueError:
                    print('¡Introduce un valor válido!')
            while True:
                try:
                    config['PV_parameters']['maxConsumtion'] = input('Consumo máximo (W) [AUTO / valor]: ')
                    if (0 < float(config['PV_parameters']['maxConsumtion'])) or (config['PV_parameters']['maxConsumtion'] == 'AUTO'):
                        break
                    else:
                        print('¡Introduce un valor mayor que 0 o "AUTO"!')
                except ValueError:
                    print('¡Introduce un valor válido!')
            while True:
                try:
                    config['PV_parameters']['maxPSCurrent'] = float(input('Intensidad máxima de la fuente (A): '))
                    if (0 <= config['PV_parameters']['maxPSCurrent'] <= config['battery']['I_LIM_HIGH']) and (0 <= config['PV_parameters']['maxPSCurrent'] <= 10):
                        break
                    else:
                        print('¡Introduce un valor dentro de los límites correctos!')
                except ValueError:
                    print('¡Introduce un valor válido!')
            while True:
                try:
                    config['PV_parameters']['maxLoadCurrent'] = float(input('Intensidad máxima de la carga (A): '))
                    if (0 <= config['PV_parameters']['maxLoadCurrent'] <= config['battery']['I_LIM_HIGH']) and (0 <= config['PV_parameters']['maxLoadCurrent'] <= 4):
                        break
                    else:
                        print('¡Introduce un valor dentro de los límites correctos!')
                except ValueError:
                    print('¡Introduce un valor válido!')
            while True:
                try:
                    config['PV_parameters']['timeSCL_PS'] = input('Escala de tiempo de la fuente (s) [AUTO / valor]: ')
                    if (0 < float(config['PV_parameters']['timeSCL_PS'])) or (config['PV_parameters']['timeSCL_PS'] == 'AUTO'):
                        break
                    else:
                        print('¡Introduce un valor mayor que 0 o "AUTO"!')
                except ValueError:
                    print('¡Introduce un valor válido!')
            while True:
                try:
                    config['PV_parameters']['timeSCL_Load'] = input('Escala de tiempo de la carga (s) [AUTO / valor]: ')
                    if (0 < float(config['PV_parameters']['timeSCL_Load'])) or (config['PV_parameters']['timeSCL_Load'] == 'AUTO'):
                        break
                    else:
                        print('¡Introduce un valor mayor que 0 o "AUTO"!')
                except ValueError:
                    print('¡Introduce un valor válido!')
            while True:
                file_name = input('Curva de irradiancia (nombre del archivo): ')
                if os.path.exists(os.path.join(parentDirectory, "input_files", file_name)):
                    config['path_files']['irradiance_curve'] = file_name
                    break
                else:
                    print('¡Introduce el nombre de un fichero existente!')
            while True:
                file_name = input('Curva de consumo (nombre del archivo): ')
                if os.path.exists(os.path.join(parentDirectory, "input_files", file_name)):
                    config['path_files']['consumtion_curve'] = file_name
                    break
                else:
                    print('¡Introduce el nombre de un fichero existente!')
                    
            saveDefault(config)
            
    if op == 8:
        showParam(config)
        
        print('____CURVAS___')
        print('Perfil de generación: ', config['path_files']['generation_profile'])
        print('Perfil de consumo: ', config['path_files']['consumtion_profile'])
        print()
        
        while(True):
            default_ = input('Parametros por defecto [1] / Cambiar parametros [0]: ')
            if default_=='0' or default_=='1':
                break
            else:
                print('¡Introduce una opción válida!')
        
        if default_ == '0':
            while True:
                file_name = input('Perfil de generación (nombre del archivo): ')
                if os.path.exists(os.path.join(parentDirectory, "input_files", file_name)):
                    config['path_files']['generation_profile'] = file_name
                    break
                else:
                    print('¡Introduce el nombre de un fichero existente!')
            while True:
                file_name = input('Perfil de consumo (nombre del archivo): ')
                if os.path.exists(os.path.join(parentDirectory, "input_files", file_name)):
                    config['path_files']['consumtion_profile'] = file_name
                    break
                else:
                    print('¡Introduce el nombre de un fichero existente!')
                    
            saveDefault(config)
            
    if op == 10:
        print('____PARÁMETROS DE LA CALIBRACIÓN___')
        print('Potenciometro: ', config['calibration_parameters']['potentiometer'])
        print('Valor: ', config['calibration_parameters']['value'])
        print()
        
        while(True):
            default_ = input('Parametros por defecto [1] / Cambiar parametros [0]: ')
            if default_=='0' or default_=='1':
                break
            else:
                print('¡Introduce una opción válida!')
        
        if default_ == '0':
            while True:
                try:
                    config['calibration_parameters']['potentiometer'] = int(input('Potenciometro [1 - 5]: '))
                    if 1 <= config['calibration_parameters']['potentiometer'] <= 5:
                        break
                    else:
                        print('¡Introduce un entero entre 1 y 5!')
                except ValueError:
                    print('¡Introduce un valor válido!')
            while True:
                try:
                    config['calibration_parameters']['value'] = int(input('Valor [0 - 255]: '))
                    if 0 <= config['calibration_parameters']['value'] <= 255:
                        break
                    else:
                        print('¡Introduce un entero entre 0 y 255!')
                except ValueError:
                    print('¡Introduce un valor válido!')
        
            saveDefault(config)                  
                    
    if op == 15:
        print('____PARÁMETROS DE LA BATERIA___')
        print('Capacidad (Ah): ', config['battery']['capacity'])
        print('SOC inicial (%): ', config['battery']['initSOC'])
        print('Tensión límite máxima (V): ', config['battery']['V_LIM_HIGH'])
        print('Tensión límite mínima (V): ', config['battery']['V_LIM_LOW'])
        print('SOC límite máximo (%): ', config['battery']['SOC_LIM_HIGH'])
        print('SOC límite mínimo (%): ', config['battery']['SOC_LIM_LOW'])
        print()
        
        while(True):
            default_ = input('Parametros por defecto [1] / Cambiar parametros [0]: ')
            if default_=='0' or default_=='1':
                break
            else:
                print('¡Introduce una opción válida!')
        
        if default_ == '0':
            while True:
                try:
                    config['battery']['capacity'] = float(input('Capacidad (Ah): '))
                    if 0 < config['battery']['capacity']:
                        break
                    else:
                        print('¡Introduce un valor mayor que 0!')
                except ValueError:
                    print('¡Introduce un valor válido!')
            while True:
                try:
                    config['battery']['initSOC'] = float(input('SOC inicial (%): '))
                    if 0 <= config['battery']['initSOC'] <= 100:
                        break
                    else:
                        print('¡Introduce un valor entre 0 y 100!')
                except ValueError:
                    print('¡Introduce un valor válido!')
            while True:
                try:
                    config['battery']['V_LIM_HIGH'] = float(input('Tensión límite máxima (V): '))
                    if 0 < config['battery']['V_LIM_HIGH']:
                        break
                    else:
                        print('¡Introduce un valor mayor que 0!')
                except ValueError:
                    print('¡Introduce un valor válido!')
            while True:
                try:
                    config['battery']['V_LIM_LOW'] = float(input('Tensión límite mínima (V): '))
                    if 0 <= config['battery']['V_LIM_LOW']:
                        break
                    else:
                        print('¡Introduce un valor mayor o igual a 0!')
                except ValueError:
                    print('¡Introduce un valor válido!')
            while True:
                try:
                    config['battery']['SOC_LIM_HIGH'] = float(input('SOC límite máximo (%): '))
                    if 0 <= config['battery']['SOC_LIM_HIGH'] <= 100:
                        break
                    else:
                        print('¡Introduce un valor entre 0 y 100!')
                except ValueError:
                    print('¡Introduce un valor válido!')
            while True:
                try:
                    config['battery']['SOC_LIM_LOW'] = float(input('SOC límite mínimo (%): '))
                    if 0 <= config['battery']['SOC_LIM_LOW'] <= 100:
                        break
                    else:
                        print('¡Introduce un valor entre 0 y 100!')
                except ValueError:
                    print('¡Introduce un valor válido!')

            saveDefault(config)

    if op == 16:
        print('____PARÁMETROS DE LA LECTURA DE TENSIÓN___')
        print('Factor de escala: ', config['read_voltage']['scaleFactor'])
        print('Resistencia 1 del divisor de tensión (ohms): ', config['read_voltage']['r1'])
        print('Resistencia 2 del divisor de tensión (ohms): ', config['read_voltage']['r2'])
        print('Tensión del zener (V): ', config['read_voltage']['zenerVoltage'])
        print()
        
        while(True):
            default_ = input('Parametros por defecto [1] / Cambiar parametros [0]: ')
            if default_=='0' or default_=='1':
                break
            else:
                print('¡Introduce una opción válida!')
        
        if default_ == '0':
            while True:
                try:
                    config['read_voltage']['scaleFactor'] = float(input('Factor de escala: '))
                    if 0 < config['read_voltage']['scaleFactor'] < 1:
                        break
                    else:
                        print('¡Introduce un valor entre 0 y 1!')
                except ValueError:
                    print('¡Introduce un valor válido!')
            while True:
                try:
                    config['read_voltage']['r1'] = float(input('Resistencia 1 del divisor de tensión (ohms): '))
                    if 0 <= config['read_voltage']['r1']:
                        break
                    else:
                        print('¡Introduce un valor mayo o igual a 0')
                except ValueError:
                    print('¡Introduce un valor válido!')
            while True:
                try:
                    config['read_voltage']['r2'] = float(input('Resistencia 2 del divisor de tensión (ohms): '))
                    if 0 <= config['read_voltage']['r2']:
                        break
                    else:
                        print('¡Introduce un valor mayor o igual a 0')
                except ValueError:
                    print('¡Introduce un valor válido!')
            while True:
                try:
                    config['read_voltage']['zenerVoltage'] = float(input('Tensión del zener (V): '))
                    if 0 <= config['read_voltage']['zenerVoltage']:
                        break
                    else:
                        print('¡Introduce un valor mayor o igual a 0')
                except ValueError:
                    print('¡Introduce un valor válido!')

            saveDefault(config)

def showParam(config):
    print('____PARÁMETROS DE LA BATERIA___')
    print('Capacidad (Ah): ', config['battery']['capacity'])
    print('SOC inicial (%): ', config['battery']['initSOC'])
    print('Tensión límite máxima (V): ', config['battery']['V_LIM_HIGH'])
    print('Tensión límite mínima (V): ', config['battery']['V_LIM_LOW'])
    print('SOC límite máximo (%): ', config['battery']['SOC_LIM_HIGH'])
    print('SOC límite mínimo (%): ', config['battery']['SOC_LIM_LOW'])
    print('Intensidad límite (A): ', config['battery']['I_LIM_HIGH'])
    print()
    print('____PARÁMETROS DE LA LECTURA DE TENSIÓN___')
    print('Factor de escala: ', config['read_voltage']['scaleFactor'])
    print('Resistencia 1 del divisor de tensión (ohms): ', config['read_voltage']['r1'])
    print('Resistencia 2 del divisor de tensión (ohms): ', config['read_voltage']['r2'])
    print('Tensión del zener (V): ', config['read_voltage']['zenerVoltage'])
    print()