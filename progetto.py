import pygame, random, sys, json
import tkinter as tk
from pygame.locals import *

pygame.init()


#Carico le immagini da usare
sfondo = pygame.image.load('Immagini/sfondo.png')
hai_vinto = pygame.image.load('Immagini/Hai vinto.png')
hai_perso = pygame.image.load('Immagini/Game over.png')
cella_stato = pygame.image.load('Immagini/cella_stato.png')
bandierina = pygame.image.load('Immagini/bandierina.png')
bomba =  pygame.image.load('Immagini/bomba.png')
cella_vuota = pygame.image.load('Immagini/cella.png')
una_mina_adiacente = pygame.image.load('Immagini/1.png')
due_mine_adiacenti = pygame.image.load('Immagini/2.png')
tre_mine_adiacenti = pygame.image.load('Immagini/3.png')
quattro_mine_adiacenti = pygame.image.load('Immagini/4.png')
cinque_mine_adiacenti = pygame.image.load('Immagini/5.png')
sei_mine_adiacenti = pygame.image.load('Immagini/6.png')
sette_mine_adiacenti = pygame.image.load('Immagini/7.png')
otto_mine_adiacenti = pygame.image.load('Immagini/8.png')




#Creo la finestra grafica
width = 850
height = 700
schermo = pygame.display.set_mode((width,height))



#Imposto il nome alla scheda
pygame.display.set_caption('Campo minato') 



#Stabilizzo il font da usare (None = font di default)
font = pygame.font.Font(None, 50)



#Colori 
ROSSO = (225, 0, 0)
GRIGIO = (130, 130, 130)
VERDE = (0, 110, 0)
BLU = (0, 0, 185)



#Assegno un'icona alla scheda
pygame.display.set_icon(bomba) 



#Variabili che utilizzo
punteggio = 0                    #punteggio ad inizio gioco
punteggio_totale = 0
num_mine = 6                    #mine ad inizio gioco



#Funzione che posiziona casualmente le mine all'interno del campo
def posiziona_mine(x):
    while x > 0:
        i  = random.randint(0,righe-1)
        j = random. randint(0,colonne-1)
        if celle[i][j] != -1:
            celle[i][j] = -1
        x -= 1



#Funzione che va a trovare le coordinate dell'intorno di una cella di coordinate (z,q)
def vicine(m,z,q):
    v = []
    if q == len(m[0])-1:
        if z == 0:
            v.append((z,q-1))
            v.append((z+1,q-1))
            v.append((z+1,q))
        elif z == len(m)-1:
            v.append((z-1,q-1))
            v.append((z-1,q))
            v.append((z,q-1))
        else:
            v.append((z-1,q-1))
            v.append((z-1,q))
            v.append((z,q-1))
            v.append((z+1,q-1))
            v.append((z+1,q))

    elif q == 0:
        if z == 0:
            v.append((z,q+1))
            v.append((z+1,q))
            v.append((z+1,q+1))
        elif z == len(m)-1:
            v.append((z-1,q))
            v.append((z-1,q+1))
            v.append((z,q+1))
        else:
            v.append((z-1,q))
            v.append((z-1,q+1))
            v.append((z,q+1))
            v.append((z+1,q))
            v.append((z+1,q+1))

    elif z == 0:
        v.append((z,q-1))
        v.append((z,q+1))
        v.append((z+1,q-1))
        v.append((z+1,q))
        v.append((z+1,q+1))

    elif z == len(m)-1:
        v.append((z-1,q-1))
        v.append((z-1,q))
        v.append((z-1,q+1))
        v.append((z,q-1))
        v.append((z,q+1))

    else:
        v.append((z-1,q-1))
        v.append((z-1,q))
        v.append((z-1,q+1))
        v.append((z,q-1))
        v.append((z,q+1))
        v.append((z+1,q-1))
        v.append((z+1,q))
        v.append((z+1,q+1))        

    return v



#Inizializzo il campo di gioco creando una matrice che contiene il numero di mine, i vari numeri con intorno le mine e le celle
#vuote senza mine intorno
def inizializza_campo():
    global celle, stato, righe, colonne
    righe = 12
    colonne = 12
    celle = [[0]*colonne for i in range (righe)]
    stato = [[0]*colonne for i in range (righe)]
    posiziona_mine(num_mine)
    for i in range(righe):
        for j in range(colonne):
            if celle[i][j] != -1:
                celleVicine = vicine(celle,i,j)
                num = 0
                for (x,y) in celleVicine:
                    if celle[x][y] == -1:
                        num += 1
                        celle [i][j] = num
    return celle 



