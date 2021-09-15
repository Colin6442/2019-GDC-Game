import pygame, numpy as np, random, time, keyboard
pygame.init()
mainRun = True
optionRun = False
winSize_x = 1700
winSize_y = 900
wallHeight = 300
wallWidth = 300

fire1 = pygame.mixer.Sound("fire1.wav")
fire2 = pygame.mixer.Sound("fire2.wav")
music = pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(-1)
sansTitle = pygame.font.SysFont('Comic Sans MS', 50)
sansTxt = pygame.font.SysFont('Comic Sans MS', 24)

scoreTxt = None

title = pygame.image.load("Title.png")
char = pygame.image.load("Shielder2.png")
enemyFire = pygame.image.load("Fireball_up.gif")
playerFire = pygame.image.load("Blue_Fire_up.gif")
enemyImg = pygame.image.load("Wizard.gif")
heartPNG = pygame.image.load("heart.png")
inactiveSheild = pygame.image.load("Radial_Shield.gif")
brokenSheild = pygame.image.load("Broken_Shield.gif")
activeSheild = pygame.image.load("Blue_Shield.gif")

pygame.display.set_caption("Shield Man GDC Game")


win = pygame.display.set_mode((winSize_x, winSize_y))


highscore = 0

def getHighScore():
    global highscore
    highscoretxt = open("highscore.txt", "r")
    output = highscoretxt.read()
    return(output)

highscore = getHighScore()

def setHighScore(input):
    global highscore
    if str(input) > str(highscore):
        highscoretxt = open("highscore.txt", "w")
        highscoretxt.write(str(input))
        highscoretxt.close()

def BoxMaker(color, x, y, width, height):
    pygame.draw.rect(win, color, (x, y, width, height))

def TextBox(var, textType, message, color, x, y):
    var = textType.render(message, True, color)
    win.blit(var, (x, y))

    '''
    scoreTxt = sansTxt.render("Score: " + str(score), True, (0, 0, 0))
    win.blit(scoreTxt, ((10 * winSize_x) / 11, 10))
    '''

def slider():
    None

def OptionScreen(clockSpeed):
    global run, timer, enemies, playerHealth, enemyCoords, enemyNum, tick, bullets, clicking, timeout, waitTimer, end, hearts, score, mouseX, mouseY, blocked, runTitle, mainRun, optionRun
    while optionRun:
        win.fill((150, 150, 150))
        xButton()
        onion = None
        back = None
        mousePos, mouseX, mouseY = mouse()
        click = pygame.mouse.get_pressed()
        TextBox(onion, sansTitle, "These are not the options you are looking for", (0,0,0), winSize_x/2 - 500, winSize_y/2)
        BoxMaker((255,255,255), winSize_x/2 - 150, winSize_y/2 + 100, 300, 100)
        TextBox(back, sansTitle, "Back", (0,0,0), winSize_x/2 - 60, winSize_y/2 + 110)
        if checkHitBox(mouseX, mouseY, 1, 1, winSize_x/2 - 150, winSize_y/2 + 100, 300, 100, 0) and click[0]:
            time.sleep(.2)
            optionRun = False
            break

        pygame.display.update()
        clock = pygame.time.Clock()
        pygame.time.delay(1)
        clock.tick(clockSpeed)

def TitleScreen(clockSpeed):
    global run, timer, enemies, playerHealth, enemyCoords, enemyNum, tick, bullets, clicking, timeout, waitTimer, end, hearts, score, mouseX, mouseY, blocked, runTitle, mainRun, optionRun
    while runTitle:
        #win.fill((150,150,150))
        win.blit(title, (0,0))
        xButton()
        mousePos, mouseX, mouseY = mouse()
        click = pygame.mouse.get_pressed()
        play = None
        options = None
        hstxt = None
        highscore = getHighScore()
        BoxMaker((255,255,255),winSize_x/2 - 170, winSize_y/2 +260, 300, 100)
        TextBox(hstxt, sansTxt, "Highscore: "+highscore, (0,0,0), winSize_x/2 - 90, winSize_y/2 + 290)
        BoxMaker((250, 250, 250), winSize_x/2 - 165, winSize_y/2 - 50, 300, 100)
        TextBox(play, sansTitle, "Play Game", (0,0,0), winSize_x/2 - 130, winSize_y/2 - 40)
        if checkHitBox(mouseX, mouseY, 1, 1, winSize_x/2 - 165, winSize_y/2 - 50, 300, 100, 0) and click[0]:
            time.sleep(.2)
            run = True
            break
        BoxMaker((250, 250, 250), winSize_x/2 - 165, winSize_y/2 + 100, 300, 100)
        TextBox(options, sansTitle, "Options", (0,0,0), winSize_x/2 - 130, winSize_y/2 + 110)
        if checkHitBox(mouseX, mouseY, 1, 1, winSize_x/2 - 165, winSize_y/2 + 100, 300, 100, 0) and click[0]:
            time.sleep(.2)
            optionRun = True
            break


        pygame.display.update()
        clock = pygame.time.Clock()
        pygame.time.delay(1)
        clock.tick(clockSpeed)





