# Simulering av smittespredning med ODE-modeller i Python
I denne oppgaven skal implementeres en ODE-basert versjon av SEEIIR-modellen, som tilsvarer modellen  Folkehelseinstituttet (FHI) brukte for å beskrive spredningen av Covid-19-pandemien. Oppgaven implementere  modellen som et system av differensialligninger og simulerer smitteutviklignen over tid av smitteutviklingen over tid. Oppgaven tar utgangspunkt i modellen beskrevet i kapittel 5 i boken ([Solving
Ordinary Differential Equations in Python](https://link.springer.com/book/10.1007/978-3-031-46768-4)). 

### Notasjonen i oppgaven

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



## Modelering med konstante parametere 
### ([scriptet SEIR0.py](https://github.com/ragnhild-thielemann/Oblig-IN1900/blob/main/scr/SEIR0.py))
#### Realistiske, konstante verdier for modellering

| Parameter | Verdi |
|-----------|-------|
| $\beta$   | 0.33  |
| $r_{ia}$  | 0.1   |
| $r_{e2}$  | 1.25  |
| $\lambda_1$ | 0.33 |
| $\lambda_2$ | 0.5  |
| $p_a$    | 0.4   |
| $\mu$    | 0.2   |

#### Startverdier for befolknigen
  - **S_0** = $5.5 \times 10^{6}$ 
  - **E₂_0** = 100
  - **E₁_0** = **Iₐ** = **R** = **I** = 0
  - **T** = 200 (vi modelerer over 200 dager)
  - **N** = 400 (vi bruker 400 datapunkter).
#### Dersom vi setter $\beta$ konstant lik 0.33 gir det plottet
  
![Demo](images/seiro_beta_033.png) 
#### Dersom vi øker $\beta$, altså har en høyere smittefrekvens gir dette vi plottet

![Demo](images/seiro_beta_04.png)

Av figurene ser man først og fremst at antall personer som blir immune $(\(R(t)\))$ øker raskt over tid. Når smittefrekvensen ($\beta$) økes, stiger også kurven for immune raskere, fordi flere individer smittes og går gjennom sykdomsforløpet før de til slutt når $\(R\).$ Dette kommer av at systemet for differensiallikninger, der vi har

$$
E_1'(t) =
\frac{\beta S I}{N} + r_i \frac{\beta S I_a}{N} + r_e^2 \frac{\beta S E_2}{N},
\$$

Antall smittede som ikke merker symptomer øker når $\beta$ øker, som igjen har ringvirkninger for de andre sykdomsgruppene. Modellen viser dermed at selv små endringer i ($\Delta$ $\beta$ = 0.4-0.33=0.07) har stor effekt på hvor raskt befolkningen oppnår immunitet. Plottene viser også at vesentlig flere blir imune med høyere smittefrekvens $\beta$, noe som gir mening, da flere gjennomgår et sykdomsforløp. 


## Modelering med variabel verdi for smitterate
### ([scriptet outbreak.py](https://github.com/ragnhild-thielemann/Oblig-IN1900/blob/main/scr/outbreak.py))

Når en pandemi intreffer, er vil myndighetene med all sansynlighet sette inn tiltak for at smittefrekvensen ($\beta$) avtar. I første del av å gjøre modellen mer realistisk, oppretter vi en "piecewise function" for smittefrekvensen, der smittefrekvensen avtar over tid. Vi setter smittefrekvensen til 0.4 de 100 dagene før myndighetene har satt inn virksomme tiltak, og 0.083 etter myndightene har satt inn tiltak. 

$$
\beta(t) =
\begin{cases}
0.4, & \text{for } t < 100, \\
0.083, & \text{for } t \geq 100.
\end{cases}
$$ 

Det gir følgene plot for sykdomsutviklingen i de ulike befolkningsgruppene

![Demo](images/varierene_beta.png) 

Simuleringen viser hvordan nedstengingen som innføres etter 100 dager får smittespredningen til å avta betydelig og flate ut. Både antall smitteutsatte og antall imune stabiliserer seg, da sykdomspredningen i befolkningen er tilnærmet lik 0. ($\beta$ = 0.083). Norge var ikke forberedt på en pandemi, men ved at smitten ble brems, fikk helsevesenet tid til å tilpasse kapasiteten, bestille nødvendig utstyr som munnbind og respiratorer, og organisere test- og karantenetiltak for å håndtere sykdommen mer effektivt. Å bremse sykdomspredningen var nødvendig for å hindre dødsfall.

### Estimering av antall respiratorplasser som kreves
I ([scriptet SEIR.py](https://github.com/ragnhild-thielemann/Oblig-IN1900/blob/main/scr/SEIR.py) estimerte  hvor mange respiratorplasser som vi hadde krevd dersom, dersom myndighetene ikke hadde iverksatt tiltak.($\beta$ med konstant verdi på 0.33) Vi la til grunn at 20 % av de smittede med Covid-19 utvikler alvorlig sykdom, og at 5 % av disse igjen ville trenge respiratorbehandling.

Beregningene våre viste et maksimalt behov på 1423 respiratorplasser, altså mer enn dobbelt så mange som den tilgjengelige kapasiteten på 700 plasser. Dette illustrerer tydelig hvor kritisk det var å sette inn tiltak for å redusere smittespredning og forhindre unødvendige dødsfall. 

## Modellering med reele verdier for smitterate

I siste del av prosjektet brukte vi FHIs verdier for smitterate ($\beta$) for å lage en mer relistisk modell for sykdomsutviklingen. I scriptet ([lockdown.py](https://github.com/ragnhild-thielemann/Oblig-IN1900/blob/main/scr/lockdown.py)) er det en klasse, som behandler dataene i tekstfilen beta.txt, slik at vi får to arrays. Disse arrayene plottes, slik at vi visuelt ser hvordan smitteraten ($\beta$) utvikler seg over tid. 

![Demo](images/beta_verdier_bilde.png)

