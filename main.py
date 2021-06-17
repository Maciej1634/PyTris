import pygame
from game import Tetris
from pygame import mixer
from os import path
import pygame_menu


def draw_screen():
    screen.blit(BG_IMG, (0, 0))
    text = font.render("punkty: "+str(game.points), True, (255, 255, 255))
    pygame.draw.rect(screen, GRID_BACKGROUND_COLOR,
                     (GAME_POSITIONS[0], GAME_POSITIONS[2], GAME_POSITIONS[1]-GAME_POSITIONS[0], GAME_POSITIONS[3]-GAME_POSITIONS[2]))
    l_up = (GAME_POSITIONS[0], GAME_POSITIONS[2])
    l_down = (GAME_POSITIONS[0], GAME_POSITIONS[3])
    r_up = (GAME_POSITIONS[1], GAME_POSITIONS[2])
    r_down = (GAME_POSITIONS[1], GAME_POSITIONS[3])
    pygame.draw.line(screen, LINE_COLOR, l_up, l_down, LINE_THICKNESS)
    pygame.draw.line(screen, LINE_COLOR, l_up, r_up, LINE_THICKNESS)
    pygame.draw.line(screen, LINE_COLOR, r_up, r_down, LINE_THICKNESS)
    pygame.draw.line(screen, LINE_COLOR, l_down, r_down, LINE_THICKNESS)
    for x in range(GRID_SIZE[1]-1):
        l_line = (l_up[0], l_up[1] + (BLOCK_SIZE*(x+1)))
        r_line = (r_up[0], r_up[1] + (BLOCK_SIZE*(x+1)))
        pygame.draw.line(screen, LINE_COLOR, l_line, r_line, LINE_THICKNESS)
    for x in range(GRID_SIZE[0]-1):
        l_line = (l_up[0] + (BLOCK_SIZE*(x+1)), l_up[1])
        r_line = (l_down[0] + (BLOCK_SIZE*(x+1)), l_down[1])
        pygame.draw.line(screen, LINE_COLOR, l_line, r_line, LINE_THICKNESS)
    screen.blit(text, (GAME_POSITIONS[1]+BLOCK_SIZE, GAME_POSITIONS[2]))


def small_grid_draw():
    l_up = (SMALL_GRID_POSITIONS[0], SMALL_GRID_POSITIONS[1])
    l_down = (SMALL_GRID_POSITIONS[0], SMALL_GRID_POSITIONS[3])
    r_up = (SMALL_GRID_POSITIONS[2], SMALL_GRID_POSITIONS[1])
    r_down = (SMALL_GRID_POSITIONS[2], SMALL_GRID_POSITIONS[3])
    pygame.draw.line(screen, LINE_COLOR, l_up, l_down, LINE_THICKNESS)
    pygame.draw.line(screen, LINE_COLOR, l_up, r_up, LINE_THICKNESS)
    pygame.draw.line(screen, LINE_COLOR, r_up, r_down, LINE_THICKNESS)
    pygame.draw.line(screen, LINE_COLOR, l_down, r_down, LINE_THICKNESS)
    for x in range(SMALL_GRID_SIZE[1]-1):
        l_line = (l_up[0], l_up[1] + (SMALL_BLOCK_SIZE*(x+1)))
        r_line = (r_up[0], r_up[1] + (SMALL_BLOCK_SIZE*(x+1)))
        pygame.draw.line(screen, LINE_COLOR, l_line, r_line, LINE_THICKNESS)
    for x in range(SMALL_GRID_SIZE[0]-1):
        l_line = (l_up[0] + (SMALL_BLOCK_SIZE*(x+1)), l_up[1])
        r_line = (l_down[0] + (SMALL_BLOCK_SIZE*(x+1)), l_down[1])
        pygame.draw.line(screen, LINE_COLOR, l_line, r_line, LINE_THICKNESS)


def draw_blocks():
    blocks = game.game_array
    for x in range(game.game_size[0]):
        for y in range(game.game_size[1]):
            if blocks[x][y] != 0:
                x_pos = GAME_POSITIONS[0] + BLOCK_SIZE*(x) + LINE_THICKNESS
                y_pos = GAME_POSITIONS[2] + BLOCK_SIZE*(y) + LINE_THICKNESS
                pygame.draw.rect(screen, game.get_pos_color(x, y),
                                 (x_pos, y_pos, BLOCK_SIZE - LINE_THICKNESS, BLOCK_SIZE - LINE_THICKNESS))


