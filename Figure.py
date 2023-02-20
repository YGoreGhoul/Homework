#класс хранящий свойства и методы для фигур
class Checkers:

    playerControl = None
    min_length = 0
    max_length = 7

# инициализация данных
    def __init__(self, location, player_control, figure_type):
        self.location = location
        self.type = figure_type
        self.playerControl = player_control

    # превращение шашки в дамку
    def update_type(self):
        self.type = "Queen"

    # перемещение фигуры,если фигура доходит до края доски, то превратить в дамку
    def move_to(self, x, y):
        match self.playerControl:
            case True:
                self.location[0] = x
                self.location[1] = y
                if self.location[1] == Checkers.max_length and self.type != "Queen":
                    self.update_type()
            case False:
                self.location[0] = x
                self.location[1] = y
                if self.location[1] == Checkers.min_length and self.type != "Queen":
                    self.update_type()

#Класс содержащий методы и свойства(атрибуты) доски, у нее есть площадь в виде двумерного массива, список фигур, очередь игрока в булевом формате, и длина\ширина
class Board:

    def __init__(self):
        self.board = [['-'] * 8] * 8
        self.figures = list()
        self.player_queue = True
        self.width = 8
        self.height = 8

# Добавление шашек в доску, по 12 на игрока
    def add_checkers(self):
        for i in range(3):
            for j in range(self.width):
                if (i % 2 == 0 and j % 2 == 0) or (i % 2 != 0 and j % 2 != 0):
                    self.figures.append(figure.Checkers([j, i], True, "Checkers"))

        for i in range(5, 8):
            for j in range(self.width):
                if (i % 2 == 0 and j % 2 == 0) or (i % 2 != 0 and j % 2 != 0):
                    self.figures.append(figure.Checkers([j, i], False, "Checkers"))

# Отрисовка доски
    def draw_board(self):
        for i in range(self.height):
            for j in range(self.width):
                self.board[i][j] = '-'

# отрисовка фигур на доске, у каждого игрока свой цвет, дамки также имеют другой цвет
    def print_board(self):
        print("y\\x ", end='')
        for i in range(self.height):
            print(str(i+1) + "  ", end='')
        print("\n")

        for i in range(self.height):
            print("\033[37m{}".format(str(i + 1) + "\t"), end='')

            for j in range(self.width):
                finded_figure = Board.find_figure(self, j, i)

                if finded_figure is not None:
                    if finded_figure.playerControl == True:
                        if finded_figure.type == "Queen":
                            print("\033[34m{}" .format("1  "), end='')
                        else:
                            print("\033[32m{}" .format("1  "), end='')
                    elif finded_figure.type == "Queen":
                        print("\033[33m{}" .format("2  "), end='')
                    else:
                        print("\033[31m{}" .format("2  "), end='')
                else:
                    print("\033[37m{}".format(self.board[i][j] + "  "), end='')
                finding_figure = None
            print('\n')

# метод переключающий очередь игрока
    def switch_queue(self):
        if self.player_queue == True:
            self.player_queue = False
        else:
            self.player_queue = True

# поиск фигуры по координатам
    def find_figure(self, x, y):

        for figure in self.figures:
            if figure.location[0] == x and figure.location[1] == y:
                return figure

        return None

# Вывод на экран очереди игрока
    def print_player(self):
        if self.player_queue == True:
            print("\033[37m{}".format("Ход игрока 1"))
        else:
            print("\033[37m{}".format("Ход игрока 2"))