#Funzione che va a scoprire la cella di coordinata (r,c)
def scopri(r,c):
    if celle[r][c] == -1:                       #abbiamo trovato una bomba e abbiamo perso
        return False

    if celle[r][c] > 0:
        stato[r][c] = 1                         #la cella sarà visualizzata
        return True

    pila = [(r,c)]
    while len(pila) > 0:                    #se trovo una cella con 0 mine intorno, vado a scoprire tutte le celle che sono intorno a quest'ultima
        (i,j) = pila.pop()                     #fino a trovare celle con mine intorno
        if stato[i][j] == 0:                    
            stato[i][j] = 1
            celleVicine = vicine(celle, i, j)
            for (x,y) in celleVicine:
                if celle[x][y] > 0:
                    stato[x][y] = 1
                else:
                    pila.append((x,y))



#Funzione che va a contare tutte le celle che sono scoperte
def celle_scoperte():
    global numScoperte
    numScoperte = 0
    for i in range(len(stato)):
        for j in range(len(stato[0])):
            if stato[i][j] == 0:
                numScoperte += 0
            elif stato[i][j] == 2:
                numScoperte += 0
            else:
                numScoperte += 1
    return numScoperte



#Funzione che verifica se abbiamo vinto o no
def vittoria():
    return celle_scoperte() == (righe*colonne) - num_mine



#Aggiornamento dello schermo con un frame per second di 60
def aggiorna():
    FPS = 60
    pygame.display.update()
    pygame.time.Clock().tick(FPS)



#Funzione che stampa il campo grafico
def stampa_celle():
    global w,h
    w = 180
    h = 150
    for i in range(len(celle)):
        for j in range(len(celle[0])):
            if celle[i][j] == 0:
                schermo.blit(cella_vuota, (w,h))
            elif celle[i][j] == 1:
                schermo.blit(una_mina_adiacente, (w,h))
            elif celle[i][j] == 2:
                schermo.blit(due_mine_adiacenti, (w,h))
            elif celle[i][j] == 3:
                schermo.blit(tre_mine_adiacenti, (w,h))
            elif celle[i][j] == 4:
                schermo.blit(quattro_mine_adiacenti, (w,h))
            elif celle[i][j] == 5:
                schermo.blit(cinque_mine_adiacenti, (w,h))
            elif celle[i][j] == 6:
                schermo.blit(sei_mine_adiacenti, (w ,h))
            elif celle[i][j] == 7:
                schermo.blit(sette_mine_adiacenti, (w,h))
            elif celle[i][j] == 8:
                schermo.blit(otto_mine_adiacenti, (w ,h))
            else:
                schermo.blit(bomba, (w ,h))
            w += 40
        w = 180
        h += 40

        

#Funzione che stampa lo stato attuale del campo di gioco
def stampa_campo_attuale():
    global w, h
    w = 180
    h = 150
    for i in range(len(stato)):
        for j in range(len(stato[0])):
            if stato[i][j] == 0:
                schermo.blit(cella_stato, (w,h))
            elif stato[i][j] == 2:
                schermo.blit(bandierina, (w,h))
            else:
                if celle[i][j] == 0:
                    schermo.blit(cella_vuota, (w,h))
                elif celle[i][j] == 1:
                    schermo.blit(una_mina_adiacente, (w,h))
                elif celle[i][j] == 2:
                    schermo.blit(due_mine_adiacenti, (w,h))
                elif celle[i][j] == 3:
                    schermo.blit(tre_mine_adiacenti, (w,h))
                elif celle[i][j] == 4:
                    schermo.blit(quattro_mine_adiacenti, (w,h))
                elif celle[i][j] == 5:
                    schermo.blit(cinque_mine_adiacenti, (w,h))
                elif celle[i][j] == 6:
                    schermo.blit(sei_mine_adiacenti, (w,h))
                elif celle[i][j] == 7:
                    schermo.blit(sette_mine_adiacenti, (w,h))
                elif celle[i][j] == 8:
                    schermo.blit(otto_mine_adiacenti, (w,h))
                else:
                    schermo.blit(bomba, (w,h))
            w += 40
        w = 180
        h += 40


        

def inizia_gioco():
    schermo.blit(sfondo, (0,0))         #Imposto lo sfondo alla finestra grafica
    aggiorna()                                  #Aggiorno lo schermo




def coordinata_x():
    global h
    h = 150
    (mousex ,mousey) = pygame.mouse.get_pos()
    x = (mousey - h) // 40
    return x




def coordinata_y():
    global w
    w = 180
    (mousex ,mousey) = pygame.mouse.get_pos()
    y = (mousex - w) // 40
    return y




