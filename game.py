try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk

import numpy as np
from random import seed
from random import randint


taille_case=20

statue = True   #sert a arreter le jeu en appuyant sur Pause

# Dans l'affichage : - case blanche  => noeud mort
#                    - case noire  => noeud vivant

#Classe contenant le traitement du jeu de la mort

class JeuDeLaVie:
    def __init__(self,taille):
        self.taille = taille
        self.nb_cases = int(taille/taille_case)
        self.A =  np.zeros((self.nb_cases,self.nb_cases),dtype=bool)
        self.Time = 100

    #initialisation aleatoire du jeu
    def initialiser(self):
        for i in range(0,self.nb_cases):
            for j in range(0,self.nb_cases):
                self.A[i][j] = randint(1,10)%2

    #initialisation de la matrice avec configuration grenouille
    def initialise_grenouille(self):
        self.A[6][6] =1
        self.A[6][7] =1
        self.A[6][8] =1
        
        self.A[7][5] =1
        self.A[7][6] =1
        self.A[7][7] =1

    #Algorithme du jeu
    def nombre_voisin_vivant(self,i,j):
        #calcul du nombre de voisin vivant du noeud (i,j)
        if i<0 or i>=self.nb_cases or  j<0 or j>=self.nb_cases :
            return 0
        l = (j>0)
        r = (j+1<self.nb_cases)
        u = (0<i)
        d = (i+1<self.nb_cases)
        s=0
        if l:
            s += self.A[i][j-1]
        if r:
            s+= self.A[i][j+1]
        if u:
            s+= self.A[i-1][j]
        if d:
            s+= self.A[i+1][j]
        if u and l:
            s+= self.A[i-1][j-1]
        if u and r :
            s+= self.A[i-1][j+1]
        if d and l:
            s+= self.A[i+1][j-1]
        if d and r:
            s+= self.A[i+1][j+1]
        return s

    def faire_un_cycle(self):
        #Collecte des neuds (i,j) qui doivent changer leurs couleurs dans le prochain tour
        List = []
        for i in range(0,self.nb_cases):
            for j in range(0,self.nb_cases):
                V =  self.nombre_voisin_vivant(i,j)
                if  (V == 3) or ( self.A[i][j] == 1 and V==2):#enquee
                    after=True
                else:
                    after=False
                if after != self.A[i][j]:
                    List.append([i,j,after])
        return List

    #Grille
    def MAJ_Grille(self,c):
        #Mise a jour de la grille 
        L = self.faire_un_cycle()
        if len(L) == 0:
            return
        while len(L) > 0:
            n=L.pop()
            self.A[n[0]][n[1]] = n[2]
            if n[2]==0:
                moS="white"
            else:
                moS="black"
            if n[0] < self.nb_cases and n[1] < self.nb_cases:
                c.create_rectangle(n[1]*taille_case,n[0]*taille_case,(n[1]+1)*taille_case,(n[0]+1)*taille_case, fill=moS)
        
    #initialisation de la grille avec les noeuds contenus dans la matrice A
    def Creer_Grille(self,c):
        for i in range(0, self.taille+1, taille_case):
            c.create_line([(i, 0), (i, self.taille)], tag='grid_line')
            c.create_line([(0, i), (self.taille, i)], tag='grid_line')
        for i in range(0,self.nb_cases):
            for j in range(0,self.nb_cases):
                if self.A[i][j]==1:
                    c.create_rectangle(j*taille_case,i*taille_case,(j+1)*taille_case,(i+1)*taille_case, fill="black")
    #note: create_rectangle(x1, y1, x2, y2) => (x1 = j , y1 = i) * taille_case  et (x2 = j+1 , y2 = i+1) * taille_case

    #Time
    def get_Time(self):
        return self.Time

    def set_Time(self,t):
        self.Time = t

# Initialiser le jeu avec une taille = 600 
Game= JeuDeLaVie(600)

# Initialiser le jeu avec une configuration dite grenouille selon wikipedia
Game.initialise_grenouille()


#Fonctions d'affichage

def create_game(event=None):
    Game.Creer_Grille(c)

def game_update(event=None):
    Game.MAJ_Grille(c)
    if statue==True :
            root.after(Game.get_Time(),game_update)     

def Bouton_Pause():
    global statue
    statue = not statue
    if statue:
        Pause.config(text = "Pause")
        game_update()
    else :
        Pause.config(text = "Reprendre")

def new_periode(event=None):
    Game.set_Time(int(Periode.get()))
    return Game.get_Time()

def set_seed(event):
    seed_ = int(choix_seed.get()) #gere l exception
    seed(seed_)
    Game.initialiser() #reinitaliser aleatoirement le jeu
    Game.MAJ_Grille(c)
    return seed_


#Instatiation du Tkinter

root = tk.Tk()

#Creation du widjet canvas

c = tk.Canvas(root, height=Game.taille, width=Game.taille, bg='white')
c.pack(fill=tk.BOTH, expand=True)

c.bind('<Configure>', create_game)

frame = tk.Frame(root)
frame.pack()

#Creation des bouton QUIT & Pause

Pause_text = tk.Button(frame, 
                   text="QUIT", 
                   fg="red",
                   command=quit)

Pause_text.pack(side=tk.LEFT)

Pause = tk.Button(frame,
                   text="Pause",
                   command=Bouton_Pause)

Pause.pack(side=tk.LEFT)

#Entrees pour definir la periode et la graine de la seed

#Periode est le temps en milisecondes entre deux transition du jeu

tk.Label(frame, text="Choisir Periode:").pack(side=tk.LEFT)
Periode = tk.Entry(frame)
Periode.pack(side=tk.LEFT)
Periode.bind("<Return>", new_periode)

# Apres input de la seed on reinitialise Game avec une distribution aleatoire de noeud vivant

tk.Label(frame, text="seed:").pack(side=tk.LEFT)
choix_seed = tk.Entry(frame)
choix_seed.pack(side=tk.LEFT)
choix_seed.bind("<Return>", set_seed)

#appel a game_update engendre un appel recursif de la game_update aisi que les apels a la methode MAJ_Grille du jeu

game_update()

#Lancer la boucle d'affichage
root.mainloop()
