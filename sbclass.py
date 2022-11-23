#импротируем ГСЧ, чтобы мог играть компьютер
import random
import time

#класс поле, здесь хранятся значения поля для игрока и для компьютера
class Field:
    def __init__(self):
        self.ships = [] #наши корабли
        self.ships_t = [] #наши выстрелы все
        self.ships_dr = [] #корабли, в которые противник попал

    #распечатка поля
    def get_field(self,ships_dr = [], opp_ships_t = [],ships = []):
        self.ships_dr_tmp = ships_dr
        self.ships_tmp = ships
        self.opp_ships_t = opp_ships_t
        for i in range(7):
            print(' | ', end='')
            for j in range(7):
                if (i, j) in self.ships_tmp and (i, j) not in self.ships_dr_tmp:
                    print('■ ',end='| ')
                elif (i, j) in self.ships_dr_tmp:
                    print('X ',end='| ')
                elif (i, j) in self.opp_ships_t and (i, j) not in self.ships_dr_tmp:
                    print('T ',end='| ')
                elif i == j == 0:
                    print('  ', end='| ')
                elif i == 0 and 0 < j < 7:
                    print(f'{j} ',end='| ')
                elif 0 < i < 7 and j == 0:
                    print(f'{i} ',end='| ')
                else:
                    print('O ',end='| ')
            print()
    #сортировка списков с координатами кораблей (нужна для проверки на победу)
    def set_sort(self):
        self.ships.sort()
        self.ships_t.sort()
        self.ships_dr.sort()
    #методы получения списков с координатами
    def get_ships(self):
        return self.ships

    def get_ships_t(self):
        return self.ships_t

    def get_ships_dr(self):
        return self.ships_dr
    #добавление значение в списки по ходу игры
    def set_ships(self,c_ship):
        self.ships.extend(c_ship)

    def set_ships_t(self,c_ship):
        self.ships_t.append(c_ship)

    def set_ships_dr(self,c_ship):
        self.ships_dr.append(c_ship)
    #очистка списка кораблей (используется при генерации поля кораблей ИИ)
    def set_ships_clear(self):
        self.ships.clear()

#в классе корабль хранятся данные о конкретном корабле на игровом поле
#координаты хранятся в виде списка кортежей
#длина соответствует количеству палуб корабля (однопалубный, двухпалубный, трехпалубный)
#за точку отсчета берется координата левого верхнего поля, направления доступны вниз и право
#наверное надо было как-то иначе использовать корабль, чтобы было больше объектно ориентированного подхода
#но как уж селал
#буду дорабатывать
class Ship:
    def __init__(self,len,orient,coord = ()):
        self.coord = coord
        self.len = len
        self.orient = orient
    #метод рассчитывает координаты корабля на доске
    def get_coord(self):
        self.tmp_l = []
        if self.len > 1:
            for self.i in range(self.len):
                if self.orient in ['Право', 'право']:
                    self.tmp_l.append((self.coord[0],self.coord[1] + self.len - 1 - self.i))
                elif self.orient in ['Вниз', 'вниз']:
                    self.tmp_l.append(((self.coord[0] + self.len - 1 - self.i,self.coord[1])))
            return self.tmp_l
        else:
            self.tmp_l.append(self.coord)
            return self.tmp_l


#далее блок функций
#проверка возможности установки корабля в данную позицию
def check_coord_ship(n_len,n_orient, n_coord = (),n_ships = ()):
    if n_coord in n_ships:
        return False
    else:
        if ((n_orient == 'право') and (n_coord[1] + n_len - 1) <= 6):
            for i in range(3):
                for j in range(n_len + 2):
                    if ((n_coord[0] - 1 + i, n_coord[1] - 1 + j) in n_ships):
                        return False
        if ((n_orient == 'вниз') and (n_coord[0] + n_len - 1) <= 6):
            for i in range(3):
                for j in range(n_len + 2):
                    if ((n_coord[0] - 1 + j, n_coord[1] - 1 + i) in n_ships):
                        return False
        return True


#начало игры и расстановка кораблей на игровом поле
def start_game(user_f,pc_f,list_of_user_ships):
    print('Здравствуйте! Мы рады приветствовать Вас в игре "Морской бой"!')
    print('Надеемся, что Вам понравится!')
    print('-'*32)
    print('На поле игрока находятся Ваши корабли. Расставляйте суда грамотно.')
    count_ships_input = [4,2,1,0] #счетчики количества усановленных кораблей, а так же счетчик количества ходов

    while count_ships_input[3] <= 6:
        print('-' * 32)
        print('Поле игрока!!!')
        print('-' * 32)
        user_f.get_field(user_f.get_ships_dr(),pc_f.get_ships_t(),user_f.get_ships())
        print('-' * 32)

        #далее ввод данных с проверками на правильность ввода
        while True:
            try:
                if count_ships_input[1] > 0 or count_ships_input[2] > 0:
                    n_len = int(input('Корабль с каким количеством палуб вы хотите разместить? '
                                      '(введите число от 1 до 3 и нажмите Enter):'))
                else:
                    n_len = 1
            except Exception:
                print('Ввод не правильный! Повторите ввод!')
                continue

            #проверка возможности создания ещё одного такого же корабля
            if 1 <= n_len <= 3 and count_ships_input[n_len-1] != 0:
                break
            else:
                print('Ввод не правильный! Повторите ввод!')
                continue

        while True:
            try:
                if (count_ships_input[1] > 0 or count_ships_input[2] > 0) and n_len > 1 :
                    orient = input('Введите направление, в котором будет строиться корабль.'
                               'Введите нужный вариан с клавиатуры и нажите Enter (возможны значени вниз и право): ')
                else:
                    orient = 'вниз'
            except Exception:
                print('Ввод не правильный! Повторите ввод!')
                continue

            if orient in ['Право', 'право', 'Вниз', 'вниз']:
                break
            else:
                print('Ввод не правильный! Повторите ввод!')
                continue
        while True:
            try:
                coord = tuple(map(int, input('Введите координаты верхнего левого края '
                                'корабля через запятую, напрмер 1,1 и нажмите Enter: ').split(',')))
                if check_coord_ship(n_len, orient, coord, user_f.get_ships()) and len(coord) == 2:
                    list_of_user_ships.append(Ship(n_len, orient, coord))
                    user_f.set_ships(list_of_user_ships[-1].get_coord())
                    count_ships_input[n_len - 1] -= 1
                    break
                else:
                    print(
                        'В данном месте уже есть корабль или расстояние до другого корабля ближе одной клетки! \nПовторите ввод!')
                    continue
            except Exception:
                print('Ввод не правильный! Повторите ввод!')
                continue

        count_ships_input[3] += 1



