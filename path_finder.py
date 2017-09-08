import time
from sense_hat import SenseHat

# constants
MAX_GRID_SIDE_INDEX = 7
GRID_SIDE_LENGTH = MAX_GRID_SIDE_INDEX+1
SLOW_DOWN_SECONDS = 0.05
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

class MuseumPathFinder:

    def __init__(self):
        self.sense = SenseHat()
        self.game_grid = list(DEFAULT_GRID)
        self.cursor_position = [0, 0]

    def store_steps(self, x, y, n):
        if x - n < 0 and x + n > MAX_GRID_SIDE_INDEX and y - n < 0 and y + n > MAX_GRID_SIDE_INDEX:
            return

        # stay in bounds
        start_x = max(x - n, 0)
        end_x = min(x + n, MAX_GRID_SIDE_INDEX)
        start_y = max(y - n, 0)
        end_y = min(y + n, MAX_GRID_SIDE_INDEX)

        # mark the edges of the region with the color code
        # for the number of steps from a security guard
        for i_x in range(start_x, end_x+1):
            for i_y in range(start_y, end_y+1):
                if i_x == start_x or i_x == end_x or i_y == start_y or i_y == end_y:
                    existing = self.game_grid[MuseumPathFinder.coordinates_to_index(i_x, i_y)]
                    if existing == EMPTY or (existing in STEPS and n - 1 < STEPS.index(existing)):
                        self.game_grid[MuseumPathFinder.coordinates_to_index(i_x, i_y)] = STEPS[n-1]
                    else:
                        continue
                    # slow down the process for visual effect
                    time.sleep(SLOW_DOWN_SECONDS)
                    self.redraw()

        self.store_steps(x, y, n + 1)

    def calculate_shortest_paths(self):
        # visit each cell and calculate/store path lengths
        # by color coding when a security guard is found
        for x in range(GRID_SIDE_LENGTH):
            for y in range(GRID_SIDE_LENGTH):
                if self.game_grid[MuseumPathFinder.coordinates_to_index(x, y)] == COP:
                    self.store_steps(x, y, 1)

    def coordinates_to_index(x, y):
        # our game grid is an array vs. matrix to simplify interface with sense hat set_pixels
        return x + y * GRID_SIDE_LENGTH

    def redraw(self):
        # render current grid and joystick cursor position
        self.sense.set_pixels(self.game_grid)
        self.sense.set_pixel(self.cursor_position[0], self.cursor_position[1], CURSOR[0], CURSOR[1], CURSOR[2])

    def animate_toy(self):
        held = False
        # joystick input loop
        while True:
            for event in self.sense.stick.get_events():
                if event.action == "released":
                    # handle cursor movement
                    if event.direction == "up" and self.cursor_position[1] > 0:
                        self.cursor_position[1] -= 1
                    elif event.direction == "left" and self.cursor_position[0] > 0:
                        self.cursor_position[0] -= 1
                    elif event.direction == "down" and self.cursor_position[1] < MAX_GRID_SIDE_INDEX:
                        self.cursor_position[1] += 1
                    elif event.direction == "right" and self.cursor_position[0] < MAX_GRID_SIDE_INDEX:
                        self.cursor_position[0] += 1
                    # handle run, reset, and mark cop
                    elif event.direction == "middle":
                        if held and self.cursor_position == [0, 0]:
                            self.calculate_shortest_paths()
                        elif held:
                            self.game_grid = list(DEFAULT_GRID)
                        else:
                            self.game_grid[MuseumPathFinder.coordinates_to_index(self.cursor_position[0], self.cursor_position[1])] = COP

                    held = False
                    self.redraw()

                elif event.action == "held":
                    # handle held down button cursor movement
                    if event.direction == "up" and self.cursor_position[1] > 0:
                        self.cursor_position[1] -= 1
                    elif event.direction == "left" and self.cursor_position[0] > 0:
                        self.cursor_position[0] -= 1
                    elif event.direction == "down" and self.cursor_position[1] < MAX_GRID_SIDE_INDEX:
                        self.cursor_position[1] += 1
                    elif event.direction == "right" and self.cursor_position[0] < MAX_GRID_SIDE_INDEX:
                        self.cursor_position[0] += 1

                    held = True

if __name__ == "__main__":
    toy = MuseumPathFinder()
    toy.animate_toy()

