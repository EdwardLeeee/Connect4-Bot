import tkinter as tk
import numpy as np
import random
ROW_COUNT = 6
COLUMN_COUNT = 7
'''
mark:
e 記分公式
s 計算分數
m mini-max

o play_game1()
t play_game2()
'''
def create_board():
    return np.zeros((ROW_COUNT, COLUMN_COUNT), dtype=int)

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0#最上方還是0就還有位子

def get_next_open_row(board, col):#回傳最靠近下面的0在哪
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def winning_move(board, piece):
    # 水平
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                return True

    # 垂直
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                return True

    # 左下右上
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):#r越大越上面
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                return True

    # 左上右下
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                return True

def draw_board(canvas, board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-1, -1, -1):  # 從底部開始繪製range(起始值,終止值（不包含）,每回和加-1)

            # 將棋盤的背景設置為藍色,outline就是邊線
            canvas.create_rectangle(c * 200, (ROW_COUNT-1-r) * 200, (c + 1) * 200, (ROW_COUNT-r) * 200, fill="lightblue",outline="lightblue")

            #空白的圈圈
            canvas.create_oval(c * 200+10, (ROW_COUNT-1-r) * 200+10, (c + 1) * 200-10 , (ROW_COUNT-r) * 200-10, fill="white",outline="white")
            #擺棋子
            if board[r][c] == 1:
                canvas.create_oval(c * 200 + 20, (ROW_COUNT-1-r) * 200 + 20, (c + 1) * 200 - 20, (ROW_COUNT-r) * 200 - 20, fill="lightgreen",outline="lightgreen")
            elif board[r][c] == 2:
                canvas.create_oval(c * 200 + 20, (ROW_COUNT-1-r) * 200 + 20, (c + 1) * 200 - 20, (ROW_COUNT-r) * 200 - 20, fill="hotpink",outline="hotpink")
#做minimax
import math
import random

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2
WINDOW_LENGTH = 4

def evaluate_window(window, piece):
    #window 是ㄧ個連續的四個子
    score = 0
    opp_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE

    if window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 7
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 4

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 7
    elif window.count(opp_piece) == 2 and window.count(EMPTY) == 2:
        score -= 4

    return score

def score_position(board, piece):
    score = 0

    # Score center column
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]#中間column
    center_count = center_array.count(piece)#算有幾顆
    score += center_count * 4

    # Score Horizontal
    for r in range(ROW_COUNT):# 0-5
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT - 3):# 0-3
            window = row_array[c:c + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score Vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT - 3):
            window = col_array[r:r + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score positive sloped diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    # Score negative sloped diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score

def get_valid_locations(board):#用list回傳合法的位置
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    random.shuffle(valid_locations)#隨機排序可選的，每局才會隨機選分數一樣的位子
    return valid_locations

# 終結：無子可下或有勝者出現
def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

# depth就是遞迴深度,就是往後看幾手
def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:#遞迴中止條件
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 999 )
            elif winning_move(board, PLAYER_PIECE):
                return (None, -999)
            else:  # Game is over, no more valid moves
                return (None, 0)# Tie
        else:  # Depth is zero
            return (None, score_position(board, AI_PIECE))
    if maximizingPlayer:
        #maximixingPlayer = True ：最大化->自己
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)#下子
            new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else:  # Minimizing player：最小化->對手
        value = math.inf
        column = valid_locations[0]
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

def is_tie(board):
    return not any(0 in row for row in board)