# Метод, позволяющий игроку делать ходы
    # Изначально игрок, вводит координаты доски через запятую, эти координаты преобразуются в массив.
    # После чего происходит серия проверок. Сначала идет проверка, нашлась ли фигура и принадлежит ли она ходящему игроку.
    # Далее, идет поиск вражеской фигуры,которую можно съесть
    # Если фигура нашлась, то идет цикл while с таким же поиском. Это необходимо если игрок может съесть 2 и более фигуры
    # Вводится координаты вражеской фигуры после чего происходит серия проверок на корректность введенных координат
    # Если все корректно то фигура съедается,а шашка перемещается за нее, а если фигура была съедена дамкой, то игрок вводит координаты куда нужно переместить дамку
    def player_move(self, player_queue):
        Board.print_player(self)

        print("\033[37m{}".format("Введите координаты шашки через запятую"))

        checkers_coordinate = input().split(',')
        finded_figure = Board.find_figure(self, int(checkers_coordinate[0]) - 1, int(checkers_coordinate[1]) - 1)

        if finded_figure is not None and finded_figure.playerControl == player_queue:
            if self.find_enemy(finded_figure.location[0],finded_figure.location[1],finded_figure) == True:
                while self.find_enemy(finded_figure.location[0],finded_figure.location[1],finded_figure) == True:
                    print("\033[37m{}".format("Введите координаты противника которого вы хотите сьесть через запятую"))
                    enemy_coordinates = input().split(',')
                    finded_enemy = self.find_figure(int(enemy_coordinates[0]) - 1, int(enemy_coordinates[1]) - 1)

                    if finded_enemy is not None:
                        enemy_x = finded_figure.location[0] - finded_enemy.location[0]
                        enemy_y = finded_figure.location[1] - finded_enemy.location[1]

                        if self.destroy_enemy(finded_enemy, finded_figure):
                            if finded_figure.type == "Checkers":
                                finded_figure.move_to(finded_figure.location[0] - (enemy_x * 2), finded_figure.location[1] - (enemy_y * 2))
                            else:
                                print("\033[37m{}".format("Введите координаты для перемещения через запятую"))
                                queen_coordinates = input().split(',')
                                finded_figure.move_to(int(queen_coordinates[0]) - 1, int(queen_coordinates[1]) - 1)
                    else:
                        print("\033[37m{}".format("Фигура не найдена"))
            else:
                print("\033[37m{}".format("Введите координаты для перемещения через запятую"))
                checkers_coordinate = input().split(',')

                x = int(checkers_coordinate[0]) - 1
                y = int(checkers_coordinate[1]) - 1

                if self.check_move(x,y,finded_figure) == True:
                    finded_figure.move_to(x,y)
                else:
                    self.player_move(player_queue)
            self.switch_queue()

