import matplotlib.pyplot as plt

def parseCurve(curve):
    V = []
    SOC =[]

    try:
        with open(curve, 'r') as f:
            for line in f:
                line = line.replace('\n', '').split(',')
                V.append(float(line[0]))
                SOC.append(float(line[1]))
        
        return V, SOC

    except Exception as e:
        print(f"<<<< ERROR AL ABRIR EL FICHERO >>>> {e}")


def parseCurve2(curve):
    V = []
    SOC =[]

    try:
        with open(curve, 'r') as f:
            for line in f:
                line = line.replace('\n', '').split(',')
                V.append(float(line[0]))
                SOC.append(float(line[3]))
        
        return V, SOC

    except Exception as e:
        print(f"<<<< ERROR AL ABRIR EL FICHERO >>>> {e}")


def V_SOC_curve(V0, SOC0, V1, SOC1):
    title = 'Curvas de descarga tensión relajada muestreo 30s (azul) y 5s (rojo)'
    name = 'curvas_carga_cargador_fuente.pdf'

    plt.figure(num=1)
    plt.close()
    plt.plot(SOC1, V1, 'r-', SOC0, V0, 'b-')
    plt.xlabel('SOC (%)')
    plt.ylabel('Tensión (V)')
    plt.title(title)
    #plt.show()
    plt.savefig(name)


def seconds2hours(t):
    for i in range(len(t)):
        t[i] = t[i] / 3600
    return t

def run():
    name_file1 = "datos_descarga_tension_relajada_30.csv"
    name_file2 = "datos_descarga_tension_relajada_5.csv"

    V0, SOC0 = parseCurve(name_file1)
    Vr, SOCr =  parseCurve(name_file2)
    
    V_SOC_curve(Vr, SOCr, V0, SOC0)

run()