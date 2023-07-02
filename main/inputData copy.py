import json

def saveDefault(config):
    save = input('Guardar cambios como valores por defecto -> Si [1] / No [0]: ')
    if save == '1':
        with open('config.json', 'w') as file:
            json.dump(config, file)

def inputData(op, config):
    if op == 1:
        print('____PARÁMETROS DE LA BATERIA___')
        print('SOC inicial (%): ', config['battery']['initSOC'])
        print()
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
                    config['battery']['initSOC'] = float(input('SOC inicial (%): '))
                    break
                except ValueError:
                    print('¡Introduce un valor válido!')
            while True:
                try:
                    config['discharge_test_parameters']['V_MIN'] = float(input('Tensión objetivo (V): '))
                    break
                except ValueError:
                    print('¡Introduce un valor válido!')
            while True:
                try:
                    config['discharge_test_parameters']['SOC_MIN'] = float(input('SOC objetivo (%): '))
                    break
                except ValueError:
                    print('¡Introduce un valor válido!')
            while True:
                try:
                    config['discharge_test_parameters']['dischargeCurr'] = float(input('Intensidad de descarga (A): '))
                    break
                except ValueError:
                    print('¡Introduce un valor válido!')
            while True:
                try:
                    config['discharge_test_parameters']['dischargeStep'] = float(input('Escalones de descarga (%): '))
                    break
                except ValueError:
                    print('¡Introduce un valor válido!')
            while True:
                try:
                    config['discharge_test_parameters']['relaxPeriod'] = float(input('Periodo de relajación (s): '))
                    break
                except ValueError:
                    print('¡Introduce un valor válido!')
            while True:
                try:
                    config['discharge_test_parameters']['samplePeriod'] = float(input('Periodo de muestreo (s): '))
                    break
                except ValueError:
                    print('¡Introduce un valor válido!')
            while True:
                try:
                    config['discharge_test_parameters']['parallelLoads'] = int(input('Número de cargas en paralelo [1 - 3]: '))
                    if 1 <= op <= 3:
                        break
                    else:
                        print('¡Introduce un entero entre 1 y 3!')
                except ValueError:
                    print('¡Introduce un valor válido!')
                    
            saveDefault(config)
                    
    if op == 2:
        print('____PARÁMETROS DE LA BATERIA___')
        print('SOC inicial (%): ', config['battery']['initSOC'])
        print()
        print('____PARÁMETROS DE LA CARGA___')
        print('Tensión límite de carga a corriente constante (V): ', config['charge_test_parameters']['V_LIM_CC'])
        print('Intensidad umbral de fin de carga (A): ', config['charge_test_parameters']['I_UMB'])
        print('Intensidad de carga (A): ', config['charge_test_parameters']['chargeCurr'])
        print('Escalones de carga (%): ', config['charge_test_parameters']['chargeStep'])
        print('Periodo de relajación (s): ', config['charge_test_parameters']['relaxPeriod'])
        print('Periodo de muestreo (s): ', config['charge_test_parameters']['samplePeriod'])
        print()
        
        default_ = input('Parametros por defecto [1] / Cambiar parametros [0]: ')
        
        if default_ == '0':
            config['battery']['initSOC'] = float(input('SOC inicial (%): '))
            config['charge_test_parameters']['V_LIM_CC'] = float(input('Tensión límite de carga a corriente constante (V): '))
            config['charge_test_parameters']['I_UMB'] = float(input('Intensidad umbral de fin de carga (A): '))
            config['charge_test_parameters']['chargeCurr'] = float(input('Intensidad de carga (A): '))
            config['charge_test_parameters']['chargeStep'] = float(input('Escalones de carga (%): '))
            config['charge_test_parameters']['relaxPeriod'] = float(input('Periodo de relajación (s): '))
            config['charge_test_parameters']['samplePeriod'] = float(input('Periodo de muestreo (s): '))
            saveDefault(config)
            
    if op == 3:
        print('____PARÁMETROS DE LA BATERIA___')
        print('SOC inicial (%): ', config['battery']['initSOC'])
        print()
        print('____PARÁMETROS DE LA DESCARGA___')
        print('Tensión objetivo (V): ', config['discharge_profile_parameters']['V_MIN'])
        print('SOC objetivo (%): ', config['discharge_profile_parameters']['SOC_MIN'])
        print('Periodo de muestreo (s): ', config['discharge_profile_parameters']['samplePeriod'])
        print('Número de cargas en paralelo: ', config['discharge_profile_parameters']['parallelLoads'])
        print()
        print('____PERFIL DE DESCARGA___')
        print('Nombre del archivo: ', config['path_files']['discharge_profile'])
        print()

        default_ = input('Parametros por defecto [1] / Cambiar parametros [0]: ')
        
        if default_ == '0':
            config['battery']['initSOC'] = float(input('SOC inicial (%): '))
            config['discharge_profile_parameters']['V_MIN'] = float(input('Tensión objetivo (V): '))
            config['discharge_profile_parameters']['SOC_MIN'] = float(input('SOC objetivo (%): '))
            config['discharge_profile_parameters']['samplePeriod'] = float(input('Periodo de muestreo (s): '))
            config['discharge_profile_parameters']['parallelLoads'] = int(input('Número de cargas en paralelo [1 - 3]: '))
            config['path_files']['discharge_profile'] = input('Nombre del archivo: ')
            saveDefault(config)
            
    if op == 4:
        print('____PARÁMETROS DE LA BATERIA___')
        print('SOC inicial (%): ', config['battery']['initSOC'])
        print()
        print('____PARÁMETROS DE LA CARGA___')
        print('Tensión límite de carga a corriente constante (V): ', config['charge_profile_parameters']['V_LIM_CC'])
        print('Intensidad umbral de fin de carga (A): ', config['charge_profile_parameters']['I_UMB'])
        print('Periodo de muestreo (s): ', config['charge_profile_parameters']['samplePeriod'])
        print()
        print('____PERFIL DE DESCARGA___')
        print('Nombre del archivo: ', config['path_files']['charge_profile'])
        print()
        
        default_ = input('Parametros por defecto [1] / Cambiar parametros [0]: ')
        
        if default_ == '0':
            config['battery']['initSOC'] = float(input('SOC inicial (%): '))
            config['charge_profile_parameters']['V_LIM_CC'] = float(input('Tensión límite de carga a corriente constante (V): '))
            config['charge_profile_parameters']['I_UMB'] = float(input('Intensidad umbral de fin de carga (A): '))
            config['charge_profile_parameters']['samplePeriod'] = float(input('Periodo de muestreo (s): '))
            config['path_files']['discharge_profile'] = input('Nombre del archivo: ')
            saveDefault(config) 
            
    if op == 5:
        print('____PARÁMETROS DE LA BATERIA___')
        print('SOC inicial (%): ', config['battery']['initSOC'])
        print()
        print('____PARÁMETROS DE LA DESCARGA___')
        print('Tensión objetivo (V): ', config['discharge_constant_parameters']['V_MIN'])
        print('SOC objetivo (%): ', config['discharge_constant_parameters']['SOC_MIN'])
        print('Intensidad de descarga (A): ', config['discharge_constant_parameters']['dischargeCurr'])
        print('Periodo de muestreo (s): ', config['discharge_constant_parameters']['samplePeriod'])
        print('Número de cargas en paralelo: ', config['discharge_constant_parameters']['parallelLoads'])
        print()

        default_ = input('Parametros por defecto [1] / Cambiar parametros [0]: ')
        
        if default_ == '0':
            config['battery']['initSOC'] = float(input('SOC inicial (%): '))
            config['discharge_constant_parameters']['V_MIN'] = float(input('Tensión objetivo (V): '))
            config['discharge_constant_parameters']['SOC_MIN'] = float(input('SOC objetivo (%): '))
            config['discharge_constant_parameters']['dischargeCurr'] = float(input('Intensidad de descarga (A): '))
            config['discharge_constant_parameters']['samplePeriod'] = float(input('Periodo de muestreo (s): '))
            config['discharge_constant_parameters']['parallelLoads'] = int(input('Número de cargas en paralelo [1 - 3]: '))
            saveDefault(config)
            
    if op == 6:
        print('____PARÁMETROS DE LA BATERIA___')
        print('SOC inicial (%): ', config['battery']['initSOC'])
        print()
        print('____PARÁMETROS DE LA CARGA___')
        print('Tensión límite de carga a corriente constante (V): ', config['charge_constant_parameters']['V_LIM_CC'])
        print('Intensidad umbral de fin de carga (A): ', config['charge_constant_parameters']['I_UMB'])
        print('Intensidad de carga (A): ', config['charge_constant_parameters']['chargeCurr'])
        print('Periodo de muestreo (s): ', config['charge_constant_parameters']['samplePeriod'])
        print()
        
        default_ = input('Parametros por defecto [1] / Cambiar parametros [0]: ')
        
        if default_ == '0':
            config['battery']['initSOC'] = float(input('SOC inicial (%): '))
            config['charge_constant_parameters']['V_LIM_CC'] = float(input('Tensión límite de carga a corriente constante (V): '))
            config['charge_constant_parameters']['I_UMB'] = float(input('Intensidad umbral de fin de carga (A): '))
            config['charge_constant_parameters']['chargeCurr'] = float(input('Intensidad de carga (A): '))
            config['charge_constant_parameters']['samplePeriod'] = float(input('Periodo de muestreo (s): '))
            saveDefault(config)  
            
    if op == 7:
        print('____PARÁMETROS DE LA BATERIA___')
        print('SOC inicial (%): ', config['battery']['initSOC'])
        print()
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
        
        default_ = input('Parametros por defecto [1] / Cambiar parametros [0]: ')
        
        if default_ == '0':
            config['battery']['initSOC'] = float(input('SOC inicial (%): '))
            config['PV_parameters']['performanceRatio'] = float(input('Performance Ratio [0 - 1]: '))
            config['PV_parameters']['installedPotency'] = float(input('Potencia instalada (W): '))
            config['PV_parameters']['STCRadiation'] = float(input('Radiación estandar (W) [valor típico: 1000]: '))
            config['PV_parameters']['maxIrradiance'] = input('Irradiancia máxima (W/m2) [AUTO / valor]: ')
            config['PV_parameters']['maxConsumtion'] = input('Consumo máximo (W) [AUTO / valor]: ')
            config['PV_parameters']['maxLoadCurrent'] = float(input('Intensidad máxima de la fuente (A): '))
            config['PV_parameters']['maxPSCurrent'] = float(input('Intensidad máxima de la carga (A): '))
            config['PV_parameters']['timeSCL_PS'] = input('Escala de tiempo de la fuente (s) [AUTO / valor]: ')
            config['PV_parameters']['timeSCL_Load'] = input('Escala de tiempo de la carga (s) [AUTO / valor]: ')
            config['path_files']['irradiance_curve'] = input('Curva de irradiancia (nombre del archivo): ')
            config['path_files']['consumtion_curve'] = input('Curva de consumo (nombre del archivo): ')
            saveDefault(config)
            
    if op == 8:
        print('____PARÁMETROS DE LA BATERIA___')
        print('SOC inicial (%): ', config['battery']['initSOC'])
        print()
        print('____CURVAS___')
        print('Curva de irradiancia: ', config['path_files']['irradiance_curve'])
        print('Curva de consumo: ', config['path_files']['consumtion_curve'])
        print()
        
        default_ = input('Parametros por defecto [1] / Cambiar parametros [0]: ')
        
        if default_ == '0':
            config['battery']['initSOC'] = float(input('SOC inicial (%): '))
            config['path_files']['irradiance_curve'] = input('Curva de irradiancia (nombre del archivo): ')
            config['path_files']['consumtion_curve'] = input('Curva de consumo (nombre del archivo): ')
            saveDefault(config)
            
    if op == 10:
        print('____PARÁMETROS DE LA CALIBRACIÓN___')
        print('Potenciometro: ', config['calibration_parameters']['potentiometer'])
        print('Valor: ', config['calibration_parameters']['value'])
        print()
        
        default_ = input('Parametros por defecto [1] / Cambiar parametros [0]: ')
        
        if default_ == '0':
            config['calibration_parameters']['potentiometer'] = int(input('Potenciometro [1 - 5]: '))
            config['calibration_parameters']['value'] = int(input('Valor [0 - 255]: '))
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
        print('____PARÁMETROS DE LA LECTURA DE TENSIÓN___')
        print('Factor de escala: ', config['read_voltage']['scaleFactor'])
        print('Resistencia 1 del divisor de tensión (ohms): ', config['read_voltage']['r1'])
        print('Resistencia 2 del divisor de tensión (ohms): ', config['read_voltage']['r2'])
        print('Tensión del zener (V): ', config['read_voltage']['zenerVoltage'])
        print()
        
        default_ = input('Parametros por defecto [1] / Cambiar parametros [0]: ')

        if default_ == '0':
            config['battery']['capacity'] = float(input('Capacidad (Ah): '))
            config['battery']['initSOC'] = float(input('SOC inicial (%): '))
            config['battery']['V_LIM_HIGH'] = float(input('Tensión límite máxima (V): '))
            config['battery']['V_LIM_LOW'] = float(input('Tensión límite mínima (V): '))
            config['battery']['SOC_LIM_HIGH'] = float(input('SOC límite máximo (%): '))
            config['battery']['SOC_LIM_LOW'] = float(input('SOC límite mínimo (%): '))
            config['read_voltage']['scaleFactor'] = float(input('Factor de escala: '))
            config['read_voltage']['r1'] = float(input('Resistencia 1 del divisor de tensión (ohms): '))
            config['read_voltage']['r2'] = float(input('Resistencia 2 del divisor de tensión (ohms): '))
            config['read_voltage']['zenerVoltage'] = float(input('Tensión del zener (V): '))
            saveDefault(config)
