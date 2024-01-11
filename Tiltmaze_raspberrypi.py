from sense_hat import SenseHat
from time import sleep, time

sense = SenseHat()
sense.clear()

r = (255, 0, 0)
g = (0, 255, 0)
b = (0, 0, 0)
w = (255, 255, 255)

def display_level(level):
    sense.show_message(f'Level {level}')

def play_level(maze):
    global game_over, x, y
    game_over = False
    start_time = time()
    lost = False

    while not game_over and not lost:
        move_marble()
        check_win(x, y)
        maze[y][x] = w
        sense.set_pixels(sum(maze, []))
        sleep(0.05)
        maze[y][x] = b

        elapsed_time = time() - start_time
        if elapsed_time > 10:
            sense.show_message('You Lose')
            lost = True
            return lost


    if not lost:
        sense.show_message('You Win')

def move_marble():
    global x, y

    pitch = sense.get_orientation()['pitch']
    roll = sense.get_orientation()['roll']

    new_x = x
    new_y = y

    if 1 < pitch < 179 and x != 0:
        new_x -= 1
    elif 359 > pitch > 179 and x != 7:
        new_x += 1

    if 1 < roll < 179 and y != 7:
        new_y += 1
    elif 359 > roll > 179 and y != 0:
        new_y -= 1
    x, y = check_wall(x, y, new_x, new_y)

def check_wall(x, y, new_x, new_y):
    if maze[new_y][new_x] != r:
        return new_x, new_y
    elif maze[new_y][x] != r:
        return x, new_y
    elif maze[y][new_x] != r:
        return new_x, y

    return x, y

def check_win(x, y):
    global game_over
    if maze[y][x] == g:
        game_over = True


levels = [
    [[r, r, r, r, r, r, r, r],
     [r, b, b, b, b, b, b, r],
     [r, r, r, b, r, b, b, r],
     [r, b, r, b, r, r, r, r],
     [r, b, b, b, b, b, b, r],
     [r, b, r, r, r, r, b, r],
     [r, b, b, r, g, b, b, r],
     [r, r, r, r, r, r, r, r]],
    
    [[b, r, r, r, r, r, b, r],
     [r, b, r, r, r, b, b, r],
     [r, r, b, r, b, r, r, r],
     [r, r, r, b, r, r, b, g],
     [r, r, b, r, b, r, b, r],
     [r, b, r, r, r, b, r, r],
     [b, r, r, r, b, r, b, r],
     [r, b, b, b, b, b, b, b]],
    
    [[b, r, r, r, r, r, r, b],
     [r, b, b, r, r, b, b, r],
     [r, r, b, r, r, b, b, r],
     [b, b, b, b, b, b, r, r],
     [b, b, b, b, b, b, r, g],
     [r, r, b, r, r, b, b, r],
     [r, b, b, r, r, b, b, b],
     [b, r, b, b, b, b, b, b]],
    
    [[r, b, b, b, b, r, r, r],
     [r, b, r, b, r, b, b, r],
     [b, r, r, b, r, b, b, r],
     [r, r, r, r, b, r, b, r],
     [b, r, r, b, r, b, r, r],
     [b, r, b, r, r, r, r, r],
     [r, b, r, b, r, b, r, g],
     [b, r, r, b, b, r, b, b]],
]
p=0
for i, maze in enumerate(levels, start=1):
    display_level(i)
    x = 1
    y = 1
    k=play_level(maze)
    if k == True:
        break
    p=i
sense.show_message("Score:"+str(p))
