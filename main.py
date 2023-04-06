import tkinter as tk
import numpy as np

# Initialisation du tableau de jeu
board = np.array([[0, 1, 0, 1, 0, 1, 0, 1],
                  [1, 0, 1, 0, 1, 0, 1, 0],
                  [0, 1, 0, 1, 0, 1, 0, 1],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0],
                  [2, 0, 2, 0, 2, 0, 2, 0],
                  [0, 2, 0, 2, 0, 2, 0, 2],
                  [2, 0, 2, 0, 2, 0, 2, 0]])

# Initialisation des variables
current_player = 1
selected_piece = None
moves = []


# Fonction pour dessiner la grille de jeu
def draw_board():
    for row in range(8):
        for col in range(8):
            if board[row][col] == 1:
                color = "#cc6600"
            elif board[row][col] == 2:
                color = "#e6e600"
            else:
                color = "white"
            canvas.create_rectangle(col * 50, row * 50, col * 50 + 50, row * 50 + 50, fill=color)
    root.update()


# Fonction pour sélectionner un pion
def select_piece(event):
    global selected_piece, moves
    col = event.x // 50
    row = event.y // 50
    if board[row][col] == current_player:
        selected_piece = (row, col)
        moves = get_valid_moves(row, col)
        highlight_moves(moves)
    else:
        selected_piece = None


# Fonction pour déplacer un pion
def move_piece(event):
    global current_player, selected_piece
    col = event.x // 50
    row = event.y // 50
    if (row, col) in moves:
        board[row][col] = current_player
        board[selected_piece] = 0
        if abs(selected_piece[0] - row) == 2:
            jump_piece(selected_piece, (row, col))
            moves = get_valid_moves(row, col)
            if moves and abs(selected_piece[0] - row) == 2:
                selected_piece = (row, col)
                highlight_moves(moves)
                return
        current_player = 3 - current_player
        selected_piece = None
        draw_board()


# Fonction pour mettre en évidence les coups possibles
def highlight_moves(moves):
    for move in moves:
        canvas.create_rectangle(move[1] * 50, move[0] * 50, move[1] * 50 + 50, move[0] * 50 + 50, fill="yellow")


# Fonction pour obtenir les mouvements valides pour un pion donné
def get_valid_moves(row, col):
    moves = []
    if board[row][col] == 1 or board[row][col] == 3:
        if row > 0 and col > 0 and board[row - 1][col - 1] == 0:
            moves.append((row - 1, col - 1))
            if row > 0 and col < 7 and board[row - 1][col + 1] == 0:
                moves.append((row - 1, col + 1))
                if board[row][col] == 3:
                    if row < 7 and col > 0 and board[row + 1][col - 1] == 0:
                        moves.append((row + 1, col - 1))
                        if row < 7 and col < 7 and board[row + 1][col + 1] == 0:
                            moves.append((row + 1, col + 1))
                            if board[row][col] == 2 or board[row][col] == 3:
                                if row < 7 and col > 0 and board[row + 1][col - 1] == 0:
                                    moves.append((row + 1, col - 1))
                                    if row < 7 and col < 7 and board[row + 1][col + 1] == 0:
                                        moves.append((row + 1, col + 1))
                                        if board[row][col] == 3:
                                            if row > 0 and col > 0 and board[row - 1][col - 1] == 0:
                                                moves.append((row - 1, col - 1))
                                                if row > 0 and col < 7 and board[row - 1][col + 1] == 0:
                                                    moves.append((row - 1, col + 1))
                                                    if board[row][col] == 1:
                                                        for move in get_jumps(row, col, [(row, col)], []):
                                                            moves.append(move)
                                                            if board[row][col] == 2:
                                                                for move in get_jumps(row, col, [(row, col)], []):
                                                                    moves.append(move)
                                                                    return moves


#Fonction pour obtenir les sauts valides pour un pion donné
def get_jumps(row, col, path, jumps):
    if board[row][col] == 1 or board[row][col] == 3:
        if row > 1 and col > 1 and board[row - 1][col - 1] in [2, 4] and (row - 2, col - 2) not in path:
            new_path = path + [(row - 2, col - 2)]
            new_jumps = jumps + [(row - 2, col - 2)]
            new_jumps += get_jumps(row - 2, col - 2, new_path, new_jumps)

            if row > 1 and col < 6 and board[row - 1][col + 1] in [2, 4] and (row - 2, col + 2) not in path:
                new_path = path + [(row - 2, col + 2)]
                new_jumps = jumps + [(row - 2, col + 2)]
                new_jumps += get_jumps(row - 2, col + 2, new_path, new_jumps)
                if board[row][col] == 3:
                    if row < 6 and col > 1 and board[row + 1][col - 1] in [2, 4] and (row + 2, col - 2) not in path:
                        new_path = path + [(row + 2, col - 2)]
                        new_jumps = jumps + [(row + 2, col - 2)]
                        new_jumps += get_jumps(row + 2, col - 2, new_path, new_jumps)
                        if row < 6 and col < 6 and board[row + 1][col + 1] in [2, 4] and (row+2, col+2) not in path:
                            new_path = path + [(row+2, col+2)]
                            new_jumps = jumps + [(row+2, col+2)]
                            new_jumps += get_jumps(row+2, col+2, new_path, new_jumps)
                            if board[row][col] == 2 or board[row][col] == 3:
                                if row < 6 and col > 1 and board[row+1][col-1] in [1, 3] and (row+2, col-2) not in path:
                                    new_path = path + [(row+2, col-2)]
                                    new_jumps = jumps + [(row+2, col-2)]
                                    new_jumps += get_jumps(row+2, col-2, new_path, new_jumps)
                                    if row < 6 and col < 6 and board[row+1][col+1] in [1, 3] and (row+2, col+2) not in path:
                                        new_path = path + [(row+2, col+2)]
                                        new_jumps = jumps + [(row+2, col+2)]
                                        new_jumps += get_jumps(row+2, col+2, new_path, new_jumps)
                                        if board[row][col] == 3:
                                            if row > 1 and col > 1 and board[row-1][col-1] in [1, 3] and (row-2, col-2) not in path:
                                                new_path = path + [(row-2, col-2)]
                                                new_jumps = jumps + [(row-2, col-2)]
                                                new_jumps += get_jumps(row-2, col-2, new_path, new_jumps)
                                                if row > 1 and col < 6 and board[row-1][col+1] in [1, 3] and (row-2, col+2) not in path:
                                                    new_path = path + [(row-2, col+2)]
                                                    new_jumps = jumps + [(row-2, col+2)]
                                                    new_jumps += get_jumps(row-2, col+2, new_path, new_jumps)
                                                    return jumps

