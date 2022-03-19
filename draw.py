import math

import pygame
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

    return x_val, y_val


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
        self.start_pos = (None, None)
        self.goal_pos = (None, None)
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
        font = pygame.font.Font('./raleway.ttf', FONT_SIZE)
        if not self.goal_set or not self.start_set:
            return

        if self.start_pos == self.goal_pos:
            return

        open = []
        close = []
        start_node = Node(self.start_pos)
        goal_node = Node(self.goal_pos)

        goal_node.g_cost = (0, 0)
        goal_node.h_cost = (0, 0)
        start_node.g_cost = (goal_node.pos[0] - start_node.pos[0], goal_node.pos[1] -
                             start_node.pos[1])

        open.append(start_node)
        path = []

        move_time = 0

        while len(open) != 0:
            curr_time = pygame.time.get_ticks()
            if curr_time > move_time:
                move_time = curr_time + SPEED

                open.sort(key=lambda z: z.total_cost)

                node = open.pop(0)
                close.append(node)

                self.curr_pos = node.pos

                if node.pos == self.goal_pos:
                    path = []
                    current = node
                    while current is not None:
                        path.append(current)
                        current = current.parent
                    break

                if node.pos != self.start_pos: set_rect(node.pos, BLUE)

                x, y = int(node.pos[0]), int(node.pos[1])

                neighbors = self.get_blocks(self, node.pos)
                for box in neighbors:
                    if is_pixel_black(box.pos):
                        if box.diagonal:
                            h_cost = 2
                        else:
                            h_cost = 1

                        g_cost = abs(box.pos[0] - self.goal_pos[0]) + abs(box.pos[1] -
                                                                          self.goal_pos[1])
                        total_cost = h_cost + g_cost
                        new_x, new_y = calc_cord(box.pos)
                        ins = Node((new_x, new_y))

                        ins.parent = node

                        ins.h_cost = h_cost
                        ins.g_cost = g_cost
                        ins.total_cost = total_cost

                        if ins.pos != self.start_pos and ins.pos != self.goal_pos: set_rect(ins.pos,
                                                                                       CYAN)
                        t_surface = font.render(str(int(total_cost)), False, BLACK)
                        screen.blit(t_surface, (box.pos[0] - 10, box.pos[1]))

                        if ins not in open and ins not in close:
                            open.append(ins)

                pygame.display.flip()

        for x in path:
            if x.pos != self.start_pos and x.pos != self.goal_pos: set_rect(x.pos, PINK)

    @staticmethod
    def get_blocks(self, pos):
        x, y = pos
        x, y = int(x), int(y)

        left = Node(calc_center(x - 2, y + 2))

        right = Node(calc_center(x + BLOCK_SIZE + 2, y + 2))
        top = Node(calc_center(x + 2, y - 2))
        bottom = Node(calc_center(x + 2, y + BLOCK_SIZE + 2))
        # dtl - diagonal top left
        # dtr - diagonal top right and so on
        dtl = Node(calc_center(x - 2, y - 2))
        dtr = Node(calc_center(x + BLOCK_SIZE + 2, y - 2))
        dbl = Node(calc_center(x - 2, y + BLOCK_SIZE + 2))
        dbr = Node(calc_center(x + BLOCK_SIZE + 2, y + BLOCK_SIZE + 2))

        return [left, right, top, bottom, dtl, dtr, dbl, dbr]



def is_pixel_black(pos):
    return not screen.get_at(pos)[:3] == WALL


def distance(pos1, pos2):
    x1, x2 = pos1[0], pos2[0]
    y1, y2 = pos1[1], pos2[1]

    delx = x2 - x1
    dely = y2 - y1
    return int(math.sqrt(pow(delx, 2) + pow(dely, 2)))


def calc_center(x1, y1):
    x, y = calc_cord((x1, y1))
    x = int(x + (BLOCK_SIZE / 2))
    y = int(y + (BLOCK_SIZE / 2))
    return (x, y)


