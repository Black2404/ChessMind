import pygame, sys
from config import *
from ui import button
from game import play_game

def main_menu():
    while True:
        SCREEN.fill(BG_COLOR)
        title = BIG_FONT.render("Chess Game", True, (0,0,0))
        SCREEN.blit(title, (WIDTH//2 - title.get_width()//2, 100))
        mx, my = pygame.mouse.get_pos()
        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True

        if button("Player vs Player", WIDTH//2-100, 220, (mx,my), click, 200, 50):
            play_game(False)
        if button("Player vs AI", WIDTH//2-100, 300, (mx,my), click, 200, 50):
            play_game(True)
        if button("Exit", WIDTH//2-100, 380, (mx,my), click, 200, 50):
            pygame.quit(); sys.exit()

        pygame.display.update()

if __name__ == "__main__":
    main_menu()