def draw_small_blocks():
    blocks = game.small_block_pos
    for x in range(4):
        x_pos = SMALL_GRID_POSITIONS[0] + \
            SMALL_BLOCK_SIZE*(blocks[x][0]) + LINE_THICKNESS
        y_pos = SMALL_GRID_POSITIONS[1] + \
            BLOCK_SIZE*(blocks[x][1]) + LINE_THICKNESS
        pygame.draw.rect(screen, NEXT_BLOCK_COLOR,
                         (x_pos, y_pos, SMALL_BLOCK_SIZE - LINE_THICKNESS, SMALL_BLOCK_SIZE - LINE_THICKNESS))


if __name__ == "__main__":
    # just bunch of self-describing variables
    SCREEN_SIZE = (1000, 768)
    BLOCK_SIZE = 35
    SMALL_BLOCK_SIZE = 30
    LINE_THICKNESS = 2
    FPS = 60
    ROTATE_TIMER_MAX = 60
    MAX_MOVE_TIMER = 10
    MAX_FALL_TIMER = 5
    MAX_ROTATE_TIMER = 5
    GAME_SPEED = 30
    GRID_SIZE = (11, 19)
    SMALL_GRID_SIZE = (5, 6)
    LINE_COLOR = (255, 255, 255)
    NEXT_BLOCK_COLOR = (255, 0, 0)
    BG_IMG = pygame.image.load(path.dirname(
        __file__)+"\\graphic\\bg.png")
    GAME_POSITIONS = (0.2*SCREEN_SIZE[0], ((0.2*SCREEN_SIZE[0]))+(BLOCK_SIZE*GRID_SIZE[0]),
                      0.1*SCREEN_SIZE[1], ((0.1*SCREEN_SIZE[1]))+(BLOCK_SIZE*GRID_SIZE[1]))
    SMALL_GRID_POSITIONS = (
        GAME_POSITIONS[1]+BLOCK_SIZE*1.2, GAME_POSITIONS[2]+BLOCK_SIZE*1.5,
        GAME_POSITIONS[1]+(SMALL_GRID_SIZE[0]*SMALL_BLOCK_SIZE)+BLOCK_SIZE*1.2, GAME_POSITIONS[2]+(SMALL_GRID_SIZE[1]*SMALL_BLOCK_SIZE)+BLOCK_SIZE*1.5)

    GRID_BACKGROUND_COLOR = (54, 52, 52)

    # init
    pygame.init()
    pygame.display.set_caption("PyTris")
    pygame.font.init()
    font = pygame.font.SysFont('Comic Sans MS', 30)
    mixer.music.load(path.dirname(
        __file__)+"\\music\\theme.ogg")
    mixer.music.play()
    game = Tetris(GRID_SIZE, SMALL_GRID_SIZE)
    game.init_game()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    clock = pygame.time.Clock()
    running = True
    # menu
    rotate_timer = 0
    game_timer = 0
    move_timer = 0
    move = 0
    fall = 0
    fall_timer = 0
    rotate = 0
    while running:
        clock.tick(FPS)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN] and fall == 0:
            game_timer = GAME_SPEED
            fall = 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_UP or event.key == pygame.K_w) and rotate == 0:
                    game.rotate_block()
                    rotate = 1
                if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and move == 0:
                    game.move_block("left")
                    move = 1
                if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and move == 0:
                    game.move_block("right")
                    move = 1

                    # if(rotate_timer == ROTATE_TIMER_MAX):
                    #     rotate_timer = 0
                    #     game.rotate_block()
        if (game_timer >= GAME_SPEED):
            game.nex_game_tick()
            game_timer = 0
            rotate = 0
        if move_timer >= MAX_MOVE_TIMER:
            move_timer = 0
            move = 0
        if fall_timer >= MAX_FALL_TIMER:
            fall_timer = 0
            fall = 0
        if rotate_timer >= MAX_ROTATE_TIMER:
            rotate_timer = 0
            rotate = 0
        move_timer += 1
        game_timer += 1
        fall_timer += 1
        rotate_timer += 1
        draw_screen()
        # small_grid_draw()
        draw_small_blocks()
        draw_blocks()
        pygame.display.flip()
    pygame.quit()
