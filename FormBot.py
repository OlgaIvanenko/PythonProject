from tkinter import Frame, Button, Label, Toplevel, Tk
from PIL import Image, ImageTk
import ReversiBot

sizeBall = 50
mapCell = 8
sizeMap = sizeBall * mapCell  # 50 * 8 = 400


class Pic:
    Cell = [[[], []], [[], []], [[], []], [[], []]]
    Field = []
    someCell = [] # картинка кто сейчас ходит
    black = 0
    white = 1
    Dark = 1
    Light = 0
    newblack = 2
    newwhite = 3

    def __init__(self):
        img = Image.open("pictures/bets.png")
        oldsize = 100
        size = (sizeBall, sizeBall)
        for i in range(0, 20):
            self.Cell[self.black][self.Dark].append(
                img.crop((i * oldsize, 0, i * oldsize + oldsize, oldsize)))
            self.Cell[self.black][self.Dark][i].thumbnail(size)
            self.Cell[self.black][self.Light].append(
                img.crop((i * oldsize, oldsize, i * oldsize + oldsize, 2 * oldsize)))
            self.Cell[self.black][self.Light][i].thumbnail(size)
            self.Cell[self.white][self.Dark].append(
                img.crop((i * oldsize, 2 * oldsize, i * oldsize + oldsize, 3 * oldsize)))
            self.Cell[self.white][self.Dark][i].thumbnail(size)
            self.Cell[self.white][self.Light].append(
                img.crop((i * oldsize, 3 * oldsize, i * oldsize + oldsize, 4 * oldsize)))
            self.Cell[self.white][self.Light][i].thumbnail(size)

            self.Cell[self.newblack][self.Dark].append(
                img.crop((i * oldsize, 4 * oldsize, i * oldsize + oldsize, 5 * oldsize)))
            self.Cell[self.newblack][self.Dark][i].thumbnail(size)
            self.Cell[self.newblack][self.Light].append(
                img.crop((i * oldsize, 5 * oldsize, i * oldsize + oldsize, 6 * oldsize)))
            self.Cell[self.newblack][self.Light][i].thumbnail(size)
            self.Cell[self.newwhite][self.Dark].append(
                img.crop((i * oldsize, 6 * oldsize, i * oldsize + oldsize, 7 * oldsize)))
            self.Cell[self.newwhite][self.Dark][i].thumbnail(size)
            self.Cell[self.newwhite][self.Light].append(
                img.crop((i * oldsize, 7 * oldsize, i * oldsize + oldsize, 8 * oldsize)))
            self.Cell[self.newwhite][self.Light][i].thumbnail(size)

        self.Field.append(self.Cell[2][0][0].copy())
        self.Field.append(self.Cell[2][1][0].copy())
        self.someCell.append(self.Cell[1][0][0].copy())
        self.someCell.append(self.Cell[0][0][0].copy())

# функция, которая отвечает за клик. Переменная Step не дает пользователю кликать, если идет процесс отрисовки.
def Click_field(event):
    if not app.Step:
        # если пользователь нажал на ячейку (и в нее можно походить), то вызывается функция Click() и пользователь ходить больше не может.
        if app.Game.Fmap[int(event.y / sizeBall)][int(event.x / sizeBall)] > 0:
            app.Game.Click(int(event.y / sizeBall), int(event.x / sizeBall))
            app.Step = True
            app.timer_Tick(0)
    # затем вызывается timer_Tick(0), который отвечает за отрисовку изменения картинки фишки в ячейке.

def new_game_bot():
    app.init_main()
    app.Bot = True
    pass

def new_game():
    app.init_main()
    app.Bot = False
    pass

