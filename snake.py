from tkinter import *
import time
import random

Game_Running = True
text = ""

game_width = 500
game_height = 500
snake_item = 20
snake_color1 = "red"
snake_color2 = "yellow"
speed_sneak = 0.15


virtual_game_x = game_width // snake_item
virtual_game_y = game_height // snake_item

snake_x = virtual_game_x // 2
snake_y = virtual_game_y // 2
snake_x_nav = 0
snake_y_nav = 0

snake_list = []
snake_size = 5
sneak_score = 0

present_color1 = "blue"
present_color2 = "black"
presents_list = []
presents_size = 25


def get_speed(s):
    global speed_sneak
    speed_sneak = s
def create_window():
    global canvas, tk, text
    tk = Tk()
    tk.title("Игра Змейка на Python")

    canvas = Canvas(tk, width=game_width, height=game_height, bd=0, highlightthickness=0)

    for i in range(presents_size):
        x = random.randrange(virtual_game_x)
        y = random.randrange(virtual_game_y)
        id1 = canvas.create_oval(x * snake_item, y * snake_item, x * snake_item + snake_item, y * snake_item + snake_item,
                                 fill=present_color2)
        id2 = canvas.create_oval(x * snake_item + 2, y * snake_item + 2, x * snake_item + snake_item - 2,
                                 y * snake_item + snake_item - 2, fill=present_color1)
        presents_list.append([x, y, id1, id2])

    canvas.bind_all("<KeyPress-Left>", snake_move)
    canvas.bind_all("<KeyPress-Right>", snake_move)
    canvas.bind_all("<KeyPress-Up>", snake_move)
    canvas.bind_all("<KeyPress-Down>", snake_move)

    canvas.pack()

    text = canvas.create_text(50, 50, text=sneak_score, font="Arial 20", fill="black")

# Прорисовка тела змейки
def snake_paint_item(canvas, x, y):
    global snake_list
    id1 = canvas.create_rectangle(x * snake_item, y * snake_item, x * snake_item + snake_item,
                                  y * snake_item + snake_item, fill=snake_color2)
    id2 = canvas.create_rectangle(x * snake_item + 2, y * snake_item + 2, x * snake_item + snake_item - 2,
                                  y * snake_item + snake_item - 2, fill=snake_color1)
    snake_list.append([x, y, id1, id2])


# Съедание яблока змейкой
def check_can_we_delete_snake_item():
    if len(snake_list) >= snake_size:
        temp_item = snake_list.pop(0)
        canvas.delete(temp_item[2])
        canvas.delete(temp_item[3])

# Проверка яблока
def check_if_we_found_present():
    global snake_size, sneak_score, text
    for i in range(len(presents_list)):
        if presents_list[i][0] == snake_x and presents_list[i][1] == snake_y:
            snake_size = snake_size + 1
            canvas.delete(presents_list[i][2])
            canvas.delete(presents_list[i][3])

# Движение змейки
def snake_move(event):
    global snake_x
    global snake_y
    global snake_x_nav
    global snake_y_nav

    if event.keysym == "Up":
        snake_x_nav = 0
        snake_y_nav = -1
        check_can_we_delete_snake_item()
    elif event.keysym == "Down":
        snake_x_nav = 0
        snake_y_nav = 1
        check_can_we_delete_snake_item()
    elif event.keysym == "Left":
        snake_x_nav = -1
        snake_y_nav = 0
        check_can_we_delete_snake_item()
    elif event.keysym == "Right":
        snake_x_nav = 1
        snake_y_nav = 0
        check_can_we_delete_snake_item()
    snake_x = snake_x + snake_x_nav
    snake_y = snake_y + snake_y_nav
    snake_paint_item(canvas, snake_x, snake_y)
    check_if_we_found_present()


# Выход из цикла
def game_over():
    global Game_Running
    Game_Running = False


# Выход за границы
def check_if_borders():
    if snake_x > virtual_game_x or snake_x < 0 or snake_y > virtual_game_y or snake_y < 0:
        canvas.create_text(game_width / 2, game_height / 2,
                           text="GAME OVER!",
                           font="Arial 20",
                           fill="#ff0000")
        game_over()

# Столкновение со своим телом
def check_we_touch_self(f_x, f_y):
    global Game_Running
    if not (snake_x_nav == 0 and snake_y_nav == 0):
        for i in range(len(snake_list)):
            if snake_list[i][0] == f_x and snake_list[i][1] == f_y:
                canvas.create_text(game_width / 2, game_height / 2,
                                   text="GAME OVER!",
                                   font="Arial 20",
                                   fill="#ff0000")
                Game_Running = False

# Добавление очков
def score():
    global snake_size, sneak_score, text
    for i in range(len(presents_list)):
        if presents_list[i][0] == snake_x and presents_list[i][1] == snake_y:
            sneak_score += 1
            canvas.delete(text)
            text = canvas.create_text(50, 50, text=sneak_score, font="Arial 20", fill="black")

def restart():
    global Game_Running, sneak_score, snake_x, snake_y, snake_x_nav, snake_y_nav, presents_list
    root.destroy()
    Game_Running = True
    sneak_score = 0
    snake_x = virtual_game_x // 2
    snake_y = virtual_game_y // 2
    snake_x_nav = 0
    snake_y_nav = 0
    presents_list = []
    main()

def start_main():
    root = Tk()
    root.title("Sneak")

    Label(font="Arial 20", text="Sneak", width=20, height=3).pack()
    but1 = Button(text="Simple", width=20, command=root.destroy)
    but2 = Button(text="Difficult", width=20, command=root.destroy)
    but1.pack()
    but2.pack()
    root.mainloop()

def main():
    global snake_x, snake_y, root

    create_window()

    while Game_Running:
        check_can_we_delete_snake_item()
        check_if_we_found_present()
        score()
        check_if_borders()
        check_we_touch_self(snake_x + snake_x_nav, snake_y + snake_y_nav)
        snake_x = snake_x + snake_x_nav
        snake_y = snake_y + snake_y_nav
        snake_paint_item(canvas, snake_x, snake_y)
        tk.update()
        time.sleep(speed_sneak)

    tk.destroy()

    root = Tk()
    root.title("Конец")

    Label(font="Arial 20", text="Ваш счёт: " + str(sneak_score), width=20, height=3).pack()
    but1 = Button(text="End", width=20, command=root.destroy)
    but2 = Button(text="Restart", width=20, command=restart)
    but1.pack()
    but2.pack()
    root.mainloop()



main()
