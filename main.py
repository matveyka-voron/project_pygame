import pygame, random, sys
from pygame.locals import *

WINDOWWIDTH = 600
WINDOWHEIGHT = 600
TEXTCOLOR = (0, 0, 0)
BACKGROUNDCOLOR = (255, 255, 255)
FPS = 60
BADDIEMINSIZE = 10
BADDIEMAXSIZE = 40
BADDIEMINSPEED = 1
BADDIEMAXSPEED = 8
ADDNEWBADDIERATE = 6
PLAYERMOVERATE = 5

def terminate():
    pygame.quit()
    sys.exit()

def waitforplayertopresskey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCACE: #Нажатие ESC - происходит выход.
                    terminate()
                return

def playerhashitbaddie(player_rect, baddies, b=None):
    for i in baddies:
        if player_rect.colliderect(i['rect']):
            return True
    return False

def draw_text(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Инициализация pygame и настройка окна
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Ловкач')
pygame.mouse.set_visible(False)

# Настройка шрифтов
font = pygame.font.SysFont(None, 35)

# Настройка звуков
gameOverSound = pygame.mixer.Sound('gameover.wav')
pygame.mixer.music.load('background.mid')

# Настройка изображений
playerImage = pygame.image.load('player.png')
playerRect = playerImage.get_rect()
baddieImage = pygame.image.load('baddie.png')

# Вывод начального экрана
windowSurface.fill(BACKGROUNDCOLOR)
draw_text('Ловкач', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
draw_text('Нажмите любую клавишу для начала игры', font, windowSurface, (WINDOWWIDTH / 5) - 30, (WINDOWHEIGHT / 3) + 50)
pygame.display.update()
waitforplayertopresskey()

topScore = 0
while True:
    #Настройка начала игры
    baddies = []
    score = 0
    playerRect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    baddieAddCounter = 0
    pygame.mixer.music.play(-1, 0.0)

    while True: # Игровой цикл будет выполнятся, пока происходит процесс игры
        score += 1 # Прибавление количества очков

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event == K_z:
                    reverseCheat = True
                if event.key == K_x:
                    slowCheat = True
                if event.key == K_LEFT or event.key == K_a:
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == K_d:
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP or event.key == K_w:
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == K_s:
                    moveUp = False
                    moveDown = True

            if event.type == KEYUP:
                if event.key == K_z:
                    reverseCheat = False
                    score = 0
                if event.key == K_x:
                    slowCheat = False
                    score = 0
                if event.key == K_ESCAPE:
                    terminate()

                if event.key == K_LEFT or event.key == K_a:
                    moveLeft = False
                if event.key == K_RIGHT or event.key == K_d:
                    moveRight = False
                if event.key == K_UP or event.key == K_w:
                    moveUp = False
                if event.key == K_DOWN or event.key == K_s:
                    moveDown = False

            if event.type == MOUSEMOTION:
                # Перемещение игрока на курсор мыши [в движении курсора]
                playerRect.centerx = event.pos[0]
                playerRect.centery = event.pos[1]
        # Если необходим, то добавить новых злодеев в верхнюю часть экрана
        if not reverseCheat and not slowCheat:
            baddieAddCounter += 1
        if baddieAddCounter == ADDNEWBADDIERATE:
            baddieAddCounter = 0
            baddieSize = random.randint(BADDIEMINSIZE, BADDIEMAXSIZE)
    newBaddie = {'rect' : pygame.Rect(random.randint(0, WINDOWWIDTH - baddieSize), 0 - baddieSize, baddieSize, baddieSize),
                 'speed' : random.randint(BADDIEMINSPEED, BADDIEMAXSPEED),
                 'surface' : pygame.transform.scale(baddieImage, (baddieSize, baddieSize)),
                 }

            baddies.append(newBaddie)

    # Перемещение игрока по дисплею
    if moveLeft and playerRect.left > 0:
        playerRect.move_ip(-1 * PLAYERMOVERATE, 0)
    if moveRight and playerRect.right < WINDOWWIDTH:
        playerRect.move_ip(PLAYERMOVERATE, 0)
    if moveUp and playerRect.top > 0:
        playerRect.move_ip(0, -1 * PLAYERMOVERATE)
    if moveDown and playerRect.bottom < WINDOWHEIGHT:
        playerRect.move_ip(0, PLAYERMOVERATE)

    # Спуск злодеев вниз
    for i in baddies:
        if not reverseCheat and not slowCheat:
            i['rect'].move_ip(0, i['speed'])
        elif reverseCheat:
            i['rect'].move_ip(0, -5)
        elif slowCheat:
            i['rect'].move_ip(0, 1)

    # Уничтожение злоеев, проникших ниже границы дисплея
    for i in baddies[:]:
        if i['rect'].top > WINDOWHEIGHT:
            baddies.remove(i)