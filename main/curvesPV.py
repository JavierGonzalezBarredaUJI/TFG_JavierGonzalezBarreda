import os
import json
from functions import seconds2hours
from functions import seconds2minutes
from functions import curve
from functions import curve3

def run(file_name, SCLtime):
    parentDirectory = os.getcwd()
    with open(file_name) as f:
        data = json.load(f)
    
    if SCLtime == 'h':
        seconds2hours(data['T'])
        curve(data['T'], data['SOC'], title='SOC vs t', name=os.path.join(parentDirectory, "output_files", "SOC.pdf"), x_axis='t (h)', y_axis='SOC (%)')
        curve(data['T'], data['V'], title='V vs t', name=os.path.join(parentDirectory, "output_files", "tension.pdf"), x_axis='t (h)', y_axis='Tensión (V)')
        curve3(data['T'], data['I_ps'], data['T'], data['I_load'], data['T'], data['I_bat'], title='I vs t', name=os.path.join(parentDirectory, "output_files", "intensidades.pdf"), 
                x_axis='t (h)', y_axis='Intensidad (A)', curve1='Intensidad fuente', curve2='Intensidad carga', curve3='Intensidad bateria')
    elif SCLtime == 'm':
        seconds2minutes(data['T'])
        curve(data['T'], data['SOC'], title='SOC vs t', name=os.path.join(parentDirectory, "output_files", "SOC.pdf"), x_axis='t (min)', y_axis='SOC (%)')
        curve(data['T'], data['V'], title='V vs t', name=os.path.join(parentDirectory, "output_files", "tension.pdf"), x_axis='t (min)', y_axis='Tensión (V)')
        curve3(data['T'], data['I_ps'], data['T'], data['I_load'], data['T'], data['I_bat'], title='I vs t', name=os.path.join(parentDirectory, "output_files", "intensidades.pdf"), 
                x_axis='t (min)', y_axis='Intensidad (A)', curve1='Intensidad fuente', curve2='Intensidad carga', curve3='Intensidad bateria')