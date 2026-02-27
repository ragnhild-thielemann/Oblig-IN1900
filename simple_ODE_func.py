#%%

import numpy as np
import matplotlib.pyplot as plt

def f(u,t):
    return u/5

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
    
f_ = ForwardEuler(f)
u,t = f_.integrer(0.1,20,5)
plt.plot(t,u)

eksakt = lambda t: 0.1*np.exp(0.2*t)
t_verdier = np.linspace(0,20,10000)
u_verdier = eksakt(t_verdier)
plt.plot(t_verdier,u_verdier)