#%%

import numpy as np
import matplotlib.pyplot as plt
from ODEsolver import Euler
class SEIR0:
    def __init__(self,beta = 0.33,r_ia = 0.1 , r_e2 = 1.25, lmda1 = 0.33, lmda2 = 0.5, p_a = 0.4, mu = 0.2):
        self.beta = beta 
        self.r_ia = r_ia
        self.r_e2 = r_e2
        self.lmda1 = lmda1
        self.lmda2 = lmda2
        self.mu = mu
        self.p_a = p_a

    def __call__(self,t,u):
        beta = self.beta
        r_ia = self.r_ia
        r_e2 = self.r_e2
        lmda1= self.lmda1
        lmda2 = self.lmda2
        p_a = self.p_a
        mu = self.mu
        S,E1,E2,I,Ia,R = u #henter ut parameterne fra u
        N = sum(u) # u inneholder antall i de ulike gruppene. N er antall mennesker, og vil være summen av disse

        dS = (-beta * S * I )/ N - r_ia * beta * S * Ia / N - r_e2 * beta * S * E2 / N #likningene vi fikk oppgitt i kompendiet
        dE1 = beta * S * I / N + r_ia * beta * S * Ia / N + r_e2 * beta * S * E2 / N - lmda1 * E1
        dE2 = lmda1 * (1 - p_a) * E1 - lmda2 * E2
        dI = lmda2 * E2 - mu * I
        dIa = lmda1 * p_a * E1 - mu * Ia
        dR = mu * (I + Ia)
        return np.array([dS, dE1, dE2, dI, dIa, dR])
    

def test_SEIR0():
    f = SEIR0() #lager en instans der vi kaller på funksjonen
    u = [1,1,1,1,1,1]
    cal = f(0,u) #gir en kalkulert verdi for f(0,u) med funksjon. Derivertverdiene er dog ikke avhenige av t, men funksjonen tar inn to parametere
    est = [-0.12925,-0.20075,-0.302,0.3,-0.068,0.4] #beregnete verdier for hånd
    tol = 10**(-9)
    for c_ , e_ in zip(cal,est):
        sucess = abs(e_ - c_) < tol
        assert sucess, "wrong calculation"

test_SEIR0()

def solve_SEIR0(model,T,N,S_0, E2_0,beta = 0.33):
    u0 = [S_0,0,E2_0,0,0,0]
    f = SEIR0(beta) #gir oss derivertverdiene
    # vi må oppdatere derivertvediene 
    f_ = model(f)
    t,u = f_.integrer(u0,T,N)
    return t,u

t,u = solve_SEIR0(Euler,300,4000,5.5*10**6,100)
def plot_SEIR0(t,u):
    navn = ["S","E1","E2","dI","dIa","dR"]
    farge = ["red","yellow","hotpink","skyblue","blue","green"]

    for n,n_ in (enumerate(navn)):
        plt.plot(t,u[:,n],label = n_, color = farge[n])
        plt.legend()




if __name__ == "__main__":
    beta = 0.4
    t,u = solve_SEIR0(Euler,300,4000,5.5*10**(6), 100,beta)
    plot_SEIR0(t,u)

    