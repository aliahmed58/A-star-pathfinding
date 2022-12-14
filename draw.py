import math
from constants import *
from Node import Node

pygame.font.init()


# Draw the boxes grid on pygame screen
def draw_grid():
    for x in range(0, WIN_WIDTH, BLOCK_SIZE):
        for y in range(0, WIN_HEIGHT, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, BLACK, rect, 1)


# Calculate starting coordinates given a position of click on a box
def calc_cord(pos):
    x_val, y_val = pos
    x_remainder, y_remainder = float(x_val / BLOCK_SIZE), float(y_val / BLOCK_SIZE)

    x_remainder = round((x_remainder - int(x_remainder)), 4) * BLOCK_SIZE
    y_remainder = round((y_remainder - int(y_remainder)), 4) * BLOCK_SIZE

    x_val -= x_remainder
    y_val -= y_remainder

    return int(x_val), int(y_val)


# Fill a rectangle given its position and color
def set_rect(pos, color):
    x, y = calc_cord(pos)
    rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
    pygame.draw.rect(screen, color, rect, BLOCK_SIZE)


# Remove a filled box given its position
def clear_rect(pos):
    x, y = pos
    rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
    pygame.draw.rect(screen, WHITE, rect, BLOCK_SIZE)


# Class that keeps track of start, goal and its positions
class Draw:
    def __init__(self):
        self.draw = False
        self.erase = False
        self.start_set = False
        self.goal_found = False
        self.goal_set = False
        self.start_pos = (0, 0)
        self.goal_pos = (0, 0)
        self.curr_pos = (None, None)
        self.s, self.g = True, False

    # Method to handle setting goal and start nodes on the grid
    def set_start_goal(self, event):
        pos = calc_cord(event.pos)
        if self.s:
            if event.button == 1:
                if not self.start_set:
                    set_rect(event.pos, RED)
                    self.start_set = True
                    self.start_pos = calc_cord(event.pos)
                    self.curr_pos = self.start_pos
            if event.button == 3:
                if self.start_pos == pos:
                    if self.start_set:
                        clear_rect(pos)
                        self.start_set = False
        if self.g:
            if event.button == 1:
                if not self.goal_set:
                    set_rect(event.pos, GREEN)
                    self.goal_pos = calc_cord(event.pos)
                    self.goal_set = True
            if event.button == 3:
                if self.goal_pos == pos:
                    if self.goal_set:
                        clear_rect(pos)
                        self.goal_set = False

    def reset(self):
        empty = (None, None)
        self.start_set, self.goal_set, self.s, self.g = False, False, True, False
        self.goal_found = False
        self.goal_pos, self.start_pos, self.curr_pos = empty, empty, empty
        screen.fill(WHITE)
        draw_grid()

    def draw_blocks(self, event):
        pos = calc_cord(event.pos)
        if pos == self.start_pos or pos == self.goal_pos:
            return
        if self.draw:
            set_rect(pos, WALL)
            pygame.display.update()
        if self.erase:
            set_rect(pos, WHITE)
            pygame.display.update()

    def a_star(self):
        # get font
        font = pygame.font.Font('./raleway.ttf', FONT_SIZE)
        if not self.goal_set or not self.start_set:
            return

        if self.start_pos == self.goal_pos:
            return

        # open list to keep track of nodes to be discovered
        open_list = []
        # close list to keep track of nodes already discovered
        close_list = []
        # create start node

        start_node = Node(self.start_pos[0], self.start_pos[1])

        # add the start node to open list
        open_list.append(start_node)

        # path list to store path after node is found
        path = []

        # move time variable
        move_time = 0

        while len(open_list) != 0:
            # get the current time from pygame
            curr_time = pygame.time.get_ticks()

            # only execute the following code after certain intervals
            if curr_time > move_time:

                # change move time each loop based on SPEED in constants.py
                move_time = curr_time + SPEED

                # sort the open list for the nodes with the lowest cost on top
                open_list.sort(key=lambda z: z.total_cost)

                # get the node with the lowest total cost
                node = open_list.pop(0)

                # add the node to close list since it doesn't need to be looked at again
                close_list.append(node)

                # set the curr position to the selected node
                self.curr_pos = (node.x, node.y)

                # if goal node is found - calculate path by back tracking the nodes using their
                # parents set during the search
                if node.x == self.goal_pos[0] and node.y == self.goal_pos[1]:
                    path = []
                    current = node
                    while current is not None:
                        path.append(current)
                        current = current.parent
                    break

                # draw the rectangle on screen
                node_pos = (node.x, node.y)
                if node_pos != self.start_pos: set_rect(node_pos, BLUE)

                # get neighbouring cells
                neighbors = self.get_blocks((node.x, node.y))
                for cell in neighbors:

                    # if cell is already in close list, skip
                    if cell in close_list:
                        continue

                    # check if the adjacent block is a valid cell
                    if is_cell_valid((cell.x, cell.y)):
                        # if the cell is diagonal give it a higher g_cost +
                        # the selected node's g_cost
                        if diagonal_allowed:
                            if cell.diagonal:
                                cell.g_cost = node.g_cost + 14
                            else:
                                cell.g_cost = node.g_cost + 10
                        else:
                            if cell.diagonal:
                                continue
                            else:
                                cell.g_cost = node.g_cost + 10
                    # if the cell is invalid, skip
                    else:
                        continue

                    dx = abs(cell.x - self.goal_pos[0])
                    dy = abs(cell.y - self.goal_pos[1])

                    # calculate the h cost by using manhattan distance
                    # cell.h_cost = BLOCK_SIZE * (dx + dy) + 20 * min(dx, dy)
                    cell.h_cost = dx + dy
                    # set the total cost as g + h
                    cell.total_cost = cell.h_cost + cell.g_cost

                    # set the neighbour cell parent as current selected node
                    cell.parent = node

                    # check if the cell is already in open list
                    # if already found, compare it's g_cost with the current cell
                    if cell in open_list:
                        index = open_list.index(cell)
                        exists = open_list[index]
                        if exists.g_cost > cell.g_cost:
                            open_list.remove(exists)
                            open_list.append(cell)

                    else:
                        # insert in open list if not present
                        open_list.append(cell)

                    # if the neighbouring node is not goal or start draw a CYAN cell
                    if (cell.x, cell.y) != self.start_pos and (cell.x, cell.y) != self.goal_pos:
                        set_rect((cell.x, cell.y), CYAN)

                    t_surface = font.render(str(int(cell.total_cost)), False, BLACK)
                    screen.blit(t_surface, (cell.x + 10, cell.y))

                pygame.display.flip()

        # Draw path in the list
        for x in path:
            if (x.x, x.y) != self.start_pos and (x.x, x.y) != self.goal_pos: set_rect((x.x, x.y),
                                                                                      PINK)

    @staticmethod
    def get_blocks(pos):
        # fetch x and y pos and convert to int
        x, y = pos
        x, y = int(x), int(y)

        # LEFT of current cell
        pos_x, pos_y = calc_cord((x - 2, y + 2))
        left = Node(pos_x, pos_y)
        # RIGHT of current cell
        pos_x, pos_y = calc_cord((x + BLOCK_SIZE + 2, y + 2))
        right = Node(pos_x, pos_y)
        # TOP of current cell
        pos_x, pos_y = calc_cord((x + 2, y - 2))
        top = Node(pos_x, pos_y)
        # BOTTOM of current cell
        pos_x, pos_y = calc_cord((x + 2, y + BLOCK_SIZE + 2))
        bottom = Node(pos_x, pos_y)
        # dtl - diagonal top left
        pos_x, pos_y = calc_cord((x - 2, y - 2))
        dtl = Node(pos_x, pos_y)
        dtl.diagonal = True
        # dtr - diagonal top right
        pos_x, pos_y = calc_cord((x + BLOCK_SIZE + 2, y - 2))
        dtr = Node(pos_x, pos_y)
        dtr.diagonal = True
        # dbl - diagonal bottom left
        pos_x, pos_y = calc_cord((x - 2, y + BLOCK_SIZE + 2))
        dbl = Node(pos_x, pos_y)
        dbl.diagonal = True
        # dbr - diagonal bottom right
        pos_x, pos_y = calc_cord((x + BLOCK_SIZE + 2, y + BLOCK_SIZE + 2))
        dbr = Node(pos_x, pos_y)
        dbr.diagonal = True 

        #  return list of all cells
        return [left, right, top, bottom, dtl, dtr, dbl, dbr]


