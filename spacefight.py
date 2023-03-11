import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 600  
FPS = 60
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 40, 40 
STEP = 5 # how much the spaceships should move every time we press a navigation key
BULLET_SPEED = 10
MAX_BULLETS = 3 # maximum bullets that can be fired each round

# creating two unique events for situtions where the bullets hit the spaceships
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

# Setting the window dimension and the title of the window
WIN = pygame.display.set_mode((WIDTH,HEIGHT)) 
pygame.display.set_caption("SPACE FIGHT")

# generates a black thick line right across the center of the screen
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 5, HEIGHT)

BULLET_HIT = pygame.mixer.Sound(os.path.join('Assets', 'Space Fight', 'hit_sound.mp3'))
BULLET_FIRE = pygame.mixer.Sound(os.path.join('Assets', 'Space Fight', 'fire_sound.mp3'))

# adds the yellow and red spaceship image to the window
YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'Space Fight', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'Space Fight', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))

# sets the font size and style for the texts displayed on the screen
HEALTH_FONT = pygame.font.SysFont('calibri', 40)
WINNER_FONT = pygame.font.SysFont('calibri', 100)


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.fill((36, 64, 95)) # colour of the window is set to navy blue

    # health of each spaceship displayed at the top
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, (255, 255, 255))
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, (255, 255, 255))
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    # draws the spaceships
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    pygame.draw.rect(WIN, (0, 0, 0), BORDER)

    # drawing the bullets
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, (255, 255, 0), bullet) # YELLOW RGB = (255, 255, 0)

    for bullet in red_bullets:
        pygame.draw.rect(WIN, (255, 0, 0), bullet) # RED RGB = (255, 0, 0)
    
    pygame.display.update()

# function to move the yellow spaceship using the A,W,S,D keys
def yellow_move(key_pressed, yellow):
    if key_pressed[pygame.K_a] and yellow.x > 20:
        yellow.x -= STEP # left
    if key_pressed[pygame.K_d] and yellow.x < BORDER.x - 100:
        yellow.x += STEP # right
    if key_pressed[pygame.K_w] and yellow.y > 20:
        yellow.y -= STEP # up
    if key_pressed[pygame.K_s] and yellow.y < HEIGHT - 20 - yellow.height:
        yellow.y += STEP # down

# function to move the red spaceship using the UP, DOWN, LEFT and RIGHT arrow keys
def red_move(key_pressed, red):
    if key_pressed[pygame.K_LEFT] and red.x > BORDER.x + 100 - red.width:
        red.x -= STEP # left
    if key_pressed[pygame.K_RIGHT] and red.x < WIDTH - 20 - red.width:
        red.x += STEP # right
    if key_pressed[pygame.K_UP] and red.y > 20:
        red.y -= STEP # up
    if key_pressed[pygame.K_DOWN] and red.y < HEIGHT - 20 - red.height:
        red.y += STEP # down

# firing and colliding of the bullets
def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_SPEED
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_SPEED
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

# text displayed when a player wins and the game resets 
def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, (255, 255, 255))
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    clock = pygame.time.Clock()

    # drawing the Pygame rects
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    # creating lists for each spaceship to keep a count on the bullet numbers as we have limited bullets
    yellow_bullets = []
    red_bullets = []

    # keeping a track of the spaceships' health
    red_health = 10
    yellow_health = 10

    # keeps the window running until we click the quit button of the window
    run = True

    while run:
        #updates the window at the mentioned FPS if possible else at the highest possible FPS
        clock.tick(FPS) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            # we are using the left and right control to fire the bullets
            # left control - yellow spaceship
            # rigth control - red spaceship
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE.play()

            # if the bullets hit the other spaceship, that spaceship's health is reduced
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT.play()
                
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT.play()
        
        # when a spaceship runs out of health, a winner is displayed
        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"

        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break
                
        # captures the key pressed and passes it to the corresponding spaceship nav function
        key_pressed = pygame.key.get_pressed()
        yellow_move(key_pressed, yellow)
        red_move(key_pressed, red)

        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        pygame.display.update()
    

if __name__ == "__main__":
    main()