def changeRes(size, winSize_x, winSize_y, no):
    if no:
        winSize_x = size[0]
        winSize_y = size[1]
        win = pygame.display.set_mode((winSize_x, winSize_y))
        no = False
    return(winSize_x, winSize_y, no)

class entity():
    def __init__(self, x, y, width, height, alpha):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.xVel = 0
        self.yVel = 0
        self.alpha = alpha
    def draw(self):
        pygame.draw.rect(win, (255, 0, 0), (self.x, self.y, 40, 40), self.alpha)

player = entity(100, round(winSize_y/2), 40, 40, 0)

class projectile():
    def __init__(self, x, y, xComp, yComp, lethal):
        self.x = x
        self.y = y
        self.xVel = xComp
        self.yVel = yComp
        self.xAccel = 0
        self.yAccel = 0
        self.bounce = 0
        self.radius = 10
        self.lethal = lethal
        self.alpha = 1
    def draw(self, color):
        pygame.draw.circle(win, color, (self.x,self.y), self.radius, self.alpha)

class heart():
    def __init__(self, x, y, grab):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.grab = True
    def draw(self):
        pygame.draw.rect(win, (255, 0, 0), (self.x, self.y, self.width, self.height))

class shield():
    def __init__(self, x, y, on):
        self.x = player.x
        self.y = player.y
        self.width = 20
        self.height = 20
        self.on = on
    def draw(self, color):
        pygame.draw.rect(win, (color), (self.x, self.y, self.width, self.height))
shieldObj = shield(player.x + player.width + 5, player.y + player.height + 10, False)

class wallObject():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = wallWidth
        self.height = wallHeight
    def draw(self):
        pygame.draw.rect(win, (0, 0, 0), (self.x, self.y, self.width, self.height))

def mouse():
    mousePos = pygame.mouse.get_pos()
    mouseX = mousePos[0]
    mouseY = mousePos[1]
    return (mousePos, mouseX, mouseY)

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

def pVelocity():
    #X Velocity
    if player.xVel != 0:
        player.xVel = player.xVel/1.5

    #Y Velocity
    if player.yVel != 0:
        player.yVel = player.yVel/1.5

def playerControls(playerSpeed):
    global menu
    if menu == False:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.xVel -= playerSpeed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.xVel += playerSpeed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player.yVel -= playerSpeed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player.yVel += playerSpeed

    'Menu'
    if menu == False:
        if keyboard.is_pressed("esc"):
            time.sleep(.2)
            menu = True

    while menu == True:
        global run, timer, enemies, playerHealth, enemyCoords, enemyNum, tick, bullets, clicking, timeout, waitTimer, end, hearts, score, mouseX, mouseY, blocked, runTitle, mainRun, optionRun
        win.fill((200, 200, 200))
        xButton()
        text1 = sansTitle.render("Menu", True, (0, 0, 0))
        win.blit(text1, (winSize_x / 2 - 70, winSize_y / 2 - 300))
        mousePos, mouseX, mouseY = mouse()
        click = pygame.mouse.get_pressed()

        BoxMaker((255,255,255), winSize_x / 2 - 150, winSize_y / 2 - 100, 300, 100)
        back = None
        TextBox(back, sansTitle, "Resume", (0,0,0), winSize_x/2-90, winSize_y/2-90)
        if checkHitBox(mouseX, mouseY, 1, 1, winSize_x / 2 - 90, winSize_y / 2 -90, 300, 100, 0) and click[0]:
            time.sleep(.2)
            menu = False
            break

        BoxMaker((255,255,255), winSize_x / 2 - 150, winSize_y / 2 + 100, 300, 100)
        quit = None
        TextBox(quit, sansTitle, "Quit", (0,0,0), winSize_x/2-50, winSize_y/2+110)
        if checkHitBox(mouseX, mouseY, 1, 1, winSize_x / 2 - 50, winSize_y / 2 +110, 300, 100, 0) and click[0]:
            time.sleep(.2)
            menu = False
            runTitle = True
            run = False
            optionRun = False
            break

        pygame.display.update()
        if keyboard.is_pressed("esc"):
            time.sleep(.2)
            menu = False

