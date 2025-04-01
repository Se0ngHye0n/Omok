import turtle
import tkinter as tk
from tkinter import messagebox
import sys
import time
import board
from game import Game
from ai import iterative_deepening


# Tkinter 루트 윈도우 숨기기
root = tk.Tk()
root.withdraw()

response = messagebox.askyesno("선, 후공 선택", "선공하시겠습니까?")
if response:
    HUMAN_PLAYER = 'X'
    AI_PLAYER = 'O'
    user_first = True
else:
    HUMAN_PLAYER = 'O'
    AI_PLAYER = 'X'
    user_first = False

game = Game()

# 오목판 그리기
board.init_board()
board.draw_grid()
board.draw_flower_points()
board.draw_labels()
turtle.update()

# AI 선공일 경우 첫 수 두기
if not user_first:
    board.write_ai_message("AI Thinking...")
    turtle.update()
    time.sleep(0.5)
    center = board.BOARD_SIZE // 2
    board.place_stone(center, center, AI_PLAYER)
    board.clear_ai_message()
    board.write_user_message("User Thinking...")
    turtle.update()
else:
    board.write_user_message("User Thinking...")
    turtle.update()

# 마우스 클릭
def handle_click(x, y):
    turtle.update()

    col = round((x - board.start_x) / board.CELL_SIZE)
    row = round((board.start_y - y) / board.CELL_SIZE)

    if 0 <= row < board.BOARD_SIZE and 0 <= col < board.BOARD_SIZE:
        state = board.get_board()
        if state[row][col] is None:
            board.place_stone(row, col, HUMAN_PLAYER)
            turtle.update()

            if game.is_terminal(state):
                board.clear_user_message()
                print("게임 종료 (사용자 승리)")
                return

            board.clear_user_message()

            board.write_ai_message("AI Thinking...")
            turtle.update()

            ai_move = iterative_deepening(game, state, max_time= 10.0)
            board.clear_ai_message()

            if ai_move:
                r, c = ai_move
                board.place_stone(r, c, AI_PLAYER)
                turtle.update()

                if game.is_terminal(board.get_board()):
                    board.clear_ai_message()
                    print("게임 종료 (AI 승리)")
                else:
                    board.write_user_message("User Thinking...")
                    turtle.update()

def quit_program():
    sys.exit()

# 클릭 이벤트 바인딩
turtle.onscreenclick(handle_click)

# 창 닫기
canvas = turtle.getcanvas()
window = canvas.winfo_toplevel()
window.protocol("WM_DELETE_WINDOW", quit_program)

# 메인 루프
turtle.done()
