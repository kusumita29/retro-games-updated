import pygame
import random
pygame.mixer.init()
pygame.font.init()

# GLOBALS VARS
WIDTH = 800
HEIGHT = 600

# the game has 10 x 20 blocks 
GAME_WIDTH = 200  
GAME_HEIGHT = 400  
BLOCK_SIZE = 20

# position to start drawing the 10 x 20 grid from
CORNER_X = 300
CORNER_Y = 120

# building the basic window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('TETRIS')


# Shape formats and all the possible rotations in a list
S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],

     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],

     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],

     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],

     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],

     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
      
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],

     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],

     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],

     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],

     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],

     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],

     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

# all the shapes represented by an alphabet which redirects it to the list
shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]


class Piece(object):
    rows = 20
    columns = 10 

    def __init__(self, column, row, shape):
        self.X = column
        self.Y = row
        self.SHAPE = shape
        self.COLOR = shape_colors[shapes.index(shape)]
        self.ROTATION = 0

# creates the grid with each block having the color black initially
# (0, 0, 0) is the RGB for black
def create_grid(locked_positions={}):
    grid = [[(0,0,0) for x in range(10)] for y in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j,i) in locked_positions:
                c = locked_positions[(j,i)]
                grid[i][j] = c
    return grid

# to rotate the blocks (if the user wants) and add the blocks to the grid
def convert_shape_format(shape):
    positions = []

    # traverses through all the possible rotations of the list
    format = shape.SHAPE[shape.ROTATION % len(shape.SHAPE)]

    # store the index of the Os in the shape list for any piece in th positions list
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.X + j, shape.Y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions

# checks if the block is moving in a valid space
def valid_space(shape, grid):

    # takes in all the indices of the blocks empty
    accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    
    # flattens out the list for easier traversal
    accepted_positions = [j for sub in accepted_positions for j in sub]

    formatted = convert_shape_format(shape)

    # if the block touches the height then the position is not valid
    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False

    return True

# if no more tetris blocks fit in the grid and it touches the height 
def check_lost(positions):
    for pos in positions:
        if pos[1] < 1:
            return True
    return False

# randomly generates a shape
def get_shape():
    global shapes, shape_colors
    return Piece(5, 0, random.choice(shapes))

# function to generate a text label when the game is lost
def draw_text_middle(text, size, color, WIN):
    font = pygame.font.SysFont('arial', size, bold=True)
    label = font.render(text, 1, color)

    WIN.blit(label, (CORNER_X + GAME_WIDTH/2 - (label.get_width() / 2), CORNER_Y + GAME_HEIGHT/2 - label.get_height()/2))

def draw_grid(WIN):
    for i in range(20):
        # drawing horizontal grey lines
        pygame.draw.line(
            WIN, (255, 255, 255), (CORNER_X, CORNER_Y+ i*BLOCK_SIZE), (CORNER_X + GAME_WIDTH, CORNER_Y + i * BLOCK_SIZE)) 
        for j in range(11):
            # drawing the vertical grey lines
            pygame.draw.line(
                WIN, (255, 255, 255), (CORNER_X + j * BLOCK_SIZE, CORNER_Y), (CORNER_X + j * BLOCK_SIZE, CORNER_Y + GAME_HEIGHT)) 

def clear_rows(grid, locked):
    inc = 0
    # check from the bottom of the grid to the top
    for i in range(len(grid)-1, -1, -1): 
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            # add positions to remove from locked
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue

    # shifts the entire column down             
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)

    return inc

def draw_window(WIN, score):
    WIN.fill((36, 64, 95))
    # adding the title to the top of the window
    title = pygame.image.load('Assets/Tetris/tetris-blocks.png')
    title = pygame.transform.scale(title, (200,40))
    WIN.blit(title, (295, 30))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(WIN, grid[i][j], (CORNER_X + j* 20, CORNER_Y + i * 20, 20, 20), 0)

    font = pygame.font.SysFont('arial', 30, bold=True)
    label = font.render('Score: ' + str(score), 1, (255,255,255))

    WIN.blit(label, (CORNER_X + GAME_WIDTH/2 - (label.get_width() / 2), CORNER_Y + HEIGHT -150 - label.get_height()/2))

    draw_grid(WIN)

    # drawing the playing area border  
    pygame.draw.rect(WIN, (255, 255, 255), (CORNER_X - 5, CORNER_Y - 5, GAME_WIDTH + 10, GAME_HEIGHT + 10), 5)

def main():
    global grid
    # the key is the position of the block in the grid 
    # the value is the color of that grid - black means its empty otherwise filled 
    locked_positions = {}  
    grid = create_grid(locked_positions)
    bg_music = pygame.mixer.Sound('Assets/Tetris/music.mp3')
    bg_music.play(loops = -1)

    run = True

    # generating and manipulating the blocks
    change_piece = False
    current_piece = get_shape()
    next_piece = get_shape()
    
    clock = pygame.time.Clock()
    fall_time = 0
    
    # to update the score
    score = 0

    while run:
        # the initial fall speed
        fall_speed = 0.5

        grid = create_grid(locked_positions)

        # it calculates the time our computer takes for a block to reach the bottom of the grid
        fall_time += clock.get_rawtime()
        clock.tick()

        # pieces falling 
        if fall_time/1000 >= fall_speed:
            fall_time = 0
            current_piece.Y += 1
            if not (valid_space(current_piece, grid)) and current_piece.Y > 0:
                current_piece.Y -= 1
                change_piece = True

        # closes the window on clicking the Quit button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

             # shifting the pieces
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.X -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.X += 1

                if event.key == pygame.K_RIGHT:
                    current_piece.X += 1
                    if not valid_space(current_piece, grid):
                        current_piece.X -= 1

                if event.key == pygame.K_DOWN:
                    current_piece.Y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.Y -= 1

                # UP arrow key rotates the piece
                if event.key == pygame.K_UP:
                    current_piece.ROTATION = current_piece.ROTATION + 1 % len(current_piece.SHAPE)
                    if not valid_space(current_piece, grid):
                        current_piece.ROTATION = current_piece.ROTATION - 1 % len(current_piece.SHAPE)

        shape_pos = convert_shape_format(current_piece)

        # # add colors to the shape
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.COLOR

        #  # if the piece touches an already placed piece or the bottom
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.COLOR
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False

            # call four times to check for multiple clear rows
            clear_rows(grid, locked_positions)

        prev_score = score
        score += clear_rows(grid, locked_positions) * 10
        # if prev_score != score:
        #     bingo_music = pygame.mixer.Sound('Assets/Tetris/bingo.mp3')

        draw_window(WIN, score)
        pygame.display.update()

        # Check if the user has lost
        if check_lost(locked_positions):
            run = False

    # displays a relevant text message
    draw_text_middle("YOU LOST", 40, (255,255,255), WIN)
    pygame.display.update()
    pygame.time.delay(2000)

if __name__ == "__main__":
    main()