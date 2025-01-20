#Import di tutte le librerie necessarie
import chess
import chess.engine
import time
import csv
from minimax_engine import MinimaxEngine
from alphabeta_engine import AlphaBetaEngine

#Creazione delle variabili engine_path. Queste prendono il percorso dell'eseguibile scaricato
stockfish_faster_path = r"stockfish-windows-x86-64-avx2\stockfish\stockfish-windows-x86-64-avx2.exe"
stockfish_moreCompatible_path = r"stockfish-windows-x86-64-sse41-popcnt\stockfish\stockfish-windows-x86-64-sse41-popcnt.exe"

#Usando la libreria "Chess engine" vengono create le variabili con l'engine al loro interno
#Engine1 = chess.engine.SimpleEngine.popen_uci(stockfish_faster_path)
#Engine2 = chess.engine.SimpleEngine.popen_uci(stockfish_moreCompatible_path)
Engine1 = MinimaxEngine(depth=6)
Engine2 = AlphaBetaEngine(depth=6)

#Qui viene invece richiesto l'inserimento del limite di tempo per ogni mossa,
#il numero di partite da giocare e come vengono definiti i possibili risultati
time_limit = float(input("Inserisci il tempo limite per ogni mossa: "))
num_games = int(input("Inserisci il numero di partite da far giocare: "))
results = {"1-0": 0, "0-1": 0, "1/2-1/2": 0}

#Viene definito come deve svolgersi la partita
#Nella funzione vengono passati come parametri i due engine che verranno poi salvati in un array.
#Viene creata poi la scacchiera e viene definito il turno al valore 0
#Poi, fino a che il gioco non sarà finito (per vittoria di uno dei 2 o pareggio), viene eseguito il comando "play".
#Questo salva le mosse in uno stack (che verrà passato fuori con il return) e aggiorna il turno ogni volta.
def play_game(engine1, engine2):
    board = chess.Board()
    engines = [engine1, engine2]
    turn = 0
    while not board.is_game_over():
        if isinstance(engines[turn], chess.engine.SimpleEngine):
            result = engines[turn].play(board, chess.engine.Limit(time=time_limit))
            move = result.move
        else:
            move = engines[turn].play(board).move  # Per gli algoritmi Python
        board.push(move)
        turn = 1 - turn
    return [board.result(), len(board.move_stack)]

#Qui, usando la libreria "CSV", viene aperto un file in quel formato in scrittura, che aggiungerà nelle righe seguenti
#a quanto già presente i risultati delle partite
with open('dati.csv', mode='a', newline='') as file:
    writer = csv.writer(file, delimiter=';')

    #Inizio del for che permette di fare tante partite quante specificate dall'utente
    #e in base al risultato di ciascuna viene scritto sul file
    for i in range(num_games):
        print("Inizio partita numero", i+1)
        result = play_game(Engine1, Engine2)
        results[result[0]] += 1
        print(f"Partita {i+1}: {result[0]}")
        if (result[0] == "1-0") :
            writer.writerow([1, 0, result[1]])
        if (result[0] == "0-1") :
            writer.writerow([0, 1, result[1]])
        if (result[0] == "1/2-1/2") :
            writer.writerow([0.5, 0.5, result[1]])

    #Ora vengono scritti i totali delle partite (dopo aver lasciato uno spazio)
    writer.writerow([])

    writer.writerow([f"VB: {results['1-0']}", f"VN: {results['0-1']}", f"Draws: {results['1/2-1/2']}"])

    writer.writerow("")
    
#Chiusura degli engine
try:
    Engine1.quit()
    Engine2.quit()
except AttributeError:
    pass  # Se non c'è il metodo, ignora l'errore

#Scrittura su terminale
print(f"Results after {num_games} games:")
print(f"Engine 1 wins: {results['1-0']}")
print(f"Engine 2 wins: {results['0-1']}")
print(f"Draws: {results['1/2-1/2']}")