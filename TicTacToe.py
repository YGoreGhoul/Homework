from itertools import combinations


VICTORY_SUM = (6, 12, 15, 18, 24)   # используется для проверки условия победы


def introduction():
    return \
        """             Игра крестики-нолики для двоих            """


class Board:
    """Создается сетка 3x3 с обозначениями игроков"""

    def __init__(self):
        self.keys = self.values = range(1, 10)
        self._board_val = dict(zip(self.keys, self.values))

    def is_full(self):
        """
        Проверка на полное заполнение ячеек X или O.
        """
        return len(set(self._board_val.values())) == 2

    def reset(self):
        """Сбрасывает все значения ячеек. Используется для перезапуска."""
        self._board_val = dict(zip(self.keys, self.values))

    def update_position(self, cell, mark):
        """
        Добавляет новые ходы в ячейки
        """
        try:
            if self._board_val[cell] not in ("X", "O"):
                self._board_val[cell] = mark
                return True
            else:
                print(f" {cell} уже занята!")
                return False
        except KeyError:
            print("Нет такой ячейки. Пожалуйста, повторите ввод.")

    def __repr__(self):
        return f"""
              {self._board_val[1]} | {self._board_val[2]} | {self._board_val[3]}
             --- --- ---
              {self._board_val[4]} | {self._board_val[5]} | {self._board_val[6]}
             --- --- ---
              {self._board_val[7]} | {self._board_val[8]} | {self._board_val[9]}
            """


class Player:
    """Содержит информацию об имени игрока, фигуре. Добавляет ходы в сетку."""
    __instance = 1

    def __init__(self, name):
        self._name = name

        # назначение символа для хода игрока
        if Player.__instance == 1:
            self._mark_type = "X"
            Player.__instance += 1
        else:
            self._mark_type = "O"

    @property
    def mark_type(self):
        return self._mark_type

    def update_board(self, board_obj, cell):
        """Добавляет ход игрока в сетку"""
        return board_obj.update_position(cell, self._mark_type)

    def __repr__(self):
        return self._name


class GameController:
    """Записывает всю информацию об игроках, отслеживает их положение и контролирует общий ход игры."""

    def __init__(self):
        self._player_names = {}  # порядок игроков и их имена
        self._player_marks = {}  # список ходов каждого игрока

    def input_names(self):
        """Запрашивает имя игрока и сохраняет их."""

        for each in range(1, 3):
            while True:
                name = input(f"Игрок #{each}, введите своё имя: ")
                # проверка на то, что строка содержи символы
                if name.strip(" ") not in (" ", ""):
                    # проверка на то, что имена не повторяются
                    if name not in self._player_names.values():
                        self._player_names[each] = name
                        self._player_marks[name] = []
                        break
                    else:
                        print("Это имя уже занято. Пожалуйста, выберите другое.")
                else:
                    print("Ваше имя не может быть пустым.")
        print("Начнём игру!".center(40))

    @staticmethod
    def input_mark(player):
        """Вводит номер ячейки, чтобы походить"""
        while True:
            input_cell = input(f"{player}, выберите ячейку (0-9) для хода '{player.mark_type}' : ")
            try:
                return int(input_cell)
            except ValueError:
                print("Пожалуйста, введите номер ячейки, используя только цифры.")

    def check_victory(self, player):
        """
        Для каждого игрока создает уникальные комбинации из всех отмеченных ячеек и для каждой комбинации проверяет, является ли:
            1) сумма всех чисел равна любому значению из VICTORY_SUM
            2) существует не более 2 чисел, делящихся на 2
            3) все числа представляют собой арифметическую прогрессию с равной разницей
            4) комбинация не должна содержать пар чисел
            [3, 4] и [6, 7]
        """
        sorted_marks = sorted(self._player_marks[str(player)])
        combinations_ = combinations(sorted_marks, 3)
        for combi in combinations_:
            # проверка положения 1
            if sum(combi) in VICTORY_SUM:
                # проверка положения 2
                even_num = [num for num in combi if num % 2 == 0]
                if len(even_num) <= 2:
                    # проверка положения 3
                    if combi[2] - combi[1] == combi[1] - combi[0]:
                        # проверка положения 4
                        combi_list = list(combi)
                        combi_list.pop()
                        if combi_list != [3, 4] and combi_list != [6, 7]:
                            return True
        return False

    def gameplay(self, board_obj, player_1_obj, player_2_obj):
        """Меняет ход, ставит фигуры в сетку, проверка на победу."""
        while True:
            for player in (player_1_obj, player_2_obj):
                while True:
                    # получает номер ячейки для размещения фигурки игрока
                    cell = self.input_mark(player)
                    # обновляет сетку с новыми ходами
                    if player.update_board(board_obj, cell):
                        # добавляет ячейку в список игрока
                        # (нужно для проверки условия победы)
                        self.update_player_marks(player, cell)
                        print(board_obj)
                        if self.check_victory(player):
                            print(f"Побеждает {player}. Поздравляем!\n")
                            self.restart(board_obj)
                        if board_obj.is_full():
                            print("Это ничья!\n")
                            self.restart(board_obj)
                        break

    def restart(self, board_obj):
        """Спрашивает пользователя о перезапуске игры. Если ответ положительный, стирает все значения и фигурки с сетки."""
        while True:
            input_restart = input("Начать сначала? Y/N: ")
            if input_restart in ("Y", "y"):
                board_obj.reset()
                for key in self._player_marks.keys():
                    self._player_marks[key] = []
                print(board_obj)
                break
            elif input_restart in ("N", "n"):
                exit()
            else:
                print("Пожалуйста, выберите 'Y' или 'N' для ответа.")

    def update_player_marks(self, player, position):
        """Добавляет новый ход к счету игрока. Нужно для проверки условия победы."""
        self._player_marks[str(player)].append(position)

    def __getitem__(self, item):
        return self._player_names[item]


if __name__ == "__main__":
    # Введение
    print(introduction())
    while True:
        # создание сетки
        board = Board()

        tic_tac_toe = GameController()
        # вызывает имена игроков
        tic_tac_toe.input_names()

        first_player = Player(tic_tac_toe[1])
        second_player = Player(tic_tac_toe[2])
        # показывает сетку
        print(board)
        # начинает игру, меняет ход, проверяет условие победы и запрашивает перезапуск
        tic_tac_toe.gameplay(board, first_player, second_player)


