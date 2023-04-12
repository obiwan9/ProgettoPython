import scipy.stats as st
import math
import pandas as pd
import numpy as np
from scipy.stats import pearsonr
import scipy.stats as st

def differenza(game_col, rating_col):
    # Creazione del dataframe con le colonne "game" e "rating"
    df = pd.DataFrame({"game": game_col, "rating": rating_col})

    # Creazione di una colonna "rating>=6" contenente True per i valori di "rating" maggiori di 6 e False altrimenti
    df["rating>6"] = df["rating"] > 6

    # Raggruppamento del dataframe per "game" e calcolo delle differenze tra il conteggio di valori True e False nella colonna "rating>6"
    diff_df = df.groupby("game")["rating>6"].apply(lambda x: x.sum() - (len(x) - x.sum())).reset_index()
    diff_df.columns = ["game", "differenza"]

    return diff_df

def rapporto(game_col, rating_col):
    # Creazione del dataframe con le colonne "game" e "rating"
    df = pd.DataFrame({"game": game_col, "rating": rating_col})

    # Creazione di una colonna "rating>6" contenente True per i valori di "rating" maggiori di  6 e False altrimenti
    df["rating>=6"] = df["rating"] >= 6

    # Raggruppamento del dataframe per "game" e calcolo del rapporto tra il conteggio di valori True e il totale di valori nella colonna rating
    rapporto_df = df.groupby("game")["rating>=6"].apply(lambda x: x.sum() / len(x)).reset_index()
    rapporto_df.columns = ["game", "rapporto"]

    return rapporto_df


def conta_rating(data):
    """Conta i valori della colonna 'rating' raggruppati per la colonna 'game' e aggiunge una colonna 'totali' con il conteggio."""
    grouped = data.groupby('game')['rating'].count().reset_index()
    grouped.rename(columns={'rating': 'totali'}, inplace=True)
    result = pd.merge(data, grouped, on='game', how='left')
    return result

def conta_rating_positivi(data):
    """
    Conta i valori della colonna 'rating' maggiori di 6 raggruppati per la colonna 'game'
    e aggiunge una colonna 'positivi' con il conteggio. Se non ci sono valori positivi,
    restituisce conteggio 0.
    """
    high_ratings = data[data['rating'] >= 6]
    grouped = high_ratings.groupby('game')['rating'].count().reset_index()
    grouped.rename(columns={'rating': 'positivi'}, inplace=True)
    result = pd.merge(data, grouped, on='game', how='left')
    result['positivi'] = result['positivi'].fillna(0)
    return result

def unique_values(data, cols):
    """Restituisce un DataFrame contenente solo i valori univoci delle colonne specificate."""
    unique_data = data[cols].drop_duplicates()
    return unique_data

def wilson(pos, n, conf=0.95):
    """
calcola l’intervallo di confidenza di Wilson per una proporzione.
 Prende in input il numero di successi pos, il numero totale di tentativi n e un intervallo di confidenza conf che ha un valore predefinito del 95%.
 Se n è uguale a 0, la funzione restituisce 0.
  Altrimenti, calcola l’intervallo di confidenza utilizzando la formula data e restituisce il limite inferiore dell’intervallo.
    """
    if n == 0:
        return 0
    z = st.norm.ppf(1 - (1 - conf) / 2)
    phat = 1.0 * pos / n
    return (phat + z * z / (2 * n) - z * math.sqrt((phat * (1 - phat) + z * z / (4 * n)) / n)) / (1 + z * z / n)

#definisco una funzione conteggio_dei positivi che conti i raitng positivi totali

def bayesian_rating(n, conf=0.95):
    """
calcola il rating  bayesiano per un sistema di valutazione a N stelle.
 Prende in input un array n che rappresenta il conteggio delle valutazioni e un intervallo di confidenza
 conf che ha un valore predefinito del 95%.
  Se la somma degli elementi di n è uguale a 0, la funzione restituisce 0.
  Altrimenti, calcola il punteggio bayesiano utilizzando la formula data e restituisce il risultato.
    """
    if sum(n)==0:
        return 0
    K = len(n)
    z = st.norm.ppf(1 - (1 - conf) / 2)
    N = sum(n)
    first_part = 0.0
    second_part = 0.0
    for k, n_k in enumerate(n):
        first_part += (k+1)*(n[k]+1)/(N+K)
        second_part += (k+1)*(k+1)*(n[k]+1)/(N+K)
    score = first_part - z * math.sqrt((second_part - first_part*first_part)/(N+K+1))
    return score

def similarity(df):
    similarities = {}
    columns = list(df.columns)
    last_col = columns[-1]
    for i in range(1, len(columns)-1):
        col = columns[i]
        corr, _ = pearsonr(df[col], df[last_col])
        similarity = round((corr * 100), 2)
        key = f"{col} vs {last_col}"
        similarities[key] = similarity
    return pd.Series(similarities)




#Definisco la classe Game che filtri il Dataset in base agli input dati dall'utente
class Game:
    def __init__(self, data):
        self.data = data

    def filter(self):
        # Chiedi all'utente i parametri di filtraggio
        anno_minimo = int(input("Voglio un gioco che sia uscito dopo il: "))
        giocatori_minimi = int(input("Inserisci il numero minimo di giocatori: "))
        giocatori_massimi = int(input("Inserisci il numero massimo di giocatori: "))
        durata_massima = int(input("Quanto tempo hai a disposizione? (in minuti) "))
        eta_minima = int(input("Inserisci l'età minima: "))
        difficolta = input("Inserisci la complessità desiderata (alta/media/bassa): ")

        # Filtra i dati in base ai parametri di input

        filtered_data = self.data[
            (self.data["Year Published"] >= anno_minimo) &
            (self.data["Min Players"] >= giocatori_minimi) &
            (self.data["Max Players"] <= giocatori_massimi) &
            (self.data["Play Time"] <= durata_massima) &
            (self.data["Min Age"] >= eta_minima)
            ]

        if difficolta.lower() == "bassa":
            filtered_data = filtered_data[filtered_data["Complexity Average"] <= 2]
        elif difficolta.lower() == "media":
            filtered_data = filtered_data[
                (filtered_data["Complexity Average"] > 2) & (filtered_data["Complexity Average"] <= 3)]
        elif difficolta.lower() == "alta":
            filtered_data = filtered_data[filtered_data["Complexity Average"] > 3]

        # Estrai il gioco con il rating più alto
        game = filtered_data[filtered_data["Rating Average"] == filtered_data["Rating Average"].max()]["Name"].iloc[0]
        return print(
            f"Il miglior gioco di {difficolta} difficoltà uscito dopo il {anno_minimo} adatto ad un gruppo di {giocatori_minimi}-{giocatori_massimi} giocatori che abbiano più di {eta_minima} anni e che non duri più di {durata_massima} minuti è: {game}")