def is_pixel_black(pos):
    try:
        return screen.get_at(pos)[:3] == WALL
    except IndexError:
        return True


def is_cell_valid(pos):
    # get x and y value from pos
    x, y = pos
    # convert pos to integer values
    x, y = int(x), int(y)

    center = calc_center(x, y)
    if 0 > center[0] > WIN_WIDTH:
        return False
    if 0 > center[1] > WIN_HEIGHT:
        return False

    # if cell is out of x bounds - return false - not valid
    if 0 > x > WIN_WIDTH:
        return False
    # if cell is out of y bounds - return false - not valid
    if 0 > y > WIN_HEIGHT:
        return False
    # if cell is a wall, return false - not valid
    if is_pixel_black((x + 1, y + 1)):
        return False

    # if all the above if conditions fail, cell is valid - return true
    return True


def distance(pos1, pos2):
    x1, x2 = pos1[0], pos2[0]
    y1, y2 = pos1[1], pos2[1]

    del_x = x2 - x1
    del_y = y2 - y1
    return int(math.sqrt(pow(del_x, 2) + pow(del_y, 2)))


# given x and y variables calculate the center of the cell
def calc_center(x1, y1):
    x, y = calc_cord((x1, y1))
    x = int(x + (BLOCK_SIZE / 2))
    y = int(y + (BLOCK_SIZE / 2))
    return x, y
