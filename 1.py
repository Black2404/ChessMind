import pygame
import random
import sys

pygame.init()

# ===== MÀU SẮC =====
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
gray = (200, 200, 200)

# ===== HÌNH ẢNH XE =====
carImg = pygame.image.load('6.jpg')

# ===== KÍCH THƯỚC MÀN HÌNH =====
display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Dodge Game')

clock = pygame.time.Clock()
car_width = 73

# ===== HÀM HIỂN THỊ TEXT =====
def text_objects(text, font, color=black):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

# ===== HÀM VẼ XE =====
def car(x, y):
    gameDisplay.blit(carImg, (x, y))

# ===== VẼ CHƯỚNG NGẠI VẬT =====
def things(thingx, thingy, thingw, thingh, color):
    pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])

# ===== HIỂN THỊ ĐIỂM =====
def things_dodged(count):
    font = pygame.font.SysFont(None, 35)
    text = font.render("Dodged: " + str(count), True, black)
    gameDisplay.blit(text, (0, 0))

# ===== THOÁT GAME =====
def quit_game():
    pygame.quit()
    sys.exit()

# ===== NÚT BẤM =====
def button(msg, x, y, w, h, ic, ac, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Nếu trỏ chuột nằm trên nút
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))

    smallText = pygame.font.Font("freesansbold.ttf", 30)
    textSurf, textRect = text_objects(msg, smallText, black)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    gameDisplay.blit(textSurf, textRect)

# ===== MÀN HÌNH INTRO =====
def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

        gameDisplay.fill(white)
        largeText = pygame.font.Font('freesansbold.ttf', 90)
        TextSurf, TextRect = text_objects("Dodge Game", largeText, blue)
        TextRect.center = ((display_width / 2), (display_height / 2) - 100)
        gameDisplay.blit(TextSurf, TextRect)

        # Nút Start và Quit
        button("Start", 150, 450, 150, 60, green, gray, game_loop)
        button("Quit", 500, 450, 150, 60, red, gray, quit_game)

        pygame.display.update()
        clock.tick(15)

# ===== VA CHẠM =====
def crash():
    largeText = pygame.font.Font('freesansbold.ttf', 75)
    TextSurf, TextRect = text_objects("You Crashed!", largeText, red)
    TextRect.center = ((display_width / 2), (display_height / 2))
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()
    pygame.time.wait(2000)
    game_intro()  # Quay lại intro sau khi crash

# ===== GAME LOOP =====
def game_loop():
    x = display_width * 0.45
    y = display_height * 0.8
    x_change = 0

    thing_startx = random.randrange(0, display_width)
    thing_starty = -600
    thing_speed = 7
    thing_width = 100
    thing_height = 100

    dodged = 0
    gameExit = False

    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                elif event.key == pygame.K_RIGHT:
                    x_change = 5
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0

        x += x_change
        gameDisplay.fill(white)

        # Chướng ngại vật
        things(thing_startx, thing_starty, thing_width, thing_height, black)
        thing_starty += thing_speed

        # Vẽ xe và điểm
        car(x, y)
        things_dodged(dodged)

        # Kiểm tra biên
        if x > display_width - car_width or x < 0:
            crash()

        # Reset vật thể sau khi rơi xuống
        if thing_starty > display_height:
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(0, display_width)
            dodged += 1
            thing_speed += 0.5
            thing_width += (dodged * 0.3)

        # Kiểm tra va chạm
        if y < thing_starty + thing_height:
            if (x > thing_startx and x < thing_startx + thing_width) or \
               (x + car_width > thing_startx and x + car_width < thing_startx + thing_width):
                crash()

        pygame.display.update()
        clock.tick(60)

# ===== CHẠY GAME =====
game_intro()