#Fonction pour effectuer un mouvement
def make_move(move):
    global board, selected_piece, turn
    row, col = move[0], move[1]
    board[row][col] = board[selected_piece[0]][selected_piece[1]]
    board[selected_piece[0]][selected_piece[1]] = 0
    if abs(selected_piece[0] - row) == 2:
        board[(selected_piece[0]+row)//2][(selected_piece[1]+col)//2] = 0
        if row == 0 and board[row][col] == 1:
            board[row][col] = 3
            if row == 7 and board[row][col] == 2:
                board[row][col] = 4
                selected_piece = None
                turn = 3 - turn

#Fonction pour vérifier s'il y a un gagnant
def check_winner():
    if not any(1 in row for row in board):
        return 2
        if not any(2 in row for row in board):
            return 1
        return None

#Fonction pour afficher l'état du plateau
def display_board():
    SQUARE_SIZE = 80
    global canvas, board_images
    canvas.delete("piece")
    for row in range(8):
        for colin in range(8):
            if (row + col) % 2 == 0:
                canvas.create_rectangle(col*SQUARE_SIZE, row*SQUARE_SIZE, (col+1)*SQUARE_SIZE, (row+1)*SQUARE_SIZE, fill="#f0d9b5")
            else:
                canvas.create_rectangle(col*SQUARE_SIZE, row*SQUARE_SIZE, (col+1)*SQUARE_SIZE, (row+1)*SQUARE_SIZE, fill="#b58863")
                if board[row][col] != 0:
                    canvas.create_image(col*SQUARE_SIZE+SQUARE_SIZE//2, row*SQUARE_SIZE+SQUARE_SIZE//2, image=board_images[board[row][col]-1], tags="piece")

#Fonction appelée lorsqu'un joueur clique sur une case
def on_click(event):
    global selected_piece, turn, moves
    if turn == 1:
        color = "red"
    else:
        color = "white"
    col = event.x // SQUARE_SIZE
    row = event.y // SQUARE_SIZE
    if selected_piece is None:
        if board[row][col] != 0 and board[row][col] // 2 == turn - 1:
            selected_piece = (row, col)
            moves = get_moves(row, col)
            jumps = get_jumps(row, col)
            if jumps:
                moves = jumps
                draw_moves(moves, color)
            else:
                if (row, col) in moves:
                    make_move((row, col))
                    winner = check_winner()
                    if winner is not None:
                        messagebox.showinfo("Fin de partie", f"Le joueur {winner} a gagné!")
                    else:
                        display_board()
                        if not jumps:
                            turn = 3 - turn
                            if turn == 1:
                                messagebox.showinfo("Tour du joueur rouge", "C'est à vous de jouer!")
                            else:
                                messagebox.showinfo("Tour du joueur blanc", "C'est à vous de jouer!")
                        else:
                            selected_piece = (row, col)
                            moves = get_moves(row, col)
                            draw_moves(moves, color)
        else:
            selected_piece = None
            moves = []
    elif (row, col) == selected_piece:
        selected_piece = None
        moves = []
    elif (row, col) in moves:
        make_move((row, col))
        winner = check_winner()
        if winner is not None:
            messagebox.showinfo("Fin de partie", f"Le joueur {winner} a gagné!")
        else:
            display_board()
            jumps = get_jumps(row, col)
            if jumps:
                selected_piece = (row, col)
                moves = jumps
                draw_moves(moves, color)
            else:
                selected_piece = None
                moves = []
                turn = 3 - turn
                if turn == 1:
                    messagebox.showinfo("Tour du joueur rouge", "C'est à vous de jouer!")
                else:
                    messagebox.showinfo("Tour du joueur blanc", "C'est à vous de jouer!")
    else:
        selected_piece = None
        moves = []

#Création de la fenêtre principale
WIDTH = 600
HEIGHT = 600

root = tk.Tk()
root.title("Jeu de dames")
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
canvas.pack()

#Création du canvas pour afficher le plateau
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
canvas.pack()

#Chargement des images des pièces
board_images = [tk.PhotoImage(file=f"{piece}.png") for piece in ["pionrouge", "pionblanc", "pionrouge", "pionblanc"]]

#Initialisation du plateau
board = np.zeros((8, 8))
for row in range(8):
    for col in range(8):
        if (row + col) % 2 == 0:
            if row < 3:
                board[row][col] = 1
            elif row > 4:
                board[row][col] = 2

#Initialisation des variables globales
selected_piece = None
moves = []
turn = 1

#Affichage initial du plateau
display_board()

#Liaison de l'événement clic de la souris à la fonction on_click
canvas.bind("<Button-1>", on_click)

#Affichage de la fenêtre principale
root.mainloop()
