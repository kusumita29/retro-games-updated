import pygame
import sys
pygame.font.init()
import spacefight
import tetris
import super_runner
import snake

# GLOBALS VARS
WIDTH = 800
HEIGHT = 600

# building the basic window
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Main Menu')

def function1():
    spacefight.main()
    return

def function2():
    tetris.main()
    return

def function3():
    super_runner.main()
    return 

def function4():
    snake.maingame()
    return

def function5():
    return 

class Button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color

    def draw(self, surface, font):
        pygame.draw.rect(surface, self.color, self.rect)
        text_surface = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
        pygame.display.update()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

button1 = Button(300, 200, 200, 50, "Space Fight", (250, 0, 0))
button2 = Button(300, 275, 200, 50, "Tetris", (70, 160, 43))
button3 = Button(300, 350, 200, 50, "Super Runner", (0, 0, 247))
button4 = Button(300, 425, 200, 50, "Snake-mania", (246, 70, 165))

def display_menu():
    font3 = pygame.font.SysFont(None, 40)
    button1.draw(WINDOW, font3)
    button2.draw(WINDOW, font3)
    button3.draw(WINDOW, font3)
    button4.draw(WINDOW, font3)
    font2 = pygame.font.SysFont(None, 80)
    label = font2.render('RETRO GAMES', 1, (247, 247, 0))
    WINDOW.blit(label, (180, 130))

    pygame.display.update()

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if button1.handle_event(event):
            function1()
        if button2.handle_event(event):
            function2()
        if button3.handle_event(event):
            function3()
        if button4.handle_event(event):
            function4()    

display_menu()