# метод на нахождение вражеской фигуры, которую можно съесть, шашка проверяет по две соседние клатки с каждой стороны и возращает true\false.
    # для дамки происходит тоже самое, только в цикле while, потому что дамка может обнажурить фигуру вплоть на другом конце доски
    def find_enemy(self, x, y, selected_figure):
        if selected_figure.type == "Checkers":
            if (Board.find_figure(self,x-1,y-1) is not None and Board.find_figure(self,x-2,y-2) is None and Board.find_figure(self,x-1,y-1).playerControl != selected_figure.playerControl
                    and Board.find_figure(self,x-1,y-1).location[0] != 0 and Board.find_figure(self,x-1,y-1).location[1] != 0 or

                    Board.find_figure(self, x - 1, y + 1) is not None and Board.find_figure(self, x - 2,y + 2) is None and Board.find_figure(self, x - 1, y + 1).playerControl != selected_figure.playerControl
                    and Board.find_figure(self, x - 1, y + 1).location[0] != 0 and Board.find_figure(self, x - 1, y + 1).location[1] != (self.height - 1) or

                    Board.find_figure(self, x + 1, y - 1) is not None and Board.find_figure(self, x + 2,y - 2) is None and Board.find_figure(self, x + 1, y - 1).playerControl != selected_figure.playerControl
                    and Board.find_figure(self, x + 1, y - 1).location[0] != (self.width - 1) and Board.find_figure(self, x + 1, y - 1).location[1] != 0 or

                    Board.find_figure(self, x + 1, y + 1) is not None and Board.find_figure(self, x + 2,y + 2) is None and Board.find_figure(self, x + 1, y + 1).playerControl != selected_figure.playerControl
                    and Board.find_figure(self, x + 1, y + 1).location[0] != (self.width - 1) and Board.find_figure(self, x + 1, y + 1).location[1] != (self.height - 1)
                ): return True
        elif selected_figure.type == "Queen":
            X = selected_figure.location[0]
            Y = selected_figure.location[1]
            while X > 0 and Y > 0:
                if (Board.find_figure(self,X - 1, Y - 1) is not None and Board.find_figure(self,X - 2, Y - 2) is not None): break
                if (Board.find_figure(self, X - 1, Y - 1) is not None and Board.find_figure(self, X - 2, Y - 2) is None and Board.find_figure(self, X,Y) is None and Board.find_figure(self, X - 1, Y - 1).playerControl != selected_figure.playerControl
                        and Board.find_figure(self, X - 1, Y - 1).location[0] != 0 and Board.find_figure(self, X - 1, Y - 1).location[1] != 0):
                    return True
                else:
                    X -= 1
                    Y -= 1

            X = selected_figure.location[0]
            Y = selected_figure.location[1]
            while X < self.width - 1 and Y > 0:
                if (Board.find_figure(self,X + 1, Y - 1) is not None and Board.find_figure(self,X + 2, Y - 2) is not None): break
                if (Board.find_figure(self, X + 1, Y - 1) is not None and Board.find_figure(self, X + 2,Y - 2) is None and Board.find_figure(self, X,Y) is None and Board.find_figure(self, X + 1, Y - 1).playerControl != selected_figure.playerControl
                        and Board.find_figure(self, X + 1, Y - 1).location[0] != (self.width - 1) and Board.find_figure(self, X + 1, Y - 1).location[1] != 0):
                    return True
                else:
                    X += 1,
                    Y -= 1
            X = selected_figure.location[0]
            Y = selected_figure.location[1]
            while X > 0 and Y < self.width - 1:
                if (Board.find_figure(self,X - 1, Y + 1) is not None and Board.find_figure(self,X - 2, Y + 2) is not None): break
                if (Board.find_figure(self, X - 1, Y + 1) is not None and Board.find_figure(self, X - 2,Y + 2) is None and Board.find_figure(self, X,Y) is None and Board.find_figure(self, X - 1, Y + 1).playerControl != selected_figure.playerControl
                        and Board.find_figure(self, X - 1, Y + 1).location[0] != 0 and Board.find_figure(self, X - 1, Y + 1).location[1] != (self.height - 1)):
                    return True
                else:
                    X -= 1
                    Y += 1
            X = selected_figure.location[0]
            Y = selected_figure.location[1]
            while X < self.width - 1 and Y < self.height - 1:
                if (Board.find_figure(self,X + 1, Y + 1) is not None and Board.find_figure(self,X + 2, Y + 2) is not None): break
                if (Board.find_figure(self, X + 1, Y + 1) is not None and Board.find_figure(self, X + 2,Y + 2) is None and Board.find_figure(self, X,Y) is None and Board.find_figure(self, X + 1, Y + 1).playerControl != selected_figure.playerControl
                        and Board.find_figure(self, X + 1, Y + 1).location[0] != (self.width - 1) and Board.find_figure(self, X + 1, Y + 1).location[1] != (self.height - 1)):
                    return True
                else:
                    X += 1
                    Y += 1
        return False

#метод уничтожающий вражескую фигуру. Сначала проверяется корректность введенных фигур,а затем шашка удаляется из списка
    def destroy_enemy(self, enemy, hero):
        if ((hero.location[0] == enemy.location[0] and hero.location[1] == enemy.location[1]) or hero.playerControl == enemy.playerControl or
                (abs(hero.location[0] - enemy.location[0] > 1) or abs(hero.location[1] - enemy.location[1] > 1)) and hero.type == "Checkers"):
            print("Не корректные координаты вражеской фигуры")
            return False
        else:
            self.figures.remove(enemy)
            return True
#метод проверяющий на корректность введенных координат,это необходимо, чтобы игрок не мог передвигать свой шашки\дамки как ему угодно
    def check_move (self, x, y, selected_figure):
        if (x + y) % 2 != 0 or selected_figure.location[0] == x or selected_figure.location[1] == y:
            print("Некорректный ход")
            return False

        if self.find_figure(x, y) is not None:
            print("Эту фигуру нельзя съесть")
            return False

        if selected_figure.type == "Checkers":
            if (abs(selected_figure.location[0] - x) > 1 or abs(selected_figure.location[1] - y) > 1 and (selected_figure.location[0] == x and selected_figure.location[1] == y)):
                print("Не корректный ход")
                return False
            elif (selected_figure.playerControl == True and y < selected_figure.location[1] or selected_figure.playerControl == False and selected_figure.location[1] < y):
                print("Назад ходить нельзя")
                return False
        return True
