import time
from sense_hat import SenseHat
sense = SenseHat()

MAX_GRID_SIDE_INDEX = 7
GRID_SIDE_LENGTH = MAX_GRID_SIDE_INDEX+1
EMPTY = [0, 0, 0] # black
CURSOR = [255, 255, 255] # white
COP = [255, 255, 255] # white
STEPS = [[255, 0, 0], # red
         [255, 127, 0], # orange
         [255, 255, 0], # yellow
         [0, 255, 0], # green
         [0, 0, 255], # blue
         [75, 0, 130], # indigo
         [159, 0, 255]] # violet
DEFAULT_GRID = [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY,
                EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY,
                EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY,
                EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY,
                EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY,
                EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY,
                EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY,
                EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY]

game_grid = list(DEFAULT_GRID)
cursor_position = [0, 0]

def paint_steps(x, y, n):
    if x - n < 0 and x + n > MAX_GRID_SIDE_INDEX and y - n < 0 and y + n > MAX_GRID_SIDE_INDEX:
        return

    start_x = max(x - n, 0)
    end_x = min(x + n, MAX_GRID_SIDE_INDEX)
    start_y = max(y - n, 0)
    end_y = min(y + n, MAX_GRID_SIDE_INDEX)

    for i_x in range(start_x, end_x+1):
        for i_y in range(start_y, end_y+1):
            if i_x == start_x or i_x == end_x or i_y == start_y or i_y == end_y:
                existing = game_grid[coordinates_to_index(i_x, i_y)]
                if existing == EMPTY or (existing in STEPS and n - 1 < STEPS.index(existing)):
                    game_grid[coordinates_to_index(i_x, i_y)] = STEPS[n-1]
                else:
                    continue
                time.sleep(0.05)
                redraw()

    paint_steps(x, y, n + 1)

def calculate_shortest_paths():
    for x in range(GRID_SIDE_LENGTH):
        for y in range(GRID_SIDE_LENGTH):
            if game_grid[coordinates_to_index(x, y)] == COP:
                paint_steps(x, y, 1)

def coordinates_to_index(x, y):
    return x + y * GRID_SIDE_LENGTH

def redraw():
    sense.set_pixels(game_grid)
    sense.set_pixel(cursor_position[0], cursor_position[1], CURSOR[0], CURSOR[1], CURSOR[2])

held = False
while True:
    for event in sense.stick.get_events():
        print(event.direction, event.action)
        if event.action == "released":
            if event.direction == "up" and cursor_position[1] > 0:
                cursor_position[1] -= 1
            elif event.direction == "left" and cursor_position[0] > 0:
                cursor_position[0] -= 1
            elif event.direction == "down" and cursor_position[1] < MAX_GRID_SIDE_INDEX:
                cursor_position[1] += 1
            elif event.direction == "right" and cursor_position[0] < MAX_GRID_SIDE_INDEX:
                cursor_position[0] += 1
            elif event.direction == "middle":
                if held and cursor_position == [0, 0]:
                    calculate_shortest_paths()
                elif held:
                    game_grid = list(DEFAULT_GRID)
                else:
                    game_grid[coordinates_to_index(cursor_position[0], cursor_position[1])] = COP

            held = False
            redraw()

        elif event.action == "held":
            if event.direction == "up" and cursor_position[1] > 0:
                cursor_position[1] -= 1
            elif event.direction == "left" and cursor_position[0] > 0:
                cursor_position[0] -= 1
            elif event.direction == "down" and cursor_position[1] < MAX_GRID_SIDE_INDEX:
                cursor_position[1] += 1
            elif event.direction == "right" and cursor_position[0] < MAX_GRID_SIDE_INDEX:
                cursor_position[0] += 1

            held = True


