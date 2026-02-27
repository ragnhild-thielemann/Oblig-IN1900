#%%

import numpy as np
import matplotlib.pyplot as plt
from datetime import date, timedelta
from SEIR import plot_SEIR
from outbreak import solve_SEIR #gir oss løsningen fra den forrgje filen
from ODEsolver import Euler
class Beta:
    def __init__(self,filename):
        with open(filename,"r") as fil:
            fil.readline()
            fil.readline()
            n = []
            beta = []
            for linje in fil:
                words = linje.split()
                day, month, year = (int(n) for n in words[0].split("."))
                n.append(date(year,month,day))  
                beta.append(float(words[2])) 
                
            dager = 0
            d_liste = [] ; b_liste = []
            for k in range(len(n)-1):
                delta = n[k+1] - n[k]
                n_days = delta.days
                dager = dager + n_days
                d_liste.append(dager)
                b_liste.append(beta[k])
        self.d_liste = d_liste ; self.b_liste = b_liste
    
    def __call__(self,t):
        d_liste = self.d_liste ; b_liste = self.b_liste
        if np.isscalar(t):
            
            for indeks, tid in enumerate(d_liste):
                if t<tid:
                    return b_liste[indeks]
        else: 
            resultat = []

            for t_ in t:
                for indeks, tid in enumerate(d_liste):
                    if t_<=tid:
                        resultat.append(b_liste[indeks])
                        break
            return np.array(resultat)

    def plot(self,T):
        t = np.linspace(0,self.d_liste[-1],T)
        u = (self(t))
        plt.plot(t,u)
n = Beta("beta.txt")
n.plot(10000)


t,u = solve_SEIR(Euler,900,1000,5.5*10**6,100,n) #gir oss løsningen fra den forrgje filen

#plot_SEIR(t,u,["I","Ia"])




