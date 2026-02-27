#%%

import numpy as np
import matplotlib.pyplot as plt

class ODEsolver: #make an ODEsolver as an class
    def __init__(self,f):
        self.f = f 
    
    def integrer(self,u0,T,N): #integrates 
        self.dt = T/N
        self.u0 = np.asarray(u0)
        u_verdier = np.zeros([N+1,np.size(u0)])
        t_verdier = np.zeros(N+1)
        u_verdier[0] = u0
        for n in range(N):
            u_verdier[n + 1] = u_verdier[n] + self.dt*self.ettstegfrem(t_verdier[n],u_verdier[n])
            t_verdier[n + 1] = t_verdier[n] + self.dt

        return t_verdier,u_verdier
    
class Euler(ODEsolver):
    def ettstegfrem(self,t,u):
        return self.f(t,u)

class RK4(ODEsolver):
    def ettstegfrem(self,t,u):
        f = self.f ; dt = self.dt
        k1 = f(t,u)
        k2 = f(t + 0.5 * dt,u + 0.5*dt*k1)
        k3 = f(t + 0.5 * dt, u + 0.5*dt*k2)
        k4 = f(t + dt, u + dt*k3)
        return (1/6)*(k1 + 2*k2 + 2*k3 + k4)