#генерация кораблей компьютером
def pc_gen(user_f,pc_f,list_of_pc_ships):
    ch = (1,2,3,4,5,6)
    n = 7
    check_steps = 0 #счетчик попыток генерации
    while n != 0:
        if n == 7:
            pc_len = 3
        elif n in [6,5]:
            pc_len = 2
        else:
            pc_len = 1

        pc_orient = random.choice(['право','вниз'])

        if pc_orient == 'право':
            pc_coord = (random.choice(ch),random.choice(ch[0:7 - pc_len]))

        if pc_orient == 'вниз':
            pc_coord = (random.choice(ch[0:7-pc_len]),random.choice(ch))

        if check_coord_ship(pc_len, pc_orient, pc_coord,pc_f.get_ships()):
            list_of_pc_ships.append(Ship(pc_len, pc_orient, pc_coord))
            pc_f.set_ships(list_of_pc_ships[-1].get_coord())
        else:
            n += 1
        n -= 1

        check_steps += 1

        if check_steps >= 100: #если попытки генерации закончились, то пробовать снова сначала
            n = 7
            check_steps = 0
            pc_f.set_ships_clear() #очистка списка координат кораблей для повторной попытки


#ход игрока
def user_shot(user_f,pc_f,list_of_pc_ships):
    while True:
        try:
            u_shot = tuple(map(int, input('Куда Вы хотите произвести выстрел? '
                                      '(введите координаты через запятую, например 1,1): ').split(',')))
            if (u_shot not in user_f.get_ships_t()) and \
                    1 <= u_shot[0] <= 6 and 1 <= u_shot[1] <= 6 and len(u_shot) == 2:
                user_f.set_ships_t(u_shot)
                if u_shot in pc_f.get_ships():
                    pc_f.set_ships_dr(u_shot)
                    print_game_info(user_f, pc_f)
                    print('Ура! Вы попали! У вас ещё один ход!')
                    print(check_ship_life(list_of_pc_ships, pc_f, u_shot))
                    print('-' * 32)
                    if check_win(user_f, pc_f):
                        return True
                    continue
                else:
                    print_game_info(user_f,pc_f)
                    print('Ход игрока!')
                    print('Мимо!')
                    print('-' * 32)
                    time.sleep(3)
                    break
            else:
                print('Ошибка ввода или в это поле вы уже стреляли! Посторите ввод!')
        except Exception:
            print('Не верный ввод! Повторите ввод!')
            continue


#ход ИИ (компьютер стреляет рандомом)
def pc_shot(user_f,pc_f,list_of_user_ships):
    while True:
        ch = (1,2,3,4,5,6)
        p_shot = (random.choice(ch),random.choice(ch))
        if (p_shot not in pc_f.get_ships_t()):
            pc_f.set_ships_t(p_shot)
            if p_shot in user_f.get_ships():
                user_f.set_ships_dr(p_shot)
                print_game_info(user_f,pc_f)
                print('Ура! Компьютер попал!!! Ещё один ход компьютера!')
                print(check_ship_life(list_of_user_ships,user_f,p_shot))
                print('-' * 32)
                time.sleep(3)
                if check_win(user_f, pc_f):
                    return True
                continue
            else:
                print_game_info(user_f,pc_f)
                print('Ход компьютера!')
                print('Мимо!')
                print('-' * 32)
                time.sleep(3)
                break

#проверка на победу
def check_win(user_f,pc_f):
    n = None
    user_f.set_sort()
    pc_f.set_sort()
    if user_f.get_ships() == user_f.get_ships_dr():
        print('-'*32)
        print('ИИ победил!!! УРА!!!')
        print('-' * 32)
        n = True
    elif pc_f.get_ships() == pc_f.get_ships_dr():
        print('-' * 32)
        print('Поздравляем!!! Вы победили!!!')
        print('-' * 32)
        n = True
    else:
        return False
    return n

#проверка жив ли ещё корабль
def check_ship_life(list_of_ships,field,shot):
    for ship in list_of_ships:
        tmp_l = ship.get_coord()
        if shot in tmp_l:
            for i in tmp_l:
                if i not in field.get_ships_dr():
                    return 'Корабль ранен!'
            return 'Корабль убит! Поздравляем!'

#печать полей в игре
def print_game_info(user_f,pc_f):
    print('-' * 32)
    pc_f.get_field(pc_f.get_ships_dr(), user_f.get_ships_t(), [])
    print('Поле ИИ! Здесь вы видите информацию о том, попадаете ли вы в корабли противника. '
          '\nХ - попадание. T - промах')
    print('-' * 32)
    user_f.get_field(user_f.get_ships_dr(), pc_f.get_ships_t(), user_f.get_ships())
    print('Поле игрока! Здвеь вы видите свои корабли и попадания противника! ')
    print('-' * 32)



