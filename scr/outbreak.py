#%%
import numpy as np
import matplotlib.pyplot as plt
from scr.ODEsolver import Euler
from scr.SEIR import SEIR, plot_SEIR

def beta(t): #betafunksjon der beta avtar etter 100 dager, da samfunnet stenger ned 
    if t < 100: #dette er en "piecwice" funksjon, som retunrer ulike verdier for beta ved ulike tider
        return 0.4

    else:
        return 0.083


def solve_SEIR(model,T,N,S_0, E2_0,beta = 0.33):
    u0 = [S_0,0,E2_0,0,0,0]
    f = SEIR(beta) #gir oss derivertverdiene
    # vi må oppdatere derivertvediene 
    f_ = model(f) #gir derivertverdiene i SEIR inn i Eulermodellen
    t,u = f_.integrer(u0,T,N)
    return t,u 
t,u = solve_SEIR(Euler,300,4000,5.5*10**6,100,beta) 

plot_SEIR(t,u)
t,u = solve_SEIR(Euler,300,4000,5.5*10**6,100,beta)
