# -*- coding: utf-8 -*-
"""
Tarea #5. IE0405 - Modelos Probabilísticos de Señales y Sistemas.
Empezada el Sábado 11 de Julio 09:14 2020

@author: Mauricio Céspedes Tenorio.
Carné: B71986
"""
#Librerías
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

print("Respuestas del inciso 4 de la Tarea #5 del curso IE0405 - Modelos Probabilísticos de Señales y Sistemas.")
print("Estudiante: Mauricio Céspedes Tenorio. Carné: B71986.")

# Número de clientes
N = 1000

# Parámetro de llegada (clientes/segundos)
lam = 2/60

# Parámetro de servicio (servicios/segundos)
nu = 2/60

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

#Vector que define el tiempo de salida del cliente en cada uno de ambos servidores:
fin = np.zeros(2)

# Inicialización del tiempo de inicio y fin de atención
inicio = t_lleg[0]          # primera llegada
fin[0] = inicio + t_serv[0]    # primera salida

#Inicialización del tiempo de atención: caso del primer cliente
t_aten = [inicio]

# Tiempos en que recibe atención cada i-ésimo cliente (!= que llega)
for i in range(1, N):
    if fin[0]>=fin[1]:
        inicio = int(np.max((t_lleg[i], fin[1])))
        fin[1] = inicio + t_serv[i]
    else:
        inicio = int(np.max((t_lleg[i], fin[0])))
        fin[0] = inicio + t_serv[i]
    t_aten.append(inicio)

#Se debe encontrar el tiempo en el que el último cliente sale, pero esto no significa que sea necesariamente el último en ser atendido al ser 2 servidores.
#Se crea la variable del tiempo de salida del último cliente:
t_salida_final = 0

#Se recorre la lista de t_aten para encontrar el tiempo de salida más grande:
for i, tiempo in enumerate(t_aten):
    t_salida_nuevo = tiempo + t_serv[i]
    if t_salida_final<t_salida_nuevo:
        t_salida_final = t_salida_nuevo

# Inicialización del vector temporal para registrar eventos
t = np.zeros(t_salida_final + 1)

# Asignación de eventos de llegada (+1) y salida (-1) de clientes
for c in range(N):
    i = t_lleg[c]
    t[i] += 1
    j = t_aten[c] + t_serv[c]
    t[j] -= 1

# Umbral de P o más personas en sistema (hay P - 2 en fila)
P = 8

# Instantes (segundos) de tiempo con P o más solicitudes en sistema
frecuencia = 0

# Proceso aleatorio (estados n = {0, 1, 2...})
Xt = np.zeros(t.shape)

# Inicialización de estado n
n = 0

# Recorrido del vector temporal y conteo de clientes (estado n)
for i, c in enumerate(t):
    n += c # sumar (+1) o restar (-1) al estado
    Xt[i] = n
    if Xt[i] >= P:
        frecuencia += 1

# Fracción de tiempo con P o más solicitudes en sistema
fraccion = frecuencia / len(t)
print(frecuencia, len(t))
# Resultados
print('Parámetro lambda = ', str(lam*60))
print('Parámetro nu = ', str(nu*60))
print('Tiempo con más de {} solicitudes en fila:'.format(P-3))
print('\t {:0.2f}%'.format(100*fraccion))
if fraccion <= 0.05:
    print('\t Sí cumple con la especificación.')
else:
    print('\t No cumple con la especificación.')
print('Simulación es equivalente a {:0.2f} horas.'.format(len(t)/3600))

# Gráfica de X(t) (estados del sistema)
plt.figure()
plt.plot(Xt)
plt.plot(range(len(t)), (P-1)*np.ones(t.shape))
plt.legend(('$X(t) = n$', '$L_q = $' + str(P-3)))
plt.ylabel('Clientes en el sistema, $n$')
plt.xlabel('Tiempo, $t$ / segundos')
plt.show()