def play_game1():
    board = create_board()
    game_over = False
    piece = 0

    def button_click(col):
        nonlocal piece, game_over
        if not game_over:
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, PLAYER_PIECE)
                draw_board(canvas, board)

                if winning_move(board, PLAYER_PIECE):
                    window = tk.Tk()
                    window.geometry("400x300")
                    window.title("Game Over")
                    window.config(bg='lightgreen')  # 設定視窗的背景顏色為淺藍色
                    window.resizable(False,False)
                    label = tk.Label(window, text="Player1 Win!!", font=('Arial', 20),justify='center', bg='lightgreen',fg='black')
                    label.place(relx=0.5, rely=0.5, anchor='center')
                    game_over = True

                if not game_over:
                    col, minimax_score = minimax(board, 6, -math.inf, math.inf, True)

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, AI_PIECE)
                        draw_board(canvas, board)

                        if winning_move(board, AI_PIECE):
                            window = tk.Tk()
                            window.geometry("400x300")
                            window.title("Game Over")
                            window.config(bg='hotpink')  # 設定視窗的背景顏色為pink
                            window.resizable(False,False)
                            label = tk.Label(window, text="Player2 Win!!", font=('Arial', 20),justify='center', bg='hotpink',fg='black')
                            label.place(relx=0.5, rely=0.5, anchor='center')
                            game_over = True

            #處理平手
            if is_tie(board):
                window = tk.Tk()
                window.geometry("400x300")
                window.title("Game Over")
                window.config(bg='lightskyblue')  # 設定視窗的背景顏色為淺灰色
                window.resizable(False,False)
                label = tk.Label(window, text="It's a Tie!!", font=('Arial', 20),justify='center', bg='lightskyblue',fg='black')
                label.place(relx=0.5, rely=0.5, anchor='center')
                game_over = True

    window = tk.Tk()
    window.title("Connect4")
    window.config(bg="lightblue")

    window.resizable(False,False)
    canvas = tk.Canvas(window, width=COLUMN_COUNT * 200, height=ROW_COUNT * 200)
    canvas.grid(row=0, columnspan=COLUMN_COUNT)  # 使用 grid 佈局

    for col in range(COLUMN_COUNT):
        button = tk.Button(window, text=f"Column {col+1}", command=lambda c=col: button_click(c),bg="lightskyblue")
        button.grid(row=1, column=col)  # 使用 grid 佈局
    draw_board(canvas, board)

def play_game2():
    board = create_board()
    game_over = False
    piece = 0

    def button_click(col):
        nonlocal piece, game_over
        if not game_over:

            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, piece + 1)

                if winning_move(board, piece + 1):
                    window = tk.Tk()
                    window.geometry("400x300")
                    window.title("Game Over")
                    window.resizable(False,False)
                    if piece == 0:
                        window.config(bg='lightgreen')  # 設定視窗的背景顏色為淺藍色
                        label = tk.Label(window, text="Player1 Win!!", font=('Arial', 20),justify='center', bg='lightgreen',fg='black')
                    else:
                        window.config(bg='hotpink')  # 設定視窗的背景顏色為淺藍色
                        label = tk.Label(window, text="Player2 Win!!", font=('Arial', 20),justify='center', bg='hotpink',fg='black')

                    label.place(relx=0.5, rely=0.5, anchor='center')
                    game_over = True

                draw_board(canvas, board)
                piece = (piece + 1) % 2

            #處理平手
            if is_tie(board):
                window = tk.Tk()
                window.geometry("400x300")
                window.title("Game Over")
                window.config(bg='lightskyblue')  # 設定視窗的背景顏色為淺灰色
                label = tk.Label(window, text="It's a Tie!!", font=('Arial', 20),justify='center', bg='lightskyblue',fg='black')
                label.place(relx=0.5, rely=0.5, anchor='center')
                game_over = True


    window = tk.Tk()
    window.title("Connect4")
    window.configure(bg="lightblue")
    window.resizable(False,False)
    canvas = tk.Canvas(window, width=COLUMN_COUNT * 200, height=ROW_COUNT * 200)#造一個畫布
    canvas.grid(row=0, columnspan=COLUMN_COUNT)

    for col in range(COLUMN_COUNT):
        button = tk.Button(window, text=f"Column {col+1}", command=lambda c=col: button_click(c),bg="lightskyblue")
        button.grid(row=1, column=col)
    draw_board(canvas, board)
    window.mainloop()


def exit_game():
    window.destroy()

window = tk.Tk()
window.geometry("1400x1200")
window.config(bg='lightblue')  # 設定視窗的背景顏色為淺藍色
window.title("Connect 4")
window.resizable(False,False)
play_button = tk.Button(window, text="人機對戰", command=play_game1)
play_button.config(height=5, width=20,bg='lightskyblue', fg='white',font=('Arial', 20))  # 設定按鈕的大小
play_button.pack(expand=True)  # 將按鈕放置在視窗的中間

play2_button = tk.Button(window, text="雙人對戰", command=play_game2)
play2_button.config(height=5, width=20,bg='deepskyblue', fg='white',font=('Arial',20))  # 設定按鈕的大小
play2_button.pack(expand=True)  # 將按鈕放置在視窗的中間

exit_button = tk.Button(window, text="離開", command=exit_game)
exit_button.config(height=5, width=20 ,bg='dodgerblue', fg='white',font=('Arial',20))  # 設定按鈕的大小
exit_button.pack(expand=True)  # 將按鈕放置在視窗的中間
window.mainloop()
