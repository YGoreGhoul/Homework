from Board import Board

#Создание игры, игровой доски и заполнение ее шашками
game_status = True
game_board = Board()
game_board.add_checkers()


while game_status:
    #Обновление доски и выод ее на экран
    game_board.draw_board()
    game_board.print_board()

    #поиск шашек игроков
    count_figure_player_one = 0
    count_figure_player_two = 0

    for figure in game_board.figures:
        if figure.playerControl == True:
            count_figure_player_one+=1
        else:
            count_figure_player_two+=1

    #Проверка на остаток шашек у игроков
    if count_figure_player_one == 0:
        print("Победил игрок 2")
        game_status = False
    elif count_figure_player_two == 0:
        print("Победил игрок 1")
        game_status = False
    else:
        #Ход игрока
        game_board.player_move(game_board.player_queue)