def chargeDisp():
    pygame.draw.rect(win, (255,0,0), (15, winSize_y - 40, 400, 20))
    if (waitTimer == 0):
        pygame.draw.rect(win, (0,255,0), (15, winSize_y - 40, (400-(10*clicking)), 20))


def drawshieldObj(color):
    xDist = mouseX - player.x
    yDist = mouseY - player.y
    desiredDist = 50

    if xDist != 0 and xDist > 0:
        theta = np.arctan(yDist / xDist)
        adj = int(round( desiredDist * np.cos(theta) ))
        opp = int(round( desiredDist * np.sin(theta) ))

    elif xDist != 0 and xDist < 0:
        theta = np.arctan(yDist / xDist)
        adj = -int(round( desiredDist * np.cos(theta) ))
        opp = -int(round( desiredDist * np.sin(theta) ))
    elif xDist == 0 and yDist < 0:
        adj = 0
        opp = -desiredDist
    else:
        adj = 0
        opp = desiredDist

    shieldObj.x = player.x + (player.width/2) + adj - (shieldObj.width/2)
    shieldObj.y = player.y + (player.height/2) + opp - (shieldObj.height/2)

    #shieldObj.draw(color)

def clickNshoot(c_bulletSpeed, timeout):
    click = pygame.mouse.get_pressed()
    reflect = False
    if(click[0] and timeout == False):
        reflect = True
        try:
            if(blocked == True):
                xComp, yComp = trajectory(c_bulletSpeed, reflect)
                bullets.append(projectile(player.x + (player.width/2), player.y + (player.height / 2), xComp, yComp, False))
        except: None
    return(reflect)

def timedout(timeout, clicking, waitTimer):
    click = pygame.mouse.get_pressed()
    if (click[0] and timeout == False):
        clicking += 1
    if clicking > 40:
        timeout = True
        clicking = 0
    if timeout == True:
        waitTimer += 1
    if waitTimer > 120:
        timeout = False
        waitTimer = 0
    if clicking > 0:
        clicking -= 0.1

    return(timeout, clicking, waitTimer)

def trajectory(bulletSpeed, reflect):
    xComp = (mouseX - player.x -15)
    yComp = (mouseY - player.y -15)
    speed = bulletSpeed

    if xComp != 0 and xComp < 0:
        theta = np.arctan(yComp / xComp)
        adj = int(round( speed * np.cos(theta) ))
        opp = int(round( speed * np.sin(theta) ))

    elif xComp != 0 and xComp > 0:
        theta = np.arctan(yComp / xComp)
        adj = -int(round( speed * np.cos(theta) ))
        opp = -int(round( speed * np.sin(theta) ))
    elif xComp == 0 and yComp > 0:
        adj = 0
        opp = -speed
    else:
        adj = 0
        opp = speed

    ''' *Set Bullet Max*
    if len(bullets) < numBulletsAllowed:
        bullets.append(projectile(player.x + player.width/2+50, player.y + player.height/2, adj, opp))'''

    return (adj, opp)

def spawnEnemy(numEnemies):
    enemies = []
    for x in range(numEnemies):
        enemies.append(entity(random.randint(winSize_x-600,winSize_x-50),random.randint(100,winSize_y-100),40,40, 0))
    return enemies

