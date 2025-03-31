import turtle
import board


# 오목판 그리기
board.init_board()
board.draw_grid()
board.draw_flower_points()
board.draw_labels()
turtle.update()

# 클릭 이벤트 바인딩
turtle.onscreenclick(board.handle_click)

# 메인 루프
turtle.done()
