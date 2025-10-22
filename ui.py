import pygame
import sys
from config import *

# UI COMPONENTS
def button(text, x, y, mouse, click, w=120, h=40):
    rect = pygame.Rect(x, y, w, h)
    color = BTN_HOVER if rect.collidepoint(mouse) else BTN_COLOR
    pygame.draw.rect(SCREEN, color, rect, border_radius=6)
    pygame.draw.rect(SCREEN, (0, 0, 0), rect, 2, border_radius=6)
    label = FONT.render(text, True, (0, 0, 0))
    SCREEN.blit(label, (rect.centerx - label.get_width() // 2, rect.centery - label.get_height() // 2))
    return rect.collidepoint(mouse) and click


def end_screen(board, message, draw_board, draw_pieces, play_game, vs_ai):
    while True:
        draw_board()
        draw_pieces(board)
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((200, 200, 200))
        SCREEN.blit(overlay, (0, 0))

        title = BIG_FONT.render(message, True, (0, 0, 0))
        SCREEN.blit(title, (WIDTH // 2 - title.get_width() // 2, 150))

        mx, my = pygame.mouse.get_pos()
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True

        if button("Restart", WIDTH // 2 - 60, 280, (mx, my), click, 120, 50):
            return play_game(vs_ai)
        if button("Quit", WIDTH // 2 - 60, 360, (mx, my), click, 120, 50):
            return False

        pygame.display.update()
