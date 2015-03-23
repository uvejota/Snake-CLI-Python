import sys
import time
import os
import Queue
import random
import RPi.GPIO as GPIO


#Funcion que muestra en pantalla el juego 
def imprimirMapa():

    #Se imprimen muchas lineas en blanco para eliminar el mapa anterior
    m = "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
    #Primero se pasa el array a un string, para mejorar el rendimiento
    for i in range(filas):
        for j in range (filas):
            m = m + " " + mapa[i][j]
        m = m+'\n'
    #Se imprime el mapa y los puntos conseguidos
    print(m)
    print (puntos)

#Funcion que se activa cuando se pulse un pin
#Si se pulsa uno de los botones de direccion se coloca en "nueva direccion"
#Y si se pulsa el boton de accion tambien cambia el estado de la variable pausa
def gestorPin (pin):
    
    global ndireccion
    global pausa
    
    if pin == DERECHA and direccion != IZQUIERDA:
        ndireccion = DERECHA
    elif pin == IZQUIERDA and direccion != DERECHA:
        ndireccion = IZQUIERDA
    elif pin == ARRIBA and direccion != ABAJO:
        ndireccion = ARRIBA
    elif pin == ABAJO and direccion != ARRIBA:
        ndireccion = ABAJO
    elif pin == SELECT:
        if pausa == True:
            pausa = False
        elif pausa == False:
            pausa = True 

#Funcion que dibuja en el tablero un fruto, aleatoriamente
def genPremio ():
    flag = 1
    while flag:
        x = random.randint(1,filas-2)
        y = random.randint(1,filas-2)
        if mapa[x][y] == VACIO:
            flag = 0

    mapa[x][y] = FRUTO
    

#Constantes con el valor de los pines
ARRIBA = 17
DERECHA = 18
IZQUIERDA = 22
ABAJO = 23

SELECT = 24

#Constantes con informacion del juego
CABEZA = 'o'
CUERPO = '+'
VACIO = ' '
MURO  = '#'
FRUTO = '*'
filas = 20

#Variables necesarias, se inicializan
pausa = False
jugar = True
premio = False
direccion = DERECHA
ndireccion = DERECHA
record = ""             #Aqui se guardaran los puntos conseguidos en esta sesion
puntos = 0
gameover = False
tt = 0.5

mapa = [[0 for i in range (filas)] for j in range (filas)] #Array con el mapa
m = ""                  #Para mejorar el rendimiento se imprimira una cadena

q = Queue.Queue()       #Cola donde se guardaran los elementos de la serpiente

#Se activan los pines como entrada y se les asigna un callback
GPIO.setmode(GPIO.BCM)
for i in [DERECHA, IZQUIERDA, ARRIBA, ABAJO, SELECT]:
    GPIO.setup(i,GPIO.IN, GPIO.PUD_UP)
    GPIO.add_event_detect(i,GPIO.FALLING)
    GPIO.add_event_callback(i,gestorPin)


        
print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\
                    /^\\/^\\\\\n\
                  _|__|  O|\\\n\
         \\/     /~     \\_/ \\\\\n\
          \\____|__________/  \\\n\
                 \\_______      \\\n\
                         `\\     \\                 \\\n\
                           |     |                  \\\n\
                          /      /                    \\\n\
                         /     /                       \\\\\n\
                       /      /                         \\ \\\n\
                      /     /                            \\  \\\n\
                    /     /             _----_            \\   \\\n\
                   /     /           _-~      ~-_         |   |\n\
                  (      (        _-~    _--_    ~-_     _/   |\n\
                   \\      ~-____-~    _-~    ~-_    ~-_-~    /\n\
                     ~-_           _-~          ~-_       _-~\n\
                        ~--______-~                ~-___-~\n")


print("\
            Alimenta a la serpiente dirigiendola hacia los frutos repartidos por el tablero.\n\
            Usa las teclas para elegir la direccion que seguira la piton.\n\
            Cada fruto da cien puntos. Cada quinientos aumentara su velocidad.\n\
            Pulsa para empezar a jugar")

while pausa == False:
    time.sleep(0.5)
      

      
#Se inicia una nueva partida
while jugar:

    #Se inicializa el mapa
    for i in range (filas):
            for j in range (filas):
                    if i == 0 or i == filas-1 or j==0 or j == filas-1:
                            mapa[i][j] = MURO
                    else:
                            mapa[i][j] = VACIO

    #Se dibuja en el la serpiente y el fruto
    mapa[6][1]= CUERPO
    mapa[6][2]= CUERPO
    mapa[6][3]= CUERPO
    mapa[6][4]= CABEZA

    genPremio()

    #Variable que guarda donde se encuentra la cabeza
    c = [6,4]
    puntos = 0

    #Se vacia la cola de partidas anteriores
    while not q.empty():
        q.get()

    #Se anade la serpiente a la cola
    q.put([6,1])
    q.put([6,2])
    q.put([6,3])
    q.put([6,4])

    gameover = False
    tt = 0.5
    ndireccion = DERECHA
    pausa = False

    #Se inicia la partida!
    while not gameover:

        #Cuando se encuentre un fruto en esta partida sera True
        premio = False

        #Si se mueve hacia la derecha
        if ndireccion == DERECHA:
            #Si hay un muro o su cola delante - Game over
            if mapa[c[0]][c[1]+1]==MURO or mapa[c[0]][c[1]+1]==CUERPO:
                gameover = True
            #Si no lo hay
            else:
                #Si hay un fruto se marca premio como true
                if mapa[c[0]][c[1]+1]==FRUTO:
                    premio = True
                
                #Donde estaba la cabeza se dibuja un cuerpo y la cabeza
                #Se vuelve a dibujar uno mas a la derecha
                mapa[c[0]][c[1]]=CUERPO
                c[1] += 1
                mapa[c[0]][c[1]]=CABEZA
                q.put([c[0],c[1]])


        elif ndireccion == IZQUIERDA:
            if mapa[c[0]][c[1]-1]==MURO or mapa[c[0]][c[1]-1]==CUERPO:
                gameover = True
            else:
                if mapa[c[0]][c[1]-1]==FRUTO:
                    premio = True
                
                mapa[c[0]][c[1]]=CUERPO
                c[1] -= 1
                mapa[c[0]][c[1]]=CABEZA
                q.put([c[0],c[1]])
                
        elif ndireccion == ABAJO:
            
            if mapa[c[0]+1][c[1]]==MURO or mapa[c[0]+1][c[1]]==CUERPO:
                gameover = True
            else:
                if mapa[c[0]+1][c[1]]==FRUTO:
                    premio = True
                
                mapa[c[0]][c[1]]=CUERPO
                c[0] += 1
                mapa[c[0]][c[1]]=CABEZA
                q.put([c[0],c[1]])

        elif ndireccion == ARRIBA:
            
            if mapa[c[0]-1][c[1]]==MURO or mapa[c[0]-1][c[1]]==CUERPO:
                gameover = True
            else:
                if mapa[c[0]-1][c[1]]==FRUTO:
                    premio = True
                
                mapa[c[0]][c[1]]=CUERPO
                c[0] -= 1
                mapa[c[0]][c[1]]=CABEZA
                q.put([c[0],c[1]])

        #Se cambia la direccion. Esto es para evitar conflictos al tocar
        #dos botones rapidamente.
        direccion = ndireccion

        #Si se ha comido un fruto en esta ejecucion se dibuja otro y aumenta
        #los puntos y la velocidad si es necesario.
        if premio:
            genPremio()
            puntos += 100
            if puntos%500 == 0:
                tt = tt - tt/5
        
        #Si no se ha comido ningun fruto, se elimina el ultimo segmento de la cola,
        #porque la serpiente se mueve y no ha crecido
        else:
            t = q.get()
            mapa[t[0]][t[1]] = VACIO

        #Si se pulsa pausa, se queda pillado en este bucle hasta que se vuelva a pulsar.    
        while pausa == True:
            time.sleep(0.1)
        if not gameover:
            imprimirMapa()
            time.sleep(tt)


    #Ahora que la partida ha terminado se pide el nombre
    pausa = True
    ndireccion = 0

    
    while pausa:
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        print("\n\n\t ________________________/ O  \\___/\n\t<_____________________________/   \\\n")
        s = "\t Has conseguido " + `puntos` + " puntos"
        print(s)
      
        print ("Jugar otra vez?\n Pulsa el boton para jugar, una direccion para salir.")
    
      
        if ndireccion > 0:
            pausa = False
            jugar = False
      
      
        #Se para un instante para aligerar la carga del procesador
        time.sleep(0.2)
    

        

        
    


    
