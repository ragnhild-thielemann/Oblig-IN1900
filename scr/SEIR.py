#%% Imports
from scr.SEIR0 import SEIR0, solve_SEIR0
from scr.ODEsolver import Euler
import matplotlib.pyplot as plt
import numpy as np

# SEIR-klasse med tidsavhengig beta
class SEIR(SEIR0):
    def __init__(self, b, r_ia=0.1, r_e2=1.25, lmda1=0.33, lmda2=0.5, p_a=0.4, mu=0.2):
        """
        Utvider SEIR0-modellen til å håndtere både konstant og tidsavhengig beta.
        """
        if isinstance(b, (float, int)):
            self.b_f = lambda t: b
        elif callable(b):
            self.b_f = b
        else:
            raise ValueError("b må være float, int eller en funksjon av t")
        
        # Initierer SEIR0 med beta til starttidspunkt
        super().__init__(self.b_f(0), r_ia=r_ia, r_e2=r_e2, lmda1=lmda1, lmda2=lmda2, p_a=p_a, mu=mu)
    
    def __call__(self, t, u):
        self.beta = self.b_f(t)  # oppdaterer beta ved gitt tid
        return super().__call__(t, u)

#testfunksjoner
def test_SEIR0_beta_const():
    """
    Tester SEIR med konstant beta mot håndberegnede verdier.
    """
    f = SEIR(0.33)
    u = [1,1,1,1,1,1]
    cal = f(0, u)
    est = [-0.12925, -0.20075, -0.302, 0.3, -0.068, 0.4]
    tol = 1e-8
    assert np.allclose(cal, est, atol=tol), "Feil i beregning med konstant beta"

def test_SEIR0_beta_var():
    """
    Tester SEIR med tidsavhengig beta-funksjon.
    """
    u = [1,1,1,1,1,1]
    
    # To beta-funksjoner
    b_1 = lambda t: -0.05*t + 0.33
    def b_2(t):
        return 0.5 if t < 100 else 0.003

    t_test = [0, 200]
    b_funcs = [b_1, b_2]

    expected = [
        [[-0.12925, -0.20075, -0.302, 0.3, -0.068, 0.4],
         [3.78741, -4.11741, -0.302, 0.3, -0.068, 0.4]],
        [[-0.19583333, -0.13416667, -0.302, 0.3, -0.068, 0.4],
         [-0.001175, -0.328825, -0.302, 0.3, -0.068, 0.4]]
    ]

    tol = 0.1
    for i, beta in enumerate(b_funcs):
        f = SEIR(beta)
        for j, t_ in enumerate(t_test):
            cal = f(t_, u)
            assert np.allclose(cal, expected[i][j], atol=tol), f"Feil i beregning med beta funksjon {i+1} og t={t_}"

# Kjører testene
test_SEIR0_beta_const()
test_SEIR0_beta_var() #testene kjører uten probmeler, som vitner om at funksjonene er korrekte

# Løsning av SEIR0

t, u = solve_SEIR0(Euler, 300, 4000, 5.5e6, 100)  # tid, populasjon, initialverdier

# Funksjon for plotting

def plot_SEIR(t, u, components=["S","I","Ia","R"]):
    """
    Plotter valgte komponenter av SEIR-løsningen.
    Returnerer dictionary med alle komponenter.
    """
    komponenter = ["S","E1","E2","I","Ia","R"]
    løsnings_dic = {k: u[:,i] for i,k in enumerate(komponenter)} #lagrer løsnigenene i en dictionary
    
    plt.figure(figsize=(10,6))
    for c in components:
        if c in løsnings_dic:
            plt.plot(t, løsnings_dic[c], label=c)
    
    plt.xlabel("Tid (dager)")
    plt.ylabel("Antall mennesker")
    plt.title("Sykdomsutvikling i SEIR-modellen")
    plt.grid(True)
    plt.legend()
    plt.show()
    
    return løsnings_dic

løsnings_dic = plot_SEIR(t, u)

# Beregning av respiratorbehov

I = løsnings_dic["I"]
andel_av_infiserte = 0.2      # 20 % av de smittede utvikler alvorlig sykdom
respiratorandel = 0.05        # 5 % av disse trenger respirator
maks_respiratorer = np.max(I) * andel_av_infiserte * respiratorandel

print(f"Det var på det meste {maks_respiratorer:.0f} mennesker som trengte respirator")