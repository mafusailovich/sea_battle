#все функции и классы находятся в отдельном файле
from sbclass import Ship,Field, start_game, check_win,check_coord_ship,pc_shot,pc_gen,user_shot,print_game_info

#создаем поля для кораблей ИИ и игрока
user_f = Field()
pc_f = Field()

#списки кораблей игрока и ИИ (в моей реализации почти бесполезны)
list_of_user_ships = []
list_of_pc_ships = []

#ход игры

#начинаем игру, расставляем корабли игрока и ИИ
while True:
    t = input('Хотите, чтобы программа автоматически расставила крабли на игровом поле? (Y/N): ')
    if t in ['Y','y','У','у']:
        pc_gen(pc_f,user_f,list_of_user_ships)
        break
    elif t in ['N','n','Н','н']:
        start_game(user_f,pc_f,list_of_user_ships)
        break
    else:
        print('Не верный ввод! Повторите ввод!')

pc_gen(user_f,pc_f,list_of_pc_ships)

#сама игра
while True:
    print_game_info(user_f,pc_f)

    #ход игрока
    if user_shot(user_f,pc_f,list_of_pc_ships):
        print('Игра окончена!')
        break

    #ход ИИ
    if pc_shot(user_f,pc_f,list_of_user_ships):
        print('Игра окончена!')
        break

