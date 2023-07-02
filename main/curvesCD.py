import os
from functions import parseCurve
from functions import seconds2hours
from functions import seconds2minutes
from functions import curve
from functions import curve2
from functions import relaxVoltCharge
from functions import relaxVoltDischarge
from functions import writeRelax
from functions import voltageCapacityTransform 


def run(file_name):
    parentDirectory = os.getcwd()
    data = parseCurve(file_name)
    seconds2hours(data['T'])
    #seconds2minutes(data['T'])

    if file_name == os.path.join(parentDirectory, "output_files", "datos_descarga.csv"):
        curve(data['SOC'], data['V'], title='Curva de descarga', name=os.path.join(parentDirectory, "output_files", "curva_descarga.pdf"), x_axis='SOC (%)', y_axis='Tensión (V)')
        curve(data['T'], data['V'], title='V vs t', name=os.path.join(parentDirectory, "output_files", "descarga_tension_tiempo.pdf"), x_axis='t (h)', y_axis='Tensión (V)')
        curve(data['T'], data['SOC'], title='SOC vs t', name=os.path.join(parentDirectory, "output_files", "descarga_soc_tiempo.pdf"), x_axis='t (h)', y_axis='SOC (%)')
        Vrelax, SOCrelax = relaxVoltDischarge(data)
        writeRelax(Vrelax, SOCrelax, os.path.join(parentDirectory, "output_files", "datos_descarga_tension_relajada.csv"))
        curve(SOCrelax, Vrelax, title='Curva de descarga con tensiones relajadas', name=os.path.join(parentDirectory, "output_files", "descarga_tension_relajada.pdf"), x_axis='SOC (%)', y_axis='Tensión (V)')
        curve2(data['SOC'], data['V'], SOCrelax, Vrelax, title='Curva de descarga', name=os.path.join(parentDirectory, "output_files", "curva_comparacion_tensiones_descarga.pdf"), x_axis='SOC (%)', y_axis='Tensión (V)', curve1='No relajada', curve2='Relajada')
        Vtrans, c = voltageCapacityTransform(Vrelax, SOCrelax)
        curve(c, Vtrans, title='Curva de descarga Ah', name=os.path.join(parentDirectory, "output_files", "curva_descarga_Ah.pdf"), x_axis='Ah', y_axis='Tensión (V)')

    elif file_name == os.path.join(parentDirectory, "output_files", "datos_carga.csv"):
        curve(data['SOC'], data['V'], title='Curva de carga', name=os.path.join(parentDirectory, "output_files", "curva_carga.pdf"), x_axis='SOC (%)', y_axis='Tensión (V)')
        curve(data['T'], data['V'], title='V vs t', name=os.path.join(parentDirectory, "output_files", "carga_tension_tiempo.pdf"), x_axis='t (h)', y_axis='Tensión (V)')
        curve(data['T'], data['SOC'], title='SOC vs t', name=os.path.join(parentDirectory, "output_files", "carga_soc_tiempo.pdf"), x_axis='t (h)', y_axis='SOC (%)')
        Vrelax, SOCrelax = relaxVoltCharge(data)
        writeRelax(Vrelax, SOCrelax, os.path.join(parentDirectory, "output_files", "datos_carga_tension_relajada.csv"))
        curve(SOCrelax, Vrelax, title='Curva de carga con tensiones relajadas', name=os.path.join(parentDirectory, "output_files", "carga_tension_relajada.pdf"), x_axis='SOC (%)', y_axis='Tensión (V)')
        curve2(data['SOC'], data['V'], SOCrelax, Vrelax, title='Curva de carga', name=os.path.join(parentDirectory, "output_files", "curva_comparacion_tensiones_carga.pdf"), x_axis='SOC (%)', y_axis='Tensión (V)', curve1='No relajada', curve2='Relajada')
        Vtrans, c = voltageCapacityTransform(Vrelax, SOCrelax)
        curve(c, Vtrans, title='Curva de carga Ah', name=os.path.join(parentDirectory, "output_files", "curva_carga_Ah.pdf"), x_axis='Ah', y_axis='Tensión (V)')

    elif file_name == os.path.join(parentDirectory, "output_files", "datos_descarga_perfil.csv"):
        curve(data['SOC'], data['V'], title='Curva de descarga', name=os.path.join(parentDirectory, "output_files", "curva_descarga.pdf"), x_axis='SOC (%)', y_axis='Tensión (V)')
        curve(data['T'], data['V'], title='V vs t', name=os.path.join(parentDirectory, "output_files", "descarga_tension_tiempo.pdf"), x_axis='t (h)', y_axis='Tensión (V)')
        curve(data['T'], data['SOC'], title='SOC vs t', name=os.path.join(parentDirectory, "output_files", "descarga_soc_tiempo.pdf"), x_axis='t (h)', y_axis='SOC (%)')

    elif file_name == os.path.join(parentDirectory, "output_files", "datos_carga_perfil.csv"):
        curve(data['SOC'], data['V'], title='Curva de carga', name=os.path.join(parentDirectory, "output_files", "curva_carga.pdf"), x_axis='SOC (%)', y_axis='Tensión (V)')
        curve(data['T'], data['V'], title='V vs t', name=os.path.join(parentDirectory, "output_files", "carga_tension_tiempo.pdf"), x_axis='t (h)', y_axis='Tensión (V)')
        curve(data['T'], data['SOC'], title='SOC vs t', name=os.path.join(parentDirectory, "output_files", "carga_soc_tiempo.pdf"), x_axis='t (h)', y_axis='SOC (%)')