def enemyBullets(enemyX, enemyY):
    xComp = player.x - enemyX
    yComp = player.y - enemyY
    speed = 5
    if xComp != 0 and xComp < 0:
        theta = np.arctan(yComp / xComp)
        adj = int(round( speed * np.cos(theta) ))
        opp = int(round( speed * np.sin(theta) ))

    elif xComp != 0 and xComp > 0:
        theta = np.arctan(yComp / xComp)
        adj = -int(round( speed * np.cos(theta) ))
        opp = -int(round( speed * np.sin(theta) ))
    elif xComp == 0 and yComp > 0:
        adj = 0
        opp = -speed
    else:
        adj = 0
        opp = speed

    bullets.append(projectile(enemyX + 20, enemyY + 20, adj, opp, True))

def reflectBullets(reflect):
    blocked = False
    if reflect == True:
        for bullet in bullets:
            if bullet.x + bullet.radius > shieldObj.x - 20 and bullet.x + bullet.radius < shieldObj.x + shieldObj.width + 20:
                if bullet.y + bullet.radius > shieldObj.y -20 and bullet.y + bullet.radius < shieldObj.y + shieldObj.height + 20:
                    if bullet.lethal == True:
                        blocked = True
                        bullets.pop(bullets.index(bullet))
                        clickNshoot(5, timeout)
    return(blocked)

def moveEnemies(enemyCoords, enemyNum):
    for enemy in enemies:
        enemy.xVel = 5
        enemy.yVel = 5

        if enemy.x > winSize_x - enemy.width:
            enemy.x -= enemy.xVel

        elif enemy.x < 0:
            enemy.x += enemy.xVel

        else:
            enemy.x += random.randint(-10, 10)

        if enemy.y > winSize_y - enemy.height:
            enemy.y -= enemy.yVel

        elif enemy.y < 0:
            enemy.y += enemy.yVel

        else:
            enemy.y += random.randint(-10, 10)

        enemyCoords = np.append(enemyCoords, [[enemy.x],[enemy.y]], axis = 1)

    return(enemyCoords)

def pHealth(playerHealth):
    if playerHealth == 3:
        #pygame.draw.rect(win, (200, 0, 0), (100, 20, 30, 30))
        win.blit(heartPNG, (100, 20))
    if playerHealth >= 2:
        #pygame.draw.rect(win, (200, 0, 0), (60, 20, 30, 30))
        win.blit(heartPNG, (60, 20))
    if playerHealth >= 1:
        #pygame.draw.rect(win, (200, 0, 0), (20, 20, 30, 30))
        win.blit(heartPNG, (20, 20))

def doBullets(numBounces, createWalls, bullets, enemies, playerHealth, tick, timer, clicking, timeout, waitTimer, end, hearts, enemyNum, score):
    global highscore
    for bullet in bullets:
        try:
            bulletIndex = bullets.index(bullet)
        except:
            None
        if bullet.x < winSize_x and bullet.x > 0 and bullet.y < winSize_y and bullet.y > 0:
            bullet.x -= bullet.xVel
            bullet.y -= bullet.yVel
        else:
            if bullet.bounce <= numBounces - 1:
                if bullet.x >= winSize_x or bullet.x <= 0:
                    bullet.xVel = -bullet.xVel
                if bullet.y >= winSize_y -50 or bullet.y <= 50:
                    bullet.yVel = -bullet.yVel
                bullet.x -= bullet.xVel
                bullet.y -= bullet.yVel
                bullet.bounce += 1
            else:
                try:
                    bullets.pop(bullets.index(bullet))
                except:
                    None


        if (bullet.lethal == True):
            if bullet.x + bullet.radius > player.x and bullet.x + bullet.radius < player.x + player.width + 16:
                if bullet.y + bullet.radius > player.y and bullet.y + bullet.radius < player.y + player.height + 16:
                    playerHit()
                    try:
                        bullets.pop(bullets.index(bullet))
                    except:
                        True
                    playerHealth -= 1
                    if playerHealth < 1:
                        setHighScore(score)
                        bullets, enemies, clicking, timeout, waitTimer, playerHealth, tick, timer, player.x, player.y, end, hearts, enemyNum, score = reset(bullets, enemies, clicking, timeout, waitTimer, playerHealth, tick, timer, player.x, player.y, end, hearts, enemyNum, score)

        elif (bullet.lethal == False):
            for enemy in enemies:
                if bullet.x + bullet.radius > enemy.x and bullet.x + bullet.radius < enemy.x + enemy.width + 10:
                    if bullet.y + bullet.radius > enemy.y and bullet.y + bullet.radius < enemy.y + enemy.height + 10:
                        score += 1
                        chance = .3
                        randomNum = random.random()
                        enemies.pop(enemies.index(enemy))
                        if (randomNum < chance):
                            hearts.append(heart(enemy.x, enemy.y, True))


        if (createWalls == True):
            for wall in walls:
                if bullet.bounce <= numBounces - 1:
                    if bullet.x > wall.x and bullet.x < wall.x + wall.width and bullet.y > wall.y and bullet.y < wall.y + wall.height:
                        if (bullet.y > wall.y and bullet.y < wall.y + wall.height) and ((bullet.x > wall.x and bullet.x < wall.x + 20) or (bullet.x > wall.x + wall.width - 20 and bullet.x < wall.x + wall.width)):
                            bullet.xVel = -bullet.xVel
                            bullet.bounce +=1
                        elif (bullet.x > wall.x and bullet.x < wall.x + wall.width) and ((bullet.y > wall.y and bullet.y < wall.y + 20) or (bullet.y > wall.y + wall.height - 20 and bullet.y < wall.y + wall.height)):
                            bullet.yVel = -bullet.yVel
                            bullet.bounce += 1
                        else:
                            bullets.pop(bulletIndex)


    return(bullets, enemies, playerHealth, tick, timer, player.x, player.y, clicking, timeout, waitTimer, end, hearts, enemyNum, score)

