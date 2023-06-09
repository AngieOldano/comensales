'''
En comensales.py esta una simulación donde tenemos Comensales, un Cocinero y una determinada 
cantidad de platos disponibles.

La cantidad de platos disponibles se encuentra en una variable global iniciada en 3. 
Esta variable global debe decrementarse cada vez que un comensal "coma" (tome un plato).

El cocinero se mantiene dormido mientras haya platos disponibles.

Si un comensal quiere comer y no hay más platos (0), este deberá:

despertar al Cocinero para que los reponga;
esperar a que este termine (actualice la variable global de nuevo a 3);
comer (decrementando la variable global).
Nota: el cocinero debe volver a dormirse cuando termine de reponer los platos.

El código del archivo NO está completo, deberá agregar la sincronización necesaria para 
que el programa dado funcione como se describe mas arriba.

No importa el orden en que comen los comensales, sí importa que no coman cuando no hay más platos.

La salida debería verse más o menos así:

19:22:57.349 [Comensal 0] - ¡Qué rico! Quedan 2 platos
19:22:57.349 [Comensal 1] - ¡Qué rico! Quedan 1 platos
19:22:57.350 [Comensal 2] - ¡Qué rico! Quedan 0 platos
19:22:57.350 [Cocinero] - Reponiendo los platos...
19:22:57.350 [Comensal 4] - ¡Qué rico! Quedan 2 platos
19:22:57.350 [Comensal 3] - ¡Qué rico! Quedan 1 platos


Ejercicios 4 Comensales y Cocinero
Modificar el ejercicio 2 de modo que la cantidad de 
comensales que pueden pedir platos al mismo tiempo son 2.


'''



import threading
import time
import logging

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)


class Cocinero(threading.Thread):
    def __init__(self):
        super().__init__()
        self.name = 'Cocinero'

    def run(self):
        global platosDisponibles

        while (True):
            semaforoCocinero.acquire()
            try:
                logging.info('Reponiendo los platos...')
                platosDisponibles = 3
            finally:
                semaforoPlato.release()

class Comensal(threading.Thread):
    def __init__(self, numero):
        super().__init__()
        self.name = f'Comensal {numero}'

    def run(self):
        global platosDisponibles

        semaforoComensales.acquire()
        semaforoPlato.acquire()
        
        try:
            while platosDisponibles == 0:
                semaforoCocinero.release()
                semaforoPlato.acquire()
            platosDisponibles -= 1
  
            logging.info(f'¡Qué rico! Quedan {platosDisponibles} platos')

        finally:
            semaforoPlato.release()
            semaforoComensales.release()

semaforoPlato = threading.Semaphore(1)
semaforoCocinero = threading.Semaphore(0)
semaforoComensales = threading.Semaphore(2)


platosDisponibles = 3

Cocinero().start()

for i in range(134):
    Comensal(i).start()
