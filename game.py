import copy
import board


class Game:

    def __init__(self):
        self.BOARD_SIZE = board.BOARD_SIZE

    def player_turn(self, state):  # 누가 둘 차례인지 확인
        x_count = sum(row.count('X') for row in state)
        o_count = sum(row.count('O') for row in state)
        return 'X' if x_count <= o_count else 'O'

    def opponent_turn(self, player):  # 순서 교대
        return 'O' if player == 'X' else 'X'

    def valid_loc(self, state):  # 돌이 인접한 위치 반환
        x_count = sum(row.count('X') for row in state)
        y_count = sum(row.count('O') for row in state)
        move_count = x_count + y_count
        if move_count < 10:
            distance = 1
        else:
            distance = 2

        loc = []
        for r in range(self.BOARD_SIZE):
            for c in range(self.BOARD_SIZE):
                if state[r][c] is None and self._has_neighbor(state, r, c, distance):
                    loc.append((r, c))
        return loc

    def _has_neighbor(self, state, r, c, distance):  # 주변에 돌이 있는지 확인
        for dr in range(-distance, distance + 1):
            for dc in range(-distance, distance + 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.BOARD_SIZE and 0 <= nc < self.BOARD_SIZE:
                    if state[nr][nc] is not None:
                        return True
        return False

    def state_update(self, state, action, player):  # 돌을 두고 난 후 state 반환
        r, c = action
        new_state = copy.deepcopy(state)
        new_state[r][c] = player
        return new_state

    def is_terminal(self, state):  # 게임이 끝났는지 확인
        return self._winner(state) is not None

    def evaluate(self, state, player):  # value 평가
        opponent = self.opponent_turn(player)
        player_score = self._pattern(state, player)
        opponent_score = self._pattern(state, opponent)
        return player_score - opponent_score

    def _check(self, state, r, c, dr, dc, player):  # 돌이 한줄로 놓인 개수와 막혀 있는지 여부 확인
        prev_r = r - dr
        prev_c = c - dc

        if 0 <= prev_r < self.BOARD_SIZE and 0 <= prev_c < self.BOARD_SIZE:
            if state[prev_r][prev_c] == player:
                return 0, 0

        count = 1
        blocked = 0

        for k in range(1, 5):
            nr = r + dr * k
            nc = c + dc * k
            if 0 <= nr < self.BOARD_SIZE and 0 <= nc < self.BOARD_SIZE:
                if state[nr][nc] == player:
                    count += 1
                elif state[nr][nc] is not None:
                    blocked += 1
            else:
                blocked += 1
        return count, blocked

    def _pattern(self, state, player):  # 상황에 따라 가중치 부여
        direction = [(0, 1), (1, 0), (1, 1), (1, -1)]  # 오른쪽, 아래쪽, 우측 하단, 좌측 하단
        score = 0

        for r in range(self.BOARD_SIZE):
            for c in range(self.BOARD_SIZE):
                if state[r][c] != player:
                    continue
                for dr, dc in direction:
                    count, blocked = self._check(state, r, c, dr, dc, player)

                    # 점수 부여 (중복 방지 후만 적용)
                    if count == 5:
                        score += 100000
                    elif count == 4 and blocked == 0:
                        score += 10000
                    elif count == 4 and blocked == 1:
                        score += 5000
                    elif count == 3 and blocked == 0:
                        score += 1000
                    elif count == 3 and blocked == 1:
                        score += 500
                    elif count == 2 and blocked == 0:
                        score += 100
        return score

    def _winner(self, state):  # 현재 상황에서 승자가 있는지 확인
        direction = [(0, 1), (1, 0), (1, 1), (1, -1)]  # 오른쪽, 아래쪽, 우측 하단, 좌측 하단

        for r in range(self.BOARD_SIZE):
            for c in range(self.BOARD_SIZE):
                if state[r][c] is None:
                    continue
                player = state[r][c]
                for dr, dc in direction:
                    count, _ = self._check(state, r, c, dr, dc, player)
                    if count == 5:
                        return player
        return None
