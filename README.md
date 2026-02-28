## Modelering av pandemi med ODE og Python 
I denne oppgaven skal implementeres en ODE-basert versjon av SEEIIR-modellen, som tilsvarer modellen  Folkehelseinstituttet brukte for å beskrive spredningen av Covid-19-pandemien. Oppgaven implementere  modellen som et system av differensialligninger og simulerer smitteutviklignen over tid av smitteutviklingen over tid.

## Notasjonen i oppgaven

Under analysen av de ulike befolkningsgruppene brukte vi følgende notasjon:

- **S** = Mottakelige (susceptible)
- **E₁** = Eksponert for smitte, men ikke smittsom
- **E₂** = Eksponert for smitte og smittsom
- **I** = Smittet med symptomer
- **Iₐ** = Smittet uten symptomer (asymptomatisk)
- **R** = Frisk / fjernet fra smitteforløpet (recovered)
- **N** = Totalt antall individer i befolkningen
Figuren under viser overgangen fra de ulike gruppene av befolkningen i SEEIIR-modellen.

![Demo](images/notasjon.png)

## Oppgave 1 - SEEIIR-modellen

Vi tok utgangspunkt i modellen beskrevet i kapittel 5 i boken ([Solving
Ordinary Differential Equations in Python](https://link.springer.com/book/10.1007/978-3-031-46768-4)). Denne modellen bruker de seks overnevnte kategoriene, men i første oppgave forenkler vi **E₂** og **E₁** til **E** (altså en samlet kategori for eksponerte), samt  **Iₐ** og **I** til **I** (en samlet kategori for smittede). 

### Systemet av  differensiallikninger
Dette systemet modellerer hvordan en smittsom sykdom sprer seg i en befolkning. Modellen tar hensyn til forskjeller i smittsomhet og inkubasjonstid, og beskriver dynamikken mellom smitte, sykdomsutvikling og immunitet. Dette gir følgene system av differensiallikniger:


$$
\begin{aligned}
S'(t) &= - \beta \frac{S I}{N} - r_{ia} \beta \frac{S I_a}{N} - r_{e2} \beta \frac{S E_2}{N}, \\
E_1'(t) &= \beta \frac{S I}{N} + r_{ia} \beta \frac{S I_a}{N} + r_{e2} \beta \frac{S E_2}{N} - \lambda_1 E_1, \\
E_2'(t) &= \lambda_1 (1 - p_a) E_1 - \lambda_2 E_2, \\
I'(t) &= \lambda_2 E_2 - \mu I, \\
I_a'(t) &= \lambda_1 p_a E_1 - \mu I_a, \\
R'(t) &= \mu (I + I_a).
\end{aligned}
$$


### Parametrene

- $\beta$: **Smittefrekvens** mellom en smittet og en sårbar person.  
- $r_{ia}$: Relativ smittsomhet til asymptomatiske ($I_a$) sammenlignet med symptomatiske ($I$).  
- $r_{e2}$: Relativ smittsomhet til pre-symptomatiske ($E_2$).  
- $\lambda_1$: Hastighet for å gå fra $E_1 \to E_2$ eller $E_1 \to I_a$ (tilsvarer $1 /$ inkubasjonstid i første fase).  
- $\lambda_2$: Hastighet for å gå fra $E_2 \to I$ (tilsvarer $1 /$ inkubasjonstid i andre fase).  
- $p_a$: Sannsynlighet for å bli **asymptomatisk**.  
- $\mu$: Gjenopprettingsrate (tilsvarer $1 /$ varighet av infeksjon).
Nedenfor er noen realistiske, konstante verdier vi bruker i første oppgave.


| Parameter | Verdi |
|-----------|-------|
| $\beta$   | 0.33  |
| $r_{ia}$  | 0.1   |
| $r_{e2}$  | 1.25  |
| $\lambda_1$ | 0.33 |
| $\lambda_2$ | 0.5  |
| $p_a$    | 0.4   |
| $\mu$    | 0.2   |


![Demo](images/metrics_and_risk.png)
![Demo](images/plottssss.png)