def makeWalls():
        walls.append(wallObject(0, 0))
        walls.append(wallObject(0, winSize_y - wallHeight))
        walls.append(wallObject(winSize_x - wallWidth, 0))
        walls.append(wallObject(winSize_x - wallHeight, winSize_y - wallHeight))

def endGame():
    if (end == True):
        if(checkHitBox(player.x, player.y, player.width, player.height, winSize_x - 20, winSize_y / 2 - 100, 25, 200, 10) == True):
            return (True)

def checkHitBox(x1, y1, width1, height1, x2, y2, width2, height2, extra):
    if (y1 < y2 + height2 + extra and y1 > y2) or (y1 + height1 > y2 and y1 + height1 < y2 + height2):
        if (x1 < x2 + width2 + extra and x1 > x2) or (x1 + width1 > x2 and x1 + width1 < x2 + width2):
            return True

def getHealth(playerHealth):
    for item in hearts:
        if checkHitBox(player.x, player.y, player.height, player.width, item.x, item.y, item.width, item.height, 0):
            if playerHealth < 3:
                playerHealth += 1
                hearts.pop(hearts.index(item))
    return(playerHealth)

def render(clockSpeed, createWalls, pColor, timeout, dColor):
    #win.blit(bg, (0, 0))
    #pygame.draw.rect(win, (pColor), (player.x, player.y, player.width, player.height), player.alpha)

    #char = pygame.transform.rotate(char, 5)
    win.blit(char, (player.x, player.y))

    TextBox(scoreTxt, sansTxt, "Score: " + str(score), (0, 0, 0), (10 * winSize_x) / 11, 10)

    "Door"
    pygame.draw.rect(win, (dColor), (winSize_x - 20, winSize_y / 2 - 100, 20, 200))
    "Door"
    
    chargeDisp()
    
    pHealth(playerHealth)

    for item in hearts:
        win.blit(heartPNG, (item.x, item.y))


    if reflect == True:
        drawshieldObj((0,150,0))
        win.blit(activeSheild, (shieldObj.x - 10, shieldObj.y - 10))
    elif reflect == False and timeout != True:
        drawshieldObj((0,0,0))
        win.blit(inactiveSheild, (shieldObj.x - 10, shieldObj.y - 10))
    if timeout == True:
        drawshieldObj((150,0,0))
        win.blit(brokenSheild, (shieldObj.x - 10, shieldObj.y - 10))
    for bullet in bullets:
        bullet.x = int(bullet.x)
        bullet.y = int(bullet.y)
        if bullet.lethal == True:
            #bullet.draw((150,0,0))
            win.blit(enemyFire, (bullet.x - 15, bullet.y - 20))
        else:
            #bullet.draw((0,150,0))
            win.blit(playerFire, (bullet.x - 15, bullet.y - 20))
    for enemy in enemies:
        #enemy.draw()
        win.blit(enemyImg, (enemy.x, enemy.y))

    if createWalls == True:
        for wall in walls:
            wall.draw()

    pygame.display.update()
    clock = pygame.time.Clock()
    clock.tick(clockSpeed)

