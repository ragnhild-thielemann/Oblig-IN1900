#%%

import numpy as np
import matplotlib.pyplot as plt
from datetime import date, timedelta
from scr.SEIR import plot_SEIR
from scr.outbreak import solve_SEIR #gir oss løsningen fra den forrgje filen
from scr.ODEsolver import Euler
class Beta: #lager en klasse for å sortere dataen i beta-verdier
    def __init__(self,filename): #betaverdiene markerer antall personer en smittet person smitter 
        with open(filename,"r") as fil: #åpner filen
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
            d_liste = [] ; b_liste = [] #to lister for å sortere verdiene, en for dager, en for betaverdier
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
        u = (self(t)) #kjører gjennom klassen, til den finner en kallbar funksjon
        plt.plot(t,u,label = "Betavalues",color = "hotpink")
        plt.xlabel("Tid(dager)")
        plt.grid()
        plt.ylabel("Verdi for beta")
        plt.title("Verdier for Beta med reelt datasett")
        plt.legend()

        plt.show()

n = Beta("beta.txt") #lager en instans av klassen, der vi legger inn filen med verdier for beta
n.plot(10000)


t,u = solve_SEIR(Euler,900,1000,5.5*10**6,100,n) #gir oss løsningen fra den forrgje filen

#plot_SEIR(t,u,["I","Ia"])




