from tkinter import *
import random

# глобальные переменные
CANVAS_WIDTH = 640
CANVAS_HEIGHT = 480
SNAKE_SIZE = 20
MOVE_INCREMENT = 20
DELAY = 100  # задержка перед следующим ходом, в миллисекундах

# цвета
SNAKE_COLOR = 'green'
FOOD_COLOR = 'red'
BONUS_COLOR = 'yellow'
WALL_COLOR = 'gray'
BACKGROUND_COLOR = 'black'
TEXT_COLOR = 'white'

# пересчёт координат
def get_new_position(coords, direction):
    x, y = coords[-1]  # координаты головы змеи
    if direction == 'Up':
        return x, y - SNAKE_SIZE
    elif direction == 'Down':
        return x, y + SNAKE_SIZE
    elif direction == 'Left':
        return x - SNAKE_SIZE, y
    elif direction == 'Right':
        return x + SNAKE_SIZE, y

# генерация случайной позиции
def get_random_position():
    x = random.randrange(0, CANVAS_WIDTH - SNAKE_SIZE, SNAKE_SIZE)
    y = random.randrange(0, CANVAS_HEIGHT - SNAKE_SIZE, SNAKE_SIZE)
    return x, y

# рисование змеи
def draw_snake(canvas, coords):
    for i, (x, y) in enumerate(coords):
        if i == len(coords) - 1:  # голова змеи
            color = SNAKE_COLOR
        else:
            color = WALL_COLOR
        canvas.create_rectangle(x, y, x + SNAKE_SIZE, y + SNAKE_SIZE, fill=color)

# рисование еды
def draw_food(canvas, food_pos):
    x, y = food_pos
    canvas.create_oval(x, y, x + SNAKE_SIZE, y + SNAKE_SIZE, fill=FOOD_COLOR)

# рисование бонуса
def draw_bonus(canvas, bonus_pos):
    x, y = bonus_pos
    canvas.create_oval(x, y, x + SNAKE_SIZE, y + SNAKE_SIZE, fill=BONUS_COLOR)

# проверка столкновения со стеной
def check_wall_collision(coords):
    x, y = coords[-1]
    if x < 0 or x >= CANVAS_WIDTH or y < 0 or y >= CANVAS_HEIGHT:
        return True
    else:
        return False

# проверка столкновения с хвостом
def check_tail_collision(coords):
    head = coords[-1]
    tail = coords[:-1]
    if head in tail:
        return True
    else:
        return False

# обработка нажатий клавиш
def handle_key_press(event):
    global direction
    global bonus_active
    if event.keysym in {'Up', 'Down', 'Left', 'Right'}:
        if event.keysym == 'Up' and direction != 'Down':
            direction = 'Up'
        elif event.keysym == 'Down' and direction != 'Up':
            direction = 'Down'
        elif event.keysym == 'Left' and direction != 'Right':
            direction = 'Left'
        elif event.keysym == 'Right' and direction != 'Left':
            direction = 'Right'
    elif event.keysym == 'p':
        start_game()
    elif event.keysym == 'e':
        root.destroy()

# обновление игрового поля
def update():
    global snake_coords
    global food_pos
    global bonus_active
    global bonus_pos
    global score
    score_var.set(f'Score: {score}')
    # движение змеи
    new_head = get_new_position(snake_coords, direction)
    snake_coords.append(new_head)
    # проверка столкновения со стеной/хвостом
    if check_wall_collision(snake_coords) or check_tail_collision(snake_coords):
        game_over()
        return
    # проверка наличия еды
    if snake_coords[-1] == food_pos:
        score += 1
        if score % 5 == 0:
            bonus_active = True
            bonus_pos = get_random_position()
        else:
            bonus_active = False
        food_pos = get_random_position()
    else:
        snake_coords.pop(0)
    # проверка наличия бонуса
    if bonus_active and snake_coords[-1] == bonus_pos:
        bonus_active = False
        snake_coords = snake_coords[:-1]
    # обновление холста
    canvas.delete('all')
    canvas.create_rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, fill=BACKGROUND_COLOR)
    draw_snake(canvas, snake_coords)
    draw_food(canvas, food_pos)
    if bonus_active:
        draw_bonus(canvas, bonus_pos)
    root.after(DELAY, update)

# начало игры
def start_game():
    global snake_coords
    global food_pos
    global bonus_active
    global bonus_pos
    global score
    score = 0
    score_var.set(f'Score: {score}')
    snake_coords = [(CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2)]
    food_pos = get_random_position()
    bonus_active = False
    bonus_pos = None
    update()

# конец игры
def game_over():
    canvas.create_text(CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2, text='Game over', font=('Arial', 24), fill=TEXT_COLOR)
    canvas.create_text(CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2 + 30, text='Press P to play again or E to exit', font=('Arial', 16), fill=TEXT_COLOR)

# создание окна
root = Tk()
root.title('Snake')
root.resizable(0, 0)

# создание холста
canvas = Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg=BACKGROUND_COLOR)
canvas.pack()

# создание строки счёта
score = 0
score_var = StringVar()
score_label = Label(root, textvariable=score_var, font=('Arial', 16), fg=TEXT_COLOR, bg=BACKGROUND_COLOR)
score_label.pack()

# обработка нажатий клавиш
direction = 'Right'
root.bind('<KeyPress>', handle_key_press)

# запуск игры
start_game()

root.mainloop()