def metti_bandierina():
    if stato[coordinata_x()][coordinata_y()] == 0:
        stato[coordinata_x()][coordinata_y()] = 2
        
    else:
        stato[coordinata_x()][coordinata_y()] = 0
    



def stampa_campo_completo():
    for i in range(len(stato)):
        for j in range(len(stato[0])):
            stato[i][j] = 1




def stampa_scritte():

    pygame.draw.rect(schermo, GRIGIO,  (670, 150, 155, 43))
    mine = font.render('Mine: ' + str(num_mine), False, ROSSO)
    schermo.blit(mine, (680,153))
    
    pygame.draw.rect(schermo, GRIGIO,  (23, 635, 270, 43))
    punteggio_attuale = font.render('Punteggio: ' +str(punteggio), False, VERDE)
    schermo.blit(punteggio_attuale, (35,640))

    pygame.draw.rect(schermo, GRIGIO,  (557, 635, 270, 43))
    punteggio_vittoria = font.render('Totale: ' +str(punteggio_totale), False, BLU)
    schermo.blit(punteggio_vittoria, (580, 640))




def abbandona():
    window.destroy()




def salva_punteggio():
    nome = text_input.get()                         #ottengo il testo che ricevo in input in text_input
    punteggio = punteggio_totale

    giocatori = {}

    giocatori['Giocatore'] = nome
    giocatori['Punti'] = punteggio
    
    s = json.dumps(giocatori, indent=4)

    with open('punteggio.txt', 'a') as f:
        f.write(s)
        f.write(',')
        f.write('\n')
    




def inserisci_nome():
    global text_input
    inserisci_nome = tk.Label(window, text='Inserisci il tuo nome.',  font=('Helvetica', 8))
    inserisci_nome.grid(row=4, column=0, sticky='W', padx=20)
    
    text_input = tk.Entry()                                                                                 #stesso valore del classico input
    text_input.grid(row=5, column=0, sticky='WE', padx = 10)

    bottone_salva = tk.Button(text='Salva!', command=salva_punteggio)
    bottone_salva.grid(row=6, column=0, sticky='W', padx=10, pady=3)
    


def salvare_partita():
    global window
    window = tk.Tk()                        #creo la finestra grafica
    window.geometry('350x180')     #dimensioni della finestra
    window.title('Salvataggio')         #assegno un nome alla finestra
    window.resizable(False, False)   #non mi fa modificare la finestra, rimane nelle misure standard

    window.grid_columnconfigure(0, weight=1)        #wheight --> lo spazio che occupa ogni widget nella colonna
    welcome_label = tk.Label(window, text='Vuoi salvare il punteggio?',  font=('Helvetica', 12))        #scrivo una frase 
    welcome_label.grid(row=0, column=0, sticky='N', padx=20, pady=10)

    bottone1 = tk.Button(text='SI', command=inserisci_nome)
    bottone1.grid(row=1, column=0, sticky='W', padx=20, pady=20)        #sticky --> l'orientamento del widget nella finestra

    bottone2 = tk.Button(text='NO', command=abbandona)
    bottone2.grid(row=1, column=0, sticky='E', padx=20, pady=20)


    window.mainloop()                   #permette l'esecuzione alla finestra grafica tkinter


    
def esci_dal_gioco():
    pygame.quit()
    sys.exit()




#imposto il programma principale
inizia_gioco()
inizializza_campo()

is_running = True

while is_running:
    stampa_campo_attuale()
    stampa_scritte()
    for event in pygame.event.get():
        if event.type == QUIT:
            salvare_partita()
            is_running = False
            esci_dal_gioco()


        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                salvare_partita()
                is_running = False
                esci_dal_gioco()

            if event.key == K_r:
                inizia_gioco()
                inizializza_campo()
                punteggio = 0


        pulsanti_mouse = pygame.mouse.get_pressed()
        if pulsanti_mouse[0] == 1:
            scopri(coordinata_x(), coordinata_y())

            if scopri(coordinata_x(), coordinata_y()) == False:
                punteggio = 0
                punteggio_totale = 0
                num_mine = 6
                schermo.blit(hai_perso, (0,0))
                stampa_campo_completo()
                aggiorna()
                    
            else:
                punteggio = celle_scoperte()
                    
                if vittoria():
                    punteggio = (celle_scoperte() + 100) + (num_mine *10)
                    punteggio_totale += punteggio
                    num_mine += 1
                    schermo.blit(hai_vinto, (0,0))
                    stampa_campo_completo()
                    aggiorna()
                

        if pulsanti_mouse[2] == 1:
            metti_bandierina()

      
    pygame.display.flip()


    




    
