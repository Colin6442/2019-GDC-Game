import pygame, Game_1.chase as gc
pygame.init()

trace = False
reduce = True
run = True
winSize_x = 1700
winSize_y = 900
win = pygame.display.set_mode((winSize_x, winSize_y))
pygame.display.set_caption("First Game")

class player():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.xVel = 0
        self.yVel = 0
player = player(0, 0, 30, 30)

class circles():
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.xVel = 0
        self.yVel = 0

bounce = circles(0, round(winSize_y/2), 50)
chase = circles(round(winSize_x/2), round(winSize_y/2), 4)


def pVelocity():
    #X Velocity
    if player.xVel > 0:
        player.xVel -= 1
    elif player.xVel < 0:
        player.xVel += 1

    #Y Velocity
    if player.yVel > 0:
        player.yVel -= 1
    elif player.yVel < 0:
        player.yVel += 1

def pMove():
    #X Boundaries
    if player.x < 0:
        player.x = 0
        player.xVel = 0
    else:
        player.x += player.xVel

    if player.x > winSize_x - player.width:
        player.x = winSize_x - player.width
        player.xVel = 0
    else:
        player.x += player.xVel

    #Y Boundaries
    if player.y < 0:
        player.y = 0
        player.yVel = 0
    else:
        player.y += player.yVel

    if player.y > winSize_y - player.height:
        player.y = winSize_y - player.height
        player.yVel = 0
    else:
        player.y += player.yVel

def mouseThing(velocity, cap):
    global mousePos
    mousePos = pygame.mouse.get_pos()
    mouseX = mousePos[0]
    mouseY = mousePos[1]
    if bounce.x < mouseX +15:
        bounce.xVel += velocity
        bounce.x += bounce.xVel
    elif bounce.x > mouseX -15:
        bounce.xVel -= velocity
        bounce.x += bounce.xVel

    if bounce.xVel > cap:
        bounce.xVel -= 5
    if bounce.xVel < -cap:
        bounce.xVel += 5

    if bounce.y < mouseY +15:
        bounce.yVel += velocity
        bounce.y += bounce.yVel
    elif bounce.y > mouseY -15:
        bounce.yVel -= velocity
        bounce.y += bounce.yVel


    if bounce.yVel > cap:
        bounce.yVel -= 5
    if bounce.yVel < -cap:
        bounce.yVel += 5

def objectsNstuff():
    fun()
    pygame.draw.rect(win, (255,0,0), (player.x, player.y, player.width, player.height))
    pygame.draw.circle(win, (0,0,0), (chase.x, chase.y), chase.radius)
    pygame.draw.circle(win, (0,20,255), (bounce.x, bounce.y), bounce.radius)
    pygame.draw.line(win, (0,0,0), (mousePos), (bounce.x, bounce.y))
    pygame.display.update()
    clock = pygame.time.Clock()
    clock.tick(30)

def fun():
    if trace == False:
        win.fill((200,200,200))

while run:
    pygame.time.delay(1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.xVel -= 2
    if keys[pygame.K_RIGHT]:
        player.xVel += 2
    if keys[pygame.K_UP]:
        player.yVel -= 2
    if keys[pygame.K_DOWN]:
        player.yVel += 2
    if keys[pygame.K_SPACE]:
        win.fill((200,200,200))
    if keys[pygame.K_z]:
        if trace == False:
            trace = True
        else:
            trace = False
    if keys[pygame.K_x]:
        if reduce == False:
            reduce = True
        else:
            reduce = False

    mouseThing(5,50)
    pVelocity()
    pMove()
    if reduce == True:
        chase.xVel, chase.yVel = gc.cVelocity(chase.xVel, chase.yVel)
    player.x, player.y, chase.x, chase.y, chase.xVel, chase.yVel = gc.cMove(5, 50, player.x, player.y, chase.x, chase.y, chase.xVel, chase.yVel)
    objectsNstuff()

pygame.quit()