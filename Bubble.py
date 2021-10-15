from tkinter import*
HAUTEUR = 500
LARGEUR = 800
fenêtre = Tk()
fenêtre.title('Bubble')
c = Canvas(fenêtre, height = HAUTEUR, width = LARGEUR, bg = 'darkblue')
c.pack()

id_sousmarin = c.create_polygon(5, 5, 5, 25, 30, 15, fill='red')
id_sousmarin2 = c.create_oval(0, 0, 30, 30, outline='red')
R_SOUSMARIN = 15
X_MIL = LARGEUR/2
Y_MIL = HAUTEUR/2
c.move(id_sousmarin, X_MIL, Y_MIL)
c.move(id_sousmarin2, X_MIL, Y_MIL)

VIT_SOUSMARIN = 10
def déplacer_sousmarin(évènement):
    if évènement.keysym == 'Up':
        c.move(id_sousmarin, 0, -VIT_SOUSMARIN)
        c.move(id_sousmarin2, 0, -VIT_SOUSMARIN)
    elif évènement.keysym == 'Down':
        c.move(id_sousmarin, 0, VIT_SOUSMARIN)
        c.move(id_sousmarin2, 0, VIT_SOUSMARIN)
    elif évènement.keysym == 'Left':
        c.move(id_sousmarin, -VIT_SOUSMARIN, 0)
        c.move(id_sousmarin2, -VIT_SOUSMARIN, 0)
    elif évènement.keysym == 'Right':
        c.move(id_sousmarin, VIT_SOUSMARIN, 0)
        c.move(id_sousmarin2, VIT_SOUSMARIN, 0)
c.bind_all('<Key>', déplacer_sousmarin)

from random import randint
id_bulle = list()
r_bulle = list()
vitesse_bulle = list()
R_BULLE_MIN = 10
R_BULLE_MAX = 30
VITESSE_BULLE_MAX = 10
ECART = 100
def créer_bulle():
    x = LARGEUR + ECART
    y = randint(0, HAUTEUR)
    r = randint(R_BULLE_MIN, R_BULLE_MAX)
    id1 = c.create_oval(x - r, y - r, x + r, y + r, outline ='white')
    id_bulle.append(id1)
    r_bulle.append(r)
    vitesse_bulle.append(randint(1, VITESSE_BULLE_MAX))

def déplacer_bulles():
    for i in range(len(id_bulle)):
        c.move(id_bulle[i], -vitesse_bulle[i], 0)

from time import sleep, time
BULLE_HASARD = 10
LIMITE_TEMPS = 30
SCORE_BONUS = 400

def trouver_coords(num_id):
    pos = c.coords(num_id)
    x = (pos[0] + pos[2])/2
    y = (pos[1] + pos[3])/2
    return x, y
def suppr_bulle(i):
    del r_bulle[i]
    del vitesse_bulle[i]
    c.delete(id_bulle[i])
    del id_bulle[i]
def effacer_bulles():
    for i in range(len(id_bulle)-1, -1, -1):
        x, y = trouver_coords(id_bulle[i])
        if x < -ECART:
            suppr_bulle(i)

from math import sqrt
def distance(id1, id2):
    x1, y1 = trouver_coords(id1)
    x2, y2 = trouver_coords(id2)
    return sqrt((x2 - x1)**2 + (y2 - y1)**2)
def collision():
    points = 0
    for bulle in range(len(id_bulle)-1, -1, -1):
        if distance(id_sousmarin2, id_bulle[bulle]) < (R_SOUSMARIN + r_bulle[bulle]):
            points += (r_bulle[bulle] + vitesse_bulle[bulle])
            suppr_bulle(bulle)
    return points

c.create_text(100, 30, text='TEMPS RESTANT', fill='white')
c.create_text(200, 30, text='SCORE', fill='white')
texte_temps = c.create_text(100, 50, fill='white')
texte_score = c.create_text(200, 50, fill='white')
def afficher_score(score):
    c.itemconfig(texte_score, text=str(score))
def afficher_temps(temps_restant):
    c.itemconfig(texte_temps, text=str(temps_restant))

score = 0
bonus = 0
fin = time() + LIMITE_TEMPS
#BOUCLE PRINCIPALE DU JEU
while time() < fin:
    if randint(1, BULLE_HASARD) == 1:
        créer_bulle()
    déplacer_bulles()
    effacer_bulles()
    score += collision()
    if(int(score/SCORE_BONUS)) > bonus:
        bonus += 1
        fin += LIMITE_TEMPS
    afficher_score(score)
    afficher_temps(int(fin - time()))
    fenêtre.update()
    sleep(0.01)

c.create_text(X_MIL, Y_MIL, \
              text = 'PARTIE TERMINEE', fill='white', font=('Helvetica', 30))
c.create_text(X_MIL, Y_MIL + 30, \
              text = 'Score :' + str(score), fill='white')
c.create_text(X_MIL, Y_MIL + 45, \
              text = 'Temps bonus :' + str(bonus*LIMITE_TEMPS), fill='white')
sleep(10)
