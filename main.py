from draw import *
from constants import *

def main():
    pygame.init()

    draw = Draw()
    screen.fill(WHITE)
    run = True

    while run:
        draw_grid()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: run = False
            # set start node
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s: draw.s, draw.g = True, False
                if event.key == pygame.K_g: draw.s, draw.g = False, True
                if event.key == pygame.K_RETURN: draw.a_star()
                if event.key == pygame.K_r: draw.reset()  # R for reset
                if event.key == pygame.K_d:
                    draw.draw = True  # D for drawing blocks
                    draw.erase = False
                if event.key == pygame.K_c:
                    draw.draw = False
                    draw.erase = True
                if event.key == pygame.K_SPACE:
                    draw.draw, draw.erase = False, False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not draw.draw: draw.set_start_goal(event)
            if event.type == pygame.MOUSEMOTION:
                if draw.draw or draw.erase:
                    draw.draw_blocks(event)
        pygame.display.update()

    pygame.quit()


main()
