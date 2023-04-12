# P3 il migliore di  tutti
Seguendo le metodologie proposte al link segnalato: https://www.evanmiller.org/how-not-to-sort-by-average-rating.html
sono stati calcolati diversi ranking per classificare i giochi in scatola in base ai voti e al numero di votanti.
Il primo approccio è stato quello di calcolare la differenza tra voti positivi e negativi, poi è stato calcolato il rapporto tra i positivi e i totali, successivamente sono stati tentati degli approcci più strutturati, quello del limite inferiore dell'intervallo di confidenza di Wilson (che è quello suggerito dal blog) e l'approssimazione bayesiana.
Per valutare il migliore tra i ranking proposti è stato preso come benchmark un dataset BGG da Kaggle, contenente i dati su 20.343 giochi, dei quali 17.022 in comune con il dataset proposto.
Il miglior criterio di ranking è risultato essere quello di Wilson, correlato all 85% con il benchmark di BGG.
Infine è stata creata una classe Game che permette all'utente di filtrare il dataset al fine di consigliare quale possa essere "il migliore di tutti" i giochi in base alle sue preferenze.
