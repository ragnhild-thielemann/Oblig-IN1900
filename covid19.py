#%%

import numpy as np
import matplotlib.pyplot as plt
from datetime import date, timedelta
from SEIR import plot_SEIR, SEIR
from outbreak import solve_SEIR #gir oss løsningen fra den forrgje filen
from ODEsolver import Euler
from lockdown import Beta
from SEIR0 import SEIR0
class SEIRimport(SEIR0): #impotrerer SEIR som en subklasse
    def __init__(self,b,r_ia = 0.1 , r_e2 = 1.55, lmda1 = 0.33, lmda2 = 0.5, p_a = 0.4, mu = 0.2,sigma = 10):
      
        self.sigma = sigma
        if isinstance(b,(float,int)):
            self.b_f = lambda t: b
        elif callable(b):
            self.b_f = b
        super().__init__(self.b_f(0),r_ia = r_ia , r_e2 = r_e2 , lmda1 = lmda1, lmda2 = lmda2 , p_a = p_a , mu = mu) #oppdaterer beta-atributten til å bli en kallbar funskjon. alle de andre atributtene er konstante, så de trenger vi ikke å oppdatere

    def __call__(self,t,u):
        self.beta = self.b_f(t)
        derivs = super().__call__(t, u)
        derivs[2] += self.sigma
        return derivs

def solve_SEIR0(model,T,N,S_0, E2_0,beta):
    u0 = [S_0,0,E2_0,0,0,0]
    f = SEIRimport(beta) #gir oss derivertverdiene
    # vi må oppdatere derivertvediene 
    f_ = model(f)
    t,u = f_.integrer(u0,T,N)
    return t,u

n = Beta("beta.txt")

t,u = solve_SEIR0(Euler,900,1000,5.5*10**6,100,n) #gir oss løsningen fra den forrgje filen

plot_SEIR(t,u,["Ia","I"])