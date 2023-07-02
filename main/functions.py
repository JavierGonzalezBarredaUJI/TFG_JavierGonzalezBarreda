import os
import time
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


parentDirectory = os.getcwd()
b = 0
d1 = None
c = 0
d2 = None
err = 0
end = 0
t_ps = 0
t_load = 0
items_ps = 0
items_load = 0


def sendTimeLoad(data):
    global t_load
    global items_load
    t_load = data[0]
    items_load = data[1]


def sendTimePS(data):
    global t_ps
    global items_ps
    t_ps = data[0]
    items_ps = data[1]


def receiveTimeLoad():
    global t_ps
    global items_ps
    return t_ps, items_ps


def receiveTimePS():
    global t_load
    global items_load
    return t_load, items_load


def endSimulation(a):
    global end
    if a == 1:
        end = 1
    elif a == 'i':
        end = 0
    return end


def communicationError(a):
    global err
    if a == 1:
        err = 1
    elif a == 'i':
        err = 0
    return err


def warningPS(a, data):
    global b
    global d1
    if a == 'callback':
        b = 1
        d1 = data
    elif a == 'notcallback':
        b = 0
    elif a == 'ps':
        return b, d1

def warningLoad(a, data):
    global c
    global d2
    if a == 'callback':
        c = 1
        d2 = data
    elif a == 'notcallback':
        c = 0
    elif a == 'load':
        return c, d2


def delay_seconds(td):
    last = time.time()
    exit = False
    while not exit:
        if (time.time() - last) > td:
            exit = True


def seconds2hours(t):
    for i in range(len(t)):
        try:
            t[i] = t[i] / 3600
        except Exception:
            t[i] = 0


def seconds2minutes(t):
    for i in range(len(t)):
        try:
            t[i] = t[i] / 60
        except Exception:
            t[i] = 0


def parseCurve(curve):
    data = {
        'V': [],               
        'SOC': [],                          
        'I': [],                            
        'T': []                             
    }

    try:
        with open(curve, 'r') as f:
            for line in f:
                line = line.replace('\n', '').split(',')
                data['V'].append(float(line[0]))
                data['SOC'].append(float(line[1]))
                data['I'].append(float(line[2]))
                data['T'].append(float(line[3]))
        
        return data

    except Exception as e:
        print(f"<<<< ERROR AL ABRIR EL FICHERO >>>> {e}")
        
        
def parseExcel(profile):
    try:
        df = pd.read_excel(profile, names=['current', 'time'])
    except Exception as e:
        print(f"<<<< ERROR AL ABRIR EL FICHERO >>>> {e}")
        
    data = df.to_numpy().transpose().tolist()
    return data[0], data[1]


def writeDataCD(data, id):
    V = data['V']
    SOC = data['SOC']
    I = data['I']
    T = data['T']

    if id == 'd':
        file_name = os.path.join(parentDirectory, "output_files", "datos_descarga.csv")
    elif id == 'c':
        file_name = os.path.join(parentDirectory, "output_files", "datos_carga.csv")
    elif id == 'dp':
        file_name = os.path.join(parentDirectory, "output_files", "datos_descarga_perfil.csv")
    elif id == 'cp':
        file_name = os.path.join(parentDirectory, "output_files", "datos_carga_perfil.csv")

    try:
        with open(file_name, 'w') as f:
            for i in range(len(V)):
                line = str(V[i]) + ',' + str(SOC[i]) + ',' + str(I[i]) + ',' + str(T[i]) +'\n'
                f.write(line)
    
    except Exception as e:
        print(f"<<<< ERROR AL ABRIR EL FICHERO >>>> {e}")


def writeDataPV(data):
    I_ps = data['I_ps']
    I_load = data['I_load']
    I_bat = data['I_bat']
    V = data['V']
    SOC = data['SOC']
    T = data['T']

    file_name = os.path.join(parentDirectory, "output_files", "datos_fv.csv")

    try:
        with open(file_name, 'w') as f:
            for i in range(len(V)):
                line = str(I_ps[i]) + ',' + str(I_load[i]) + ',' + str(I_bat[i]) + ',' + str(V[i]) + ',' + str(SOC[i]) + ',' + str(T[i]) +'\n'
                f.write(line)
    
    except Exception as e:
        print(f"<<<< ERROR AL ABRIR EL FICHERO >>>> {e}")


def writeRelax(V, SOC, file_name):

    try:
        with open(file_name, 'w') as f:
             for i in range(len(V)):
                line = str(V[i]) + ',' + str(SOC[i]) +'\n'
                f.write(line)
    
    except Exception as e:
        print(f"<<<< ERROR AL ABRIR EL FICHERO >>>> {e}")


def relaxVoltDischarge(data):
    V = data['V']
    SOC = data['SOC']
    I = data['I']
    V_relax = []
    SOC_relax = []
    N = 10

    V_relax.append(V[0])
    SOC_relax.append(SOC[0])

    for i in range(len(V)-1):
        if (I[i] < 0.1) and (I[i+1] >= 4 and (i != 0)):
            #if V[i] == V[i-1]:
            media = sum(V[i-N+1:i+1]) / N
            V_relax.append(media)
            SOC_relax.append(SOC[i])

    media = sum(V[-N:]) / N
    V_relax.append(media)
    SOC_relax.append(SOC[len(V)-1])

    return V_relax, SOC_relax


def relaxVoltCharge(data):
    V = data['V']
    SOC = data['SOC']
    I = data['I']
    V_relax = []
    SOC_relax = []
    N = 10

    V_relax.append(V[0])
    SOC_relax.append(SOC[0])

    for i in range(len(V)-1):
        if (I[i] < 0.1) and (I[i+1] >= 0.1 and (i != 0)):
            #if V[i] == V[i-1]:
            media = sum(V[i-N+1:i+1]) / N
            V_relax.append(media)
            SOC_relax.append(SOC[i])

    media = sum(V[-N:]) / N
    V_relax.append(media)
    SOC_relax.append(SOC[len(V)-1])

    return V_relax, SOC_relax


def voltageCapacityTransform(V, SOC):
    C = 20
    c = []
    for i in range(len(V)):
        V[i] = V[i] / 17
        c.append((((100 - SOC[i]) / 100) * C) / 8)

    return V, c 


def curve(x, y, title, name, x_axis, y_axis):
    plt.figure(num=1)
    plt.close()
    plt.plot(x, y)
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    plt.title(title)
    #plt.show()
    plt.savefig(name)

def curve2(x1, y1, x2, y2, title, name, x_axis, y_axis, curve1, curve2):
    plt.figure(num=1)
    plt.close()
    plt.plot(x1, y1, 'b-', label=curve1)
    plt.plot(x2, y2, 'r-', label=curve2)
    plt.legend()
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    plt.title(title)
    #plt.show()
    plt.savefig(name)


def curve3(x1, y1, x2, y2, x3, y3, title, name, x_axis, y_axis, curve1, curve2, curve3):
    plt.figure(num=1)
    plt.close()
    plt.plot(x1, y1, 'b-', label=curve1)
    plt.plot(x2, y2, 'r-', label=curve2)
    plt.plot(x3, y3, 'y-', label=curve3)
    plt.legend()
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    plt.title(title)
    #plt.show()
    plt.savefig(name)


def calculateSOC(I_bat, t, soc, C):
    try:
        charge = (I_bat * (t/3600) * 100) / C
        soc = soc + charge
    
    except Exception as e:
        print(f"<<<< ERROR CALCULO>>>> {e}")
        soc = 0

    return soc