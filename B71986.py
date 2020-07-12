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
nu = 2/60

# Distribución de los tiempos de llegada entre cada cliente
X = stats.expon(scale = 1/lam)

# Distribución de los tiempos de servicio a cada cliente
#Si n<2:
Y1 = stats.expon(scale = 1/nu)
#Si n>=2:
Y2 = stats.expon(scale = 1/(2*nu))


# Intervalos entre llegadas (segundos desde último cliente)
t_inte = np.ceil(X.rvs(N)).astype('int')

# Tiempos de las llegadas (segundos desde el inicio)
t_lleg = [t_inte[0]]
for i in range(1, len(t_inte)):
    siguiente = t_lleg[i-1] + t_inte[i]
    t_lleg.append(siguiente)

# Tiempos de servicio (segundos desde inicio de servicio): inicialmente se considera el caso n<2 al haber menos de 2 clientes
t_serv = np.ceil(Y1.rvs(N)).astype('int')

# Inicialización del tiempo de inicio y fin de atención
inicio = t_lleg[0]  # primera llegada
t_ev = np.concatenate([np.zeros(inicio-1), np.array([1])]) # vector de eventos
fin = inicio + t_serv[0]    # primera salida

#Cantidad de personas que han llegado al servicio: (se inicia con el primero)
contador_lleg = 1
#Cantidad de personas que han salido del servicio:
contador_out = 0

#Se utiliza un bucle while que crea el vector temporal total. Se evalúa la llegada y salía de clientes en orden cronológico hasta que la última persona en ser atendida ya salió del sistema.
while contador_out < N:
    #Se determina si están operando dos servidores o sólo uno:
    if (contador_lleg-contador_out)<1: #Tiene que compararse con 1, ya que el tiempo de servicio de cualquier cliente por encima del primero será 1/(2*mu), luego se comentará con su respectivo diagrama de transición:
        #En caso de haber un sólo servidor, el tiempo de servicio está definido por 1/mu
        t_serv = np.ceil(Y1.rvs(N)).astype('int')
        #Se evalúa si aún están llegando clientes o si ya llegaron todos. Tiene que ser menor que N ya que los índices de las listas están definidos desde 0, no desde 1.
        if contador_lleg<N:
            #Se evalúa cuál es el siguiente evento en la línea temporal: llegada de otro cliente, salida del cliente actual o ambas simultáneamente
            if t_lleg[contador_lleg]<fin:   #Se evalúa si el siguiente cliente llega antes de que el actual se vaya y si pueden llegar más personas
                #Se agregan los 0's (representan segundos que pasaron hasta que sucedió otro evento) entre el último suceso y la llegada del cliente.
                t_ev = np.concatenate([t_ev, np.zeros((t_lleg[contador_lleg]-len(t_ev))-1), np.array([1])]) #Se agrega a la línea temporal la llegada del cliente en el tiempo dado
                #Se indica que ya llegó otro cliente:
                contador_lleg += 1
            elif t_lleg[contador_lleg]>fin: #Se evalúa si el cliente actual se vaya antes de que llegue el siguiente
                #Se agregan los 0's (representan segundos que pasaron hasta que sucedió otro evento) entre el último suceso y la salida del cliente.
                t_ev = np.concatenate([t_ev, np.zeros((fin-len(t_ev))-1), np.array([-1])]) #Se agrega al vector de eventos la salida del cliente actual
                #Se indica que salió otro cliente:
                contador_out += 1
                #Se establece el tiempo de salida del próximo cliente dependiendo de si llegó antes de que el actual saliera o no. A este resultdo se le suma el tiempo de servicio.
                fin = np.max((t_lleg[contador_out], fin)) + t_serv[contador_out]
            elif t_lleg[contador_lleg]==fin: #Si sale y entra una persona al mismo tiempo
                #En este caso, sólo se agregan 0's entre el evento anterior y el actual, ya que hay un +1 y -1 al mismo tiempo, que es un 0.
                t_ev = np.concatenate([t_ev, np.zeros(fin-len(t_ev))])
                #Se indica que salió otra persona
                contador_out += 1
                #Se actualiza el siguiente tiempo de salida, como en la parte anterior.
                fin = np.max((t_lleg[contador_out], fin)) + t_serv[contador_out]
                #Se indica que llegó otro cliente
                contador_lleg += 1
        #En caso de que ya llegaron todos los clientes y aún no queda sólo un cliente en salir:
        elif contador_lleg==N and contador_out<(N-1):
            #Se agregan los 0's (representan segundos que pasaron hasta que sucedió otro evento) entre el último suceso y la salida del cliente.
            t_ev = np.concatenate([t_ev, np.zeros((fin-len(t_ev))-1), np.array([-1])]) #Se agrega al vector de eventos la salida del cliente actual
            #Se indica que salió otro cliente
            contador_out += 1
            #Se actualiza el siguiente tiempo de salida como ya se explicó:
            fin = np.max((t_lleg[contador_out], fin)) + t_serv[contador_out]
        #Este caso sólo aplica para la salida del último cliente:
        else:
            #Se agregan los 0's (representan segundos que pasaron hasta que sucedió otro evento) entre el último suceso y la salida del cliente.
            t_ev = np.concatenate([t_ev, np.zeros((fin-len(t_ev))-1), np.array([-1])]) #Se agrega al vector de eventos la salida del cliente actual
            #Se suma el último cliente a los que ya salieron:
            contador_out += 1

    #Caso con dos servidores:
    else:
        #Se duplica el mu, con lo que se reduce el tiempo de servicio:
        t_serv = np.ceil(Y2.rvs(N)).astype('int')
        #Se evalúa si aún están llegando clientes o si ya llegaron todos. Tiene que ser menor que N ya que los índices de las listas están definidos desde 0, no desde 1.
        if contador_lleg<N:
            #Se evalúa cuál es el siguiente evento en la línea temporal: llegada de otro cliente, salida del cliente actual o ambas simultáneamente
            if t_lleg[contador_lleg]<fin:   #Se evalúa si el siguiente cliente llega antes de que el actual se vaya y si pueden llegar más personas
                #Se agregan los 0's (representan segundos que pasaron hasta que sucedió otro evento) entre el último suceso y la llegada del cliente.
                t_ev = np.concatenate([t_ev, np.zeros((t_lleg[contador_lleg]-len(t_ev))-1), np.array([1])]) #Se agrega a la línea temporal la llegada del cliente en el tiempo dado
                #Se indica que ya llegó otro cliente:
                contador_lleg += 1
            elif t_lleg[contador_lleg]>fin: #Se evalúa si el cliente actual se vaya antes de que llegue el siguiente
                #Se agregan los 0's (representan segundos que pasaron hasta que sucedió otro evento) entre el último suceso y la salida del cliente.
                t_ev = np.concatenate([t_ev, np.zeros((fin-len(t_ev))-1), np.array([-1])]) #Se agrega al vector de eventos la salida del cliente actual
                #Se indica que salió otro cliente:
                contador_out += 1
                #Se establece el tiempo de salida del próximo cliente dependiendo de si llegó antes de que el actual saliera o no. A este resultdo se le suma el tiempo de servicio.
                fin = np.max((t_lleg[contador_out], fin)) + t_serv[contador_out]
            elif t_lleg[contador_lleg]==fin: #Si sale y entra una persona al mismo tiempo
                #En este caso, sólo se agregan 0's entre el evento anterior y el actual, ya que hay un +1 y -1 al mismo tiempo, que es un 0.
                t_ev = np.concatenate([t_ev, np.zeros(fin-len(t_ev))])
                #Se indica que salió otra persona
                contador_out += 1
                #Se actualiza el siguiente tiempo de salida, como en la parte anterior.
                fin = np.max((t_lleg[contador_out], fin)) + t_serv[contador_out]
                #Se indica que llegó otro cliente
                contador_lleg += 1
        #En caso de que ya llegaron todos los clientes y aún no queda sólo un cliente en salir:
        elif contador_lleg==N and contador_out<(N-1):
            #Se agregan los 0's (representan segundos que pasaron hasta que sucedió otro evento) entre el último suceso y la salida del cliente.
            t_ev = np.concatenate([t_ev, np.zeros((fin-len(t_ev))-1), np.array([-1])]) #Se agrega al vector de eventos la salida del cliente actual
            #Se indica que salió otro cliente
            contador_out += 1
            #Se actualiza el siguiente tiempo de salida como ya se explicó:
            fin = np.max((t_lleg[contador_out], fin)) + t_serv[contador_out]
        #Este caso sólo aplica para la salida del último cliente:
        else:
            #Se agregan los 0's (representan segundos que pasaron hasta que sucedió otro evento) entre el último suceso y la salida del cliente.
            t_ev = np.concatenate([t_ev, np.zeros((fin-len(t_ev))-1), np.array([-1])]) #Se agrega al vector de eventos la salida del cliente actual
            #Se suma el último cliente a los que ya salieron:
            contador_out += 1

# Umbral de P o más personas en sistema (hay P - 1 en fila)
P = 6

# Instantes (segundos) de tiempo con P o más solicitudes en sistema
frecuencia = 0

# Proceso aleatorio (estados n = {0, 1, 2...})
Xt = np.zeros(t_ev.shape)

# Inicialización de estado n
n = 0

# Recorrido del vector temporal y conteo de clientes (estado n)
for i, c in enumerate(t_ev):
    n += c # sumar (+1) o restar (-1) al estado
    Xt[i] = n
    if Xt[i] >= P:
        frecuencia += 1

# Fracción de tiempo con P o más solicitudes en sistema
fraccion = frecuencia/len(t_ev)

# Resultados
print('Parámetro lambda = ', str(lam*60))
print('Parámetro nu = ', str(nu*60))
print('Tiempo con más de {} solicitudes en fila:'.format(P-1))
print('\t {:0.2f}%'.format(100*fraccion))
if fraccion <= 0.05:
    print('\t Sí cumple con la especificación.')
else:
    print('\t No cumple con la especificación.')
print('Simulación es equivalente a {:0.2f} horas.'.format(len(t_ev)/3600))

# Gráfica de X(t) (estados del sistema)
plt.figure()
plt.plot(Xt)
plt.plot(range(len(t_ev)), (P-1)*np.ones(t_ev.shape))
plt.ylabel('Clientes en el sistema, $n$')
plt.xlabel('Tiempo, $t$ / segundos')
plt.show()
