## Modelering av pandemi med ODE og Python 
I denne oppgaven skal implementeres en ODE-basert versjon av SEEIIR-modellen, som tilsvarer modellen  Folkehelseinstituttet brukte for å beskrive spredningen av Covid-19-pandemien. Oppgaven implementere  modellen som et system av differensialligninger og simulerer smitteutviklignen over tid av smitteutviklingen over tid. Oppgaven tar utgangspunkt i modellen beskrevet i kapittel 5 i boken ([Solving
Ordinary Differential Equations in Python](https://link.springer.com/book/10.1007/978-3-031-46768-4)). 

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

## SEEIIR-modellen



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

## Modelering av den enkleste modellen, med konstante parametere 
### (scriptet SEIR0.py)
Vi tar utgangspunkt i startverdiene: 
  - **S_0** = $5.5 \times 10^{6}$ 
  - **E₂_0** = 100
  - **E₁_0** = **Iₐ** = **R** = **I** = 0
  - **T** = 200 (vi modelerer over 200 dager)
  - **N** = 400 (vi bruker 400 datapunkter).
#### Dersom vi setter $\beta$ konstant lik 0.33 gir det plottet
  
![Demo](images/seiro_beta_033.png) 
#### Dersom vi øker $\beta$, altså har en høyere smittefrekvens gir dette vi plottet

![Demo](images/seiro_beta_04.png)

Av figurene ser man først og fremst at antall personer som blir immune (\(R(t)\)) øker raskt over tid. Når smittefrekvensen ($\beta$) økes, stiger også kurven for immune raskere, fordi flere individer smittes og går gjennom sykdomsforløpet før de til slutt når \(R\). Dette kommer av at systemet for differensiallikninger, der vi har

$$
E_1'(t) =
\frac{\beta S I}{N} + r_i \frac{\beta S I_a}{N} + r_e^2 \frac{\beta S E_2}{N},
\$$

Antall smittede som ikke merker symptomer øker når $\beta$ øker, som igjen har ringvirkninger for de andre sykdomsgruppene. Modellen viser dermed at selv små endringer i ($\Delta$ $\beta$ = 0.4-0.33=0.07) har stor effekt på hvor raskt befolkningen oppnår immunitet. Plottene viser også at vesentlig flere blir imune med høyere smittefrekvens $\beta$, noe som gir mening, da flere gjennomgår et sykdomsforløp. 
 




