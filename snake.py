import sys
import time
import os
import Queue
import random
import RPi.GPIO as GPIO
 

CABEZA = 'o'
CUERPO = '+'
VACIO = ' '
MURO  = '#'
FRUTO = '*'
filas = 20

DERECHA = 18
IZQUIERDA = 22
ARRIBA = 17
ABAJO = 23

SELECT = 24

ndireccion = 0
pausa = False

def imprimirMapa():
    m = "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
    for i in range(filas):
        for j in range (filas):
            m = m + " " + mapa[i][j]
        m = m+'\n'
    print(m)
    print (puntos)

    
def cambiarDireccion (pin):
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
	ndireccion = SELECT
            
def genPremio ():
    flag = 1
    while flag:
        x = random.randint(1,filas-2)
        y = random.randint(1,filas-2)
        if mapa[x][y] == VACIO:
            flag = 0

    mapa[x][y] = FRUTO



GPIO.setmode(GPIO.BCM)
for i in [DERECHA, IZQUIERDA, ARRIBA, ABAJO, SELECT]:
    GPIO.setup(i,GPIO.IN, GPIO.PUD_UP)
    GPIO.add_event_detect(i,GPIO.FALLING)
    GPIO.add_event_callback(i,cambiarDireccion)

        
mapa = [[0 for i in range (filas)] for j in range (filas)]

m = ""

jugar = True
q = Queue.Queue()
direccion = DERECHA
ndireccion = DERECHA
record = ""


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
           Pulsa para empezar a jugar")

while ndireccion != SELECT:
    time.sleep(0.5)

ndireccion = DERECHA

while jugar:
    
    for i in range (filas):
            for j in range (filas):
                    if i == 0 or i == filas-1 or j==0 or j == filas-1:
                            mapa[i][j] = MURO
                    else:
                            mapa[i][j] = VACIO


    mapa[6][1]= CUERPO
    mapa[6][2]= CUERPO
    mapa[6][3]= CUERPO
    mapa[6][4]= CABEZA

    genPremio()

    c = [6,4]
    puntos = 0

    while not q.empty():
        q.get()

    q.put([6,1])
    q.put([6,2])
    q.put([6,3])
    q.put([6,4])

    gameover = False
    tt = 0.5

    while not gameover:

        imprimirMapa()
        
        premio = False
        
        if ndireccion == DERECHA:
            if mapa[c[0]][c[1]+1]==MURO or mapa[c[0]][c[1]+1]==CUERPO:
                gameover = True
            else:
                if mapa[c[0]][c[1]+1]==FRUTO:
                    premio = True

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

        direccion = ndireccion
        
        if premio:
            genPremio()
            puntos += 100
            if puntos%500 == 0:
                tt = tt - tt/5
        else:
            t = q.get()
            mapa[t[0]][t[1]] = VACIO
            
        mapa[c[0]][c[1]] = CABEZA

        while pausa == True:
            time.sleep(0.1)
            
        time.sleep(tt)


    fin = True

    ndireccion = 0
    
    n = ['A', 'A', 'A']
    i = 1
    
    
    while fin:
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        print("\n\n\t ________________________/ O  \\___/\n\t<_____________________________/   \\\n")
        print("\          Has conseguido ")
        print(puntos)
        print(" puntos")
        print("\nIntroduce tu nombre:")

        print(n[0], n[1], n[2])

        if ndireccion == ABAJO:
            n[i] += 1
            ndireccion = 0
        elif ndireccion == ARRIBA:
            n[i] -= 1
            ndireccion = 0
        elif ndireccion == DERECHA:
            i += 1
            if i > 2:
                i = 2
        elif ndireccion == IZQUIERDA:
            i -= 1
            if i < 0:
                i = 0
        elif ndireccion == SELECT:
            fin = False
            

        ndireccion = 0
        time.sleep(0.2)


    records += '\n' + n + ' ' + puntos

    print(records)

    fin = True

    print ("Jugar otra vez")

    ndireccion = 0

    while fin:
        if ndireccion == SELECT:
            fin = False
        elif ndireccion > 0:
            fin = False
            jugar = False
        sleep(0.5)

        

        
    


    
