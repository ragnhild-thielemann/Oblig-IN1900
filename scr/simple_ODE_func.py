#%%

"""
En enkel ODE-solver
"""
import numpy as np
import matplotlib.pyplot as plt

class ODEsolver:
    def __init__(self,f):
        self.f = f
    
    def integrer(self,u0,T,N):
        self.u0 = np.asarray(u0)
        self.dt = T/N
        t_verdier = np.zeros(N+1)
        u_verdier = np.zeros(N+1)
        u_verdier[0] = u0
        for n in range(N):
            u_verdier[n+1] = u_verdier[n] + self.ettstegfrem(u_verdier[n],t_verdier[n])*self.dt
            t_verdier[n+1] = t_verdier[n] + self.dt
        return u_verdier,t_verdier

class ForwardEuler(ODEsolver):
    def ettstegfrem(self,u,t):
        return self.f(u,t)
    
