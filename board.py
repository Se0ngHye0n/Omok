import turtle


BOARD_SIZE = 19
CELL_SIZE = 30
BOARD_LENGTH = CELL_SIZE * (BOARD_SIZE - 1)

start_x = -BOARD_LENGTH // 2
start_y = BOARD_LENGTH // 2 - 50


user_msg = turtle.Turtle()
user_msg.hideturtle()
user_msg.penup()
user_msg.color("black")

ai_message = turtle.Turtle()
ai_message.hideturtle()
ai_message.penup()
ai_message.color("black")

# 오목판 상태 저장 (빈칸은 None)
board = []
for _ in range(BOARD_SIZE):
    row = []
    for _ in range(BOARD_SIZE):
        row.append(None)
    board.append(row)

def get_board():
    return board

current_player = "X"  # 흑: X, 백: O

# 터틀 초기화
def init_board():
    turtle.title("Omok (Adversarial Search Homework)")
    turtle.setup(width=650, height=700)
    turtle.speed(0)
    turtle.hideturtle()
    turtle.tracer(False)  # 오목판 한번에 생성
    turtle.penup()
    turtle.bgcolor("#f2b06d")

# 오목판 그리기
def draw_grid():
    for i in range(BOARD_SIZE):
        y = start_y - i * CELL_SIZE
        turtle.penup()
        turtle.goto(start_x, y)
        turtle.pendown()
        turtle.forward(BOARD_LENGTH)

    for i in range(BOARD_SIZE):
        x = start_x + i * CELL_SIZE
        turtle.penup()
        turtle.goto(x, start_y)
        turtle.setheading(-90)
        turtle.pendown()
        turtle.forward(BOARD_LENGTH)

# 화점
def draw_flower_points():
    flower_positions = [3, 9, 15]
    for x in flower_positions:
        for y in flower_positions:
            draw_dot_at(x, y)

# 화점 찍기
def draw_dot_at(x_idx, y_idx):
    x = start_x + x_idx * CELL_SIZE
    y = start_y - y_idx * CELL_SIZE
    turtle.penup()
    turtle.goto(x, y)
    turtle.dot(6, "black")

# 좌표 표시
def draw_labels():
    font = ("Arial", 10, "normal")

    for i in range(BOARD_SIZE):
        x = start_x + i * CELL_SIZE
        y = start_y + CELL_SIZE // 2
        turtle.penup()
        turtle.goto(x, y)
        turtle.write(str(i + 1), align="center", font=font)

    for i in range(BOARD_SIZE):
        x = start_x - CELL_SIZE // 2
        y = start_y - i * CELL_SIZE
        letter = chr(65 + i)
        turtle.penup()
        turtle.goto(x, y - 7.5)
        turtle.write(letter, align="right", font=font)

def write_user_message(msg, color= "black"):
    user_msg.clear()
    user_msg.goto(-200, turtle.window_height() // 2 - 60)
    user_msg.write(msg, align= "center", font= ("Arial", 14, "bold"))
    turtle.update()

def clear_user_message():
    user_msg.clear()
    turtle.update()

def write_ai_message(msg, color= "black"):
    ai_message.clear()
    ai_message.goto(200, turtle.window_height() // 2 - 60)
    ai_message.write(msg, align= "center", font= ("Arial", 14, "bold"))
    turtle.update()

def clear_ai_message():
    ai_message.clear()
    turtle.update()

# 돌 놓기
def place_stone(row, col, player):
    x = start_x + col * CELL_SIZE
    y = start_y - row * CELL_SIZE
    turtle.penup()
    turtle.goto(x, y)

    if player == 'X':
        turtle.dot(20, "black")
    elif player == 'O':
        turtle.dot(20, "white")  # 흰색 돌 중심
        turtle.pencolor("black")
        turtle.setheading(0)
        turtle.penup()
        turtle.goto(x, y - 10)  # 외곽선을 정확히 중심에 맞춰서
        turtle.pendown()
        turtle.circle(10)
        turtle.penup()

    board[row][col] = player
