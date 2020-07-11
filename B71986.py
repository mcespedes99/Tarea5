# -*- coding: utf-8 -*-
"""
Tarea #3. IE0405 - Modelos Probabilísticos de Señales y Sistemas.
Empezada el Miércoles 17 de Junio 17:14 2020

@author: Mauricio Céspedes Tenorio.
Carné: B71986
"""
#Librerías
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

print("Respuestas de la Tarea #3 del curso IE0405 - Modelos Probabilísticos de Señales y Sistemas.")
print("Estudiante: Mauricio Céspedes Tenorio. Carné: B71986.")

# Número de clientes
N = 1000

# Parámetro de llegada (clientes/segundos)
lam = 2/60

# Parámetro de servicio (servicios/segundos)
nu = 3/60

# Distribución de los tiempos de llegada entre cada cliente
X = stats.expon(scale = 1/lam)

# Distribución de los tiempos de servicio a cada cliente
Y = stats.expon(scale = 1/nu)

# Intervalos entre llegadas (segundos desde último cliente)
t_inte = np.ceil(X.rvs(N)).astype('int')

# Tiempos de las llegadas (segundos desde el inicio)
t_lleg = [t_inte[0]]
for i in range(1, len(t_inte)):
    siguiente = t_lleg[i-1] + t_inte[i]
    t_lleg.append(siguiente)

# Tiempos de servicio (segundos desde inicio de servicio)
t_serv = np.ceil(Y.rvs(N)).astype('int')

# Inicialización del tiempo de inicio y fin de atención
inicio = t_lleg[0]          # primera llegada
t_ev = np.concatenate([np.zeros(inicio-1), np.array([1])])        # vector de eventos
fin = inicio + t_serv[0]    # primera salida
t_out = len(np.concatenate([np.zeros(fin-1), np.array([-1])]))    # vector de salidas

contador_lleg = 2
contador_out = 1
while contador_out < N:
    if t_lleg[contador_lleg-1]<t_out and contador_lleg<N:
        t_ev = np.concatenate([t_ev, np.zeros((t_lleg[contador_lleg-1]-len(t_ev))-1), np.array([1])])
        contador_lleg += 1
    elif t_lleg[contador_lleg-1]>t_out:
        t_ev = np.concatenate([t_ev, np.zeros((t_out-len(t_ev))-1), np.array([-1])])
        if t_out>=t_lleg[contador_out]: #Si el cliente n que sale y lo hace después de que el n+1 llegó
            t_out = t_out + t_serv[contador_out]
        else:
            t_out = t_lleg[contador_out] + t_serv[contador_out]
        contador_out += 1
    else:
        t_ev = np.concatenate([t_ev, np.zeros(t_out-len(t_ev))])
        t_out = t_out + t_serv[contador_out]
        contador_out += 1
        contador_lleg += 1