ticking = 0

def playerHit():
    win.fill((196, 45, 45))
    pygame.display.update()
    time.sleep(.1)

def notConstant(tick, num, enemyCoords, enemyNum, timer):
    if tick == num - 30:
        if enemies != []:
            fire2.play()
    if tick > num:
        tick = 0
        for x in range(enemyNum):
            try:
                enemyX = enemyCoords[0][x]
                enemyY = enemyCoords[1][x]
                enemyBullets(enemyX, enemyY)
            except:
                None
    else:
        tick += 1
    return tick

def reset(bullets, enemies, clicking, timeout, waitTimer, playerHealth, tick, timer, playerX, playerY, end, hearts, enemyNum, score):
    bullets = []
    enemies = []
    hearts = []
    clicking = 0
    timeout = False
    waitTimer = 0
    playerHealth = 3
    tick = 0
    timer = 0
    playerX= 100
    playerY = round(winSize_y/2)
    enemyNum = 1
    score = 0
    enemies = spawnEnemy(enemyNum)
    end = False
    return(bullets, enemies, clicking, timeout, waitTimer, playerHealth, tick, timer, playerX, playerY, end, hearts, enemyNum, score)

def xButton():
    global run, runTitle, mainRun, optionRun
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            runTitle = False
            mainRun = False
            optionRun = False


enemyCoords = np.array([ [], [] ], np.int32)
hearts = []
bullets = []
enemies = []
clicking = 0
timeout = False
waitTimer = 0
playerHealth = 3
enemyNum = 1
score = 0
pColor = 0, 0, 255
dColor = 0, 0, 0
runTitle = True
run = False
menu = False
createWalls = False
reflect = False
tick = 0
no = True
end = False
if createWalls == True:
    walls = []
    makeWalls()

Title = True

enemies = spawnEnemy(enemyNum)

timer = 0
def main():
    global run, timer, enemies, playerHealth, enemyCoords, enemyNum, tick, bullets, clicking, timeout, waitTimer, end, hearts, score, mouseX, mouseY, blocked, reflect, mainRun, runTitle
    while run:
        win.fill((150, 150, 150))
        #win.blit(bg, (0,0))
        pygame.time.delay(1)
        timer += 1

        if enemies == []:
            end = True
            dColor = (200, 200, 200)
        else:
            dColor = (0, 0, 0)

        xButton()

        setHighScore(score)

        playerHealth = getHealth(playerHealth)

        #winSize_x, winSize_y, no = changeRes((1280,720), winSize_x, winSize_y, no)

        enemyCoords = moveEnemies(enemyCoords, enemyNum)

        tick = notConstant(tick, 100, enemyCoords, enemyNum, timer)

        enemyCoords = np.array([[], []], np.int32)

        bullets, enemies, playerHealth, tick, timer, player.x, player.y, clicking, timeout, waitTimer, end, hearts, enemyNum, score = doBullets(2, createWalls, bullets, enemies, playerHealth, tick, timer, clicking, timeout, waitTimer, end, hearts, enemyNum, score)

        timeout, clicking, waitTimer = timedout(timeout, clicking, waitTimer)

        reflect = clickNshoot(5, timeout)#  -  -  -  -  #(ballSpeed, numBalls)

        blocked = reflectBullets(reflect)

        playerControls(1.01)#  -  -  -  -  -  -  -  #(playerSpeed)

        pMove()

        pVelocity()

        mousePos, mouseX, mouseY = mouse()

        render(120, createWalls, pColor, timeout, dColor)#  -  -  -  -  -  -  -  #(clock tick speed)

        dummy = 0

        if endGame() == True:
            enemyNum += 1
            enemies = spawnEnemy(enemyNum)
            bullets, dummy, clicking, timeout, waitTimer, dummy, tick, timer, player.x, player.y, end, hearts, dummy, dummy = reset(bullets, enemies, clicking, timeout, waitTimer, playerHealth, tick, timer, player.x, player.y, end, hearts, enemyNum, score)


while mainRun:
    TitleScreen(120)
    OptionScreen(120)
    main()

pygame.quit()