# вся логика
class Main(Frame):
    Game = None
    p = Pic()
    Step = False
    Bot = True

    # при ходе меняет картинку текущего игрока
    def SetStep(self):
        img = self.p.Cell[self.Game.actionPlayer + 1][0][19].copy()
        img.thumbnail((30, 30))
        render = ImageTk.PhotoImage(img)
        self.step.configure(image=render)
        self.step.image = render

    # при ходе меняет счет
    def SetScore(self):
        score = self.Game.Score()
        self.Score.config(text='Белые: ' + str(score[0]) + ' кл.\nЧерные: ' + str(score[1]) + ' кл.')
        pass

    # функция инициализации при запуске игры
    def init_main(self):
        # кнопка новой игры с ботом
        btn_new_game_bot = Button(text='Играть с ботом', command=new_game_bot, bg='#d7d8c0', bd=2, width='13')
        btn_new_game_bot.place(x=10, y=7)
        # кнопка новой игры один на один
        btn_new_game = Button(text='Играть вдвоём', command=new_game, bg='#d7d8c0', bd=2, width='13')
        btn_new_game.place(x=119, y=7)

        self.map = []  # вспомогательный массив-копия поля для отрисовки. Нужен для того, чтобы запоминать вид поля до шага.
        # При вызове функции Paint(), которая отвечает за отрисовку только изменившихся клеток, сравнивается поле до хода и после хода
        # если что-то изменималось, то меняются только изменившиеся клетки.

        self.Game = ReversiBot.Field()  # создается объект игры(логики)

        # картинка с полем
        self.img = Image.open('pictures/field.jpg')
        self.img.thumbnail((sizeMap, sizeMap))
        self.render = ImageTk.PhotoImage(self.img)
        self.field = Label(window, image=self.render)
        self.field.place(x=8, y=38)
        self.field.image = self.render
        self.field.bind('<Button-1>', Click_field)

        # Метка со Счетом игры
        self.Score = Label(justify='right')
        self.Score.place(x=225, y=3)
        self.SetScore()

        # Метка "Ходит:"
        label = Label(justify='left', text='Ходит:')
        label.place(x=335, y=9)

        # картика с шариком цвета игрока, который ходит
        cell = self.p.Cell[0][0][0].copy()
        cell.thumbnail((30, 30))
        render = ImageTk.PhotoImage(cell)
        self.step = Label(window, image=render)
        self.step.place(x=378, y=3)
        self.step.image = render

        # наполним вспомогательный массив-клон поля
        for y in range(0, self.Game.max):
            self.map.append([])
            for x in range(0, self.Game.max):
                self.map[y].append(None)
        self.Paint(19)
        self.cloneMap()
        self.Step = False

    def cloneMap(self):
        for y in range(0, self.Game.max):
            for x in range(0, self.Game.max):
                self.map[y][x] = self.Game.Map[y][x].player

    def timer_Tick(self, i):
        # через каждые 30 милисекунд будет обновляться картинка в ячейке. Вызывается функция Paint()
        if i == 0:
            self.SetStep()
            self.SetScore()
        if i < 20:
            self.Paint(i)
            self.after(30, self.timer_Tick, i + 1)

        else:
            self.cloneMap()
            if not self.Game.IsStep():
                create_window_end_game()
            else:
                if self.Bot:
                    if self.Game.actionPlayer == 1:  # or self.Game.actionPlayer == 1:  # два бота играют сам с собой
                        self.Game.BotStep()
                        app.SetScore()
                        self.after(300, self.timer_Tick, 0)
                    else:
                        self.Step = False
                else:
                    self.Step = False

    # Функция, которая отвечает за отрисовку только тех фишек, которые изменились. Она определяет изменившиеся ячейчки и выывает фукнцию Draw()
    def Paint(self, i):
        for y in range(0, self.Game.max):
            for x in range(0, self.Game.max):
                if self.Game.Map[x][y].player != self.map[x][y]:
                    player = self.Game.Map[x][y].player
                    if self.map[x][y] == 0:
                        player += 2
                    bgcolor = 0 if (x + y) % 2 == 0 else 1
                    self.Draw(y, x, player, bgcolor, i)


    def Draw(self, x, y, player, bgcolor, i):
        if player == 0:
            self.img.paste(self.p.Field[bgcolor], (x * sizeBall, y * sizeBall))
        else:
            self.img.paste(self.p.Cell[player - 1][bgcolor][i], (x * sizeBall, y * sizeBall))
        self.render = ImageTk.PhotoImage(self.img)
        self.field.configure(image=self.render)
        self.field.image = self.render


def create_window_end_game():
    end = Toplevel(window)
    end.title("Вы закончили игру")
    end.geometry("300x120")
    end.resizable(False, False)
    new_game_bot = Button(end, text='OK', command=end.destroy, bg='#d7d8c0', bd=2, width='17')
    new_game_bot.place(x=80, y=80)
    label = Label(end, text='', font='15')
    label.place(x=30, y=15)
    score = app.Game.Score()
    text = 'Счёт: ' + str(score[0]) + ' белых и ' + str(score[1]) + ' черных'
    if score[0] == score[1]:
        label.config(text='Ничья!\n' + text)
    elif score[0] > score[1]:
        label.config(text='Черные победили!\n' + text)
    else:
        label.config(text='Черные проиграли!\n' + text)

#Запуск программы
if __name__ == "__main__":
    window = Tk()
    app = Main(window) # экземпляр класса Main. Через него могу обращаться к него функциям и переменным.
    app.init_main()
    app.pack()
    window.title("Реверси")
    window.geometry("420x450")
    window.resizable(False, False)
    window.mainloop()
