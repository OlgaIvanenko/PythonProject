class Cell:
    x = None
    y = None
    player = None  # отвечает за цвет фишки на поле

     # конструктор инициализации
    def __init__(self, x, y, player):
        self.x = x
        self.y = y
        self.player = player


class Field:
    max = 8
    actionPlayer = 2

    def __init__(self):
        self.Map = [] # контейнер, список с шариками. в Map записываются реальные перевернутые фишки, которые потом прорисовываются на экране
        # изначально Map, Fmap- одномерные массивы. В цикле 8 раз добавили в них пустой массив(список),
        # который выглядит [[],[],[],[],[],[],[],[],] и все еще пустой,
        # а потом в каждый из пустого списка добавили 8 ячеек

        # контейнер, вспомогательная невидимая карта, которая хранит в себе значения просчитаннных ходов.
        # Есть поле, есть точки, куда можно походить и куда нельзя. Чтобы посчитать такие точки, надо
        # оббежать все клетки и посмотреть можно ли походить текущему игроку или нет. В ячейку ставится число
        # которое равно количеству фишек противника, которые можно перевернуть.
        self.Fmap = []
        # размещение пустых ячеек в контейнерах (изначально все пусто)
        for y in range(0, int(self.max)):
            self.Map.append([])
            self.Fmap.append([])
            for x in range(0, int(self.max)):
                self.Map[y].append(Cell(y, x, 0))
                self.Fmap[y].append(0) # добавляем везде 0

        self.Map[3][3] = Cell(3, 3, 2)
        self.Map[4][3] = Cell(4, 3, 1)
        self.Map[3][4] = Cell(3, 4, 1)
        self.Map[4][4] = Cell(4, 4, 2)
        self.FindStep(self.actionPlayer)

    # функции FindStep() CheckStep() работают вместе - они ищут фишки противника, которые можно перевернуть. Циклом прохожу по всем ячейкам,
    # нахожу ячейки текущего игрока и во все стороны от него проверяю фишки противника.
    # Если за фишкой или фишками противника пустое пусто место, то в Фмап заношу то количество фишек противника,
    # которые цикл встретил на своем пути.
    def FindStep(self, player):
        for y in range(0, int(self.max)):
            for x in range(0, int(self.max)):
                self.Fmap[y][x] = 0
        for y in range(0, int(self.max)):
            for x in range(0, int(self.max)):
                if self.Map[y][x].player == player:
                    self.CheckStep(y, x, 0, -1, player, 1)
                    self.CheckStep(y, x, 1, -1, player, 1)
                    self.CheckStep(y, x, 1, 0, player, 1)
                    self.CheckStep(y, x, 1, 1, player, 1)
                    self.CheckStep(y, x, 0, 1, player, 1)
                    self.CheckStep(y, x, -1, 1, player, 1)
                    self.CheckStep(y, x, -1, 0, player, 1)
                    self.CheckStep(y, x, -1, -1, player, 1)


    # передаются координаты текущей ячейки, а потом проверяется во всех направлениях
    def CheckStep(self, y, x, py, px, player, k):
        xj = x + k * px
        yi = y + k * py
        if yi < 0 or yi >= self.max or xj < 0 or xj >= self.max: # не должно выходить за рамки
            return
        if self.Map[yi][xj].player != 0 and self.Map[yi][xj].player != player: # если след ячейка не пустая и равна цвету противника, то след шаг
            self.CheckStep(y, x, py, px, player, k + 1)
        if self.Map[yi][xj].player == 0 and k >= 2: # если ячейка пустая и шагов больше 2, то в Фмап записывается колво ячеек, кот
            self.Fmap[yi][xj] += k - 1      # можно перевернуть


    # AllStep() и Step() работают вместе и отвечают за то, чтобы текущий игрок мог забрать себе фишки противника.
    # AllStep() вызывает функцию Step(), которая от кликнутой ячейки проверяет во всех направлениях фишки, которые можно перевернуть
    def AllStep(self, y, x, player):
        self.Step(y, x, 0, -1, player, 1)
        self.Step(y, x, 1, -1, player, 1)
        self.Step(y, x, 1, 0, player, 1)
        self.Step(y, x, 1, 1, player, 1)
        self.Step(y, x, 0, 1, player, 1)
        self.Step(y, x, -1, 1, player, 1)
        self.Step(y, x, -1, 0, player, 1)
        self.Step(y, x, -1, -1, player, 1)

    def Step(self, y, x, py, px, player, k):
        yi = y + k * py
        xj = x + k * px
        if yi < 0 or yi >= self.max or xj < 0 or xj >= self.max:
            return
        if self.Map[yi][xj].player != 0 and self.Map[yi][xj].player != player:
            self.Step(y, x, py, px, player, k + 1)
        if self.Map[yi][xj].player == player:
            for a in range(1, k):
                yi = y + a * py
                xj = x + a * px
                self.Map[yi][xj].player = player

    def ChangePlayer(self):
        self.actionPlayer = (1 - (self.actionPlayer - 1)) + 1
        self.FindStep(self.actionPlayer)

    # функция чтобы пользователь мог походить. Пользователь кликает на какую-то ячейку и проверяется пустая ли эта клетка.
    # В клетку клика заносится цвет текущего игрока, а затем срабаотывает функция AllStep(). Затем меняется игрок и проверяется
    # есть ли доступные ходы
    def Click(self, y, x):
        print('Клик по [' + str(y) + ', ' + str(x) + '], фишек =', self.Fmap[y][x])
        if self.Fmap[y][x] > 0:
            self.Map[y][x].player = self.actionPlayer
            self.AllStep(y, x, self.actionPlayer)
            self.ChangePlayer()
            if not self.IsStep():
                self.ChangePlayer()

    def IsStep(self):
        for y in range(0, int(self.max)):
            for x in range(0, int(self.max)):
                if self.Fmap[y][x] > 0:
                    return True
        return False

    # Бот, суть которого заключается в поиске ячейки, откуда можно забрать максимальное количетсво фишек.
    # Поскольку самый выигрышный вариант это кликать по углам, то есть 4 проверки на то, чтобы походить туда.
    # Если бот не может походить в угол, то он может проверить на возможность хода по крайним ячейкам по бокам или в внутри поля.
    # Бот вызывается в FormBot.py
    def BotStep(self):
        max = xmax = ymax = 0
        if self.Fmap[0][0] > 0: self.Click(0, 0); return
        if self.Fmap[self.max - 1][0] > 0: self.Click(self.max - 1, 0); return
        if self.Fmap[0][self.max - 1] > 0: self.Click(0, self.max - 1); return
        if self.Fmap[self.max - 1][self.max - 1] > 0: self.Click(self.max - 1, self.max - 1); return
        for y in range(0, int(self.max)):
            for x in range(0, int(self.max)):
                if x == 0 or y == 0 or x == self.max - 1 or y == self.max - 1:
                    if self.Fmap[y][x] > 0:
                        self.Click(y, x)
                        return
                if self.Fmap[y][x] > max:
                    max = self.Fmap[y][x]
                    ymax = y
                    xmax = x
        if max > 0:
            self.Click(ymax, xmax)

    def Score(self):
        score = [0, 0]
        for y in range(0, int(self.max)):
            for x in range(0, int(self.max)):
                if self.Map[y][x].player == 1:
                    score[0] += 1
                if self.Map[y][x].player == 2:
                    score[1] += 1
        return score
