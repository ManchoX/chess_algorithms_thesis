import pandas as pd
import matplotlib.pyplot as plt

# Leggi il file CSV con tabulazione come delimitatore e senza header
df = pd.read_csv("dati_houdini_vs_critter_2s.csv", delimiter=";", header=None, dtype=str)

# Visualizza le prime righe per controllare eventuali errori nei dati
print(df.head())
print(df.info())

df = df.dropna(axis=1, how='all')

df.columns = ["White_Result", "Black_Result", "Moves"]
df = df.dropna(subset=["Moves"])  # Rimuove le righe con NaN nella colonna "Moves"
df["White_Result"] = df["White_Result"].astype(float)
df["Black_Result"] = df["Black_Result"].astype(float)
df["Moves"] = df["Moves"].astype(int)

print(df["Moves"].isnull().sum())  # Conta quanti valori NaN ci sono
print(df["Moves"].head())

# Calcola le vittorie, le sconfitte e i pareggi
white_wins = (df["White_Result"] == 1).sum()  # Vittorie del bianco
black_wins = (df["Black_Result"] == 1).sum()  # Vittorie del nero
draws = ((df["White_Result"] == 0.5) & (df["Black_Result"] == 0.5)).sum()  # Pareggi

print(f"White wins: {white_wins}")
print(f"Black wins: {black_wins}")
print(f"Draws: {draws}")

labels = ["White Wins", "Black Wins", "Draws"]
values = [white_wins, black_wins, draws]

plt.bar(labels, values, color=['white', 'black', 'gray'], edgecolor='black')
plt.title("Results of Chess Matches")
plt.ylabel("Number of Games")
plt.show()

plt.hist(df["Moves"], bins=10, color='purple', edgecolor='black')
plt.title("Distribution of Number of Moves")
plt.xlabel("Number of Moves")
plt.ylabel("Frequency")
plt.show()