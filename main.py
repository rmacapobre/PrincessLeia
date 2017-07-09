try:
    import pygame_sdl2
    pygame_sdl2.import_as_pygame()
except ImportError:
    pass

import pygame
import glob
import math
import random

class Ewok:
    def __init__(self, startx, starty, number = -1):
        self.x = startx
        self.y = starty
        self.angle = 0
        self.direction = pygame.K_DOWN
        self.saved = False
        self.missed = False
        if (number == -1):
            number = random.randint(0, 4)
        if (number == 0): self.img =  pygame.image.load("images/ewok1.png")
        elif (number == 1): self.img = pygame.image.load("images/ewok2.png")
        elif (number == 2): self.img = pygame.image.load("images/ewok3.png")
        else: self.img =  pygame.image.load("images/ewok4.png")
        self.type = number

    def move(self):
        number = random.randint(0, 9)
        if (number == 0): self.x -= 5
        if (number == 1): self.x -= 10
        if (number == 2): self.x += 5
        if (number == 3): self.x += 10
        if (number == 4): self.x -= 2
        if (number == 5): self.x -= 7
        if (number == 6): self.x += 2
        if (number == 7): self.x += 7
        self.y += 5
        if (self.y == 350):
            self.y = 60
            if (not self.saved):
                self.missed = True
            self.saved = False

    def display(self, screen):
        pos = (self.x, self.y)
        rotatedSurface = pygame.transform.rotate(self.img, self.angle)
        screen.blit(rotatedSurface, pos)
        number = random.randint(0, 9)
        if (number == 1 or number == 5):
            self.angle += 45

class EwokTower:
    def __init__(self):
        self.list = []
        self.reachDS = 0
        self.win = False
    def add(self, ewok):
        count = len(self.list)
        if count == 0:
            ewok.x = 240
            ewok.y = 350
            self.list.insert(0, ewok)
        else:
            ewok.y = self.list[0].y - 15
            if (ewok.y >= 70):
                ewok.x = 240
                self.list.insert(0, ewok)
            else:
                ewok.x += self.reachDS
                if (ewok.x <= 410):
                    self.reachDS += 15
                    self.list.append(ewok)
                elif (ewok.x > 410):
                    self.win = True


class Person:
    def __init__(self, startx, starty, name):
        self.x = startx
        self.y = starty
        self.current = 1
        self.direction = pygame.K_SPACE

        # Get list of filenames
        self.frontNames = sorted(glob.glob("images/" + name + "Front*.png"))
        self.backNames = sorted(glob.glob("images/" + name + "Back*.png"))
        self.leftNames = sorted(glob.glob("images/" + name + "Left*.png"))
        self.rightNames = sorted(glob.glob("images/" + name + "Right*.png"))

        # load images
        self.front = []
        self.back = []
        self.left = []
        self.right = []
        for item in self.frontNames: self.front.append(pygame.image.load(item))
        for item in self.backNames: self.back.append(pygame.image.load(item))
        for item in self.leftNames: self.left.append(pygame.image.load(item))
        for item in self.rightNames: self.right.append(pygame.image.load(item))

    def display(self, screen):
        pos = (self.x, self.y)
        if (self.direction == pygame.K_DOWN or self.direction == pygame.K_SPACE):
            if (not self.front): return
            screen.blit(self.front[self.current-1], pos)
        if (self.direction == pygame.K_UP):
            if (not self.back): return
            screen.blit(self.back[self.current-1], pos)
        if (self.direction == pygame.K_LEFT):
            if (not self.left): return
            screen.blit(self.left[self.current-1], pos)
        if (self.direction == pygame.K_RIGHT):
            if (not self.right): return
            screen.blit(self.right[self.current-1], pos)
        self.current += 1
        if (self.current == 5): self.current = 1

    def move(self):
        if (self.direction == pygame.K_DOWN): self.y += 5
        if (self.direction == pygame.K_UP): self.y -= 5
        if (self.direction == pygame.K_LEFT): self.x -= 10
        if (self.direction == pygame.K_RIGHT): self.x += 10
        # Define limits for Princess Leia
        if self.x <= 10: self.x = 10
        if self.x >= 450: self.x = 450
        if self.y <= 330: self.y = 340
        if self.y >= 340: self.y = 340

    def shift(self):
        if (self.direction == pygame.K_LEFT): self.x -= 1
        if (self.direction == pygame.K_RIGHT): self.x += 1
        # Define limits for Darth Sidious
        if self.x < 325: self.direction = pygame.K_RIGHT
        if self.x > 400: self.direction = pygame.K_LEFT

    def fall(self):
        if (self.y >= 340): return
        self.direction = pygame.K_DOWN
        number = random.randint(0, 9)
        if (number == 0): self.x -= 5
        if (number == 1): self.x -= 10
        if (number == 2): self.x += 5
        if (number == 3): self.x += 10
        if (number == 4): self.x -= 2
        if (number == 5): self.x -= 7
        if (number == 6): self.x += 2
        if (number == 7): self.x += 7
        self.y += 15

# Entry point

pygame.init()
screen = pygame.display.set_mode((500, 400))
pygame.display.set_caption("Princesse Leia")

black = (0, 0, 0)
white = (255, 255, 255)
yellow = (255, 255, 0)
clock = pygame.time.Clock()

pygame.font.init()
verdana = pygame.font.SysFont('Verdana', 15)
arial = pygame.font.SysFont('Arial', 15)

mf = pygame.image.load("images/mf.jpg")
mf = pygame.transform.scale(mf, (500, 400))

darthSidius = Person(350, 60, "ds")
darthSidius.direction = pygame.K_LEFT
princesseLeia = Person(10, 350, "leia")

fallingEwoks = []
ewokTower = EwokTower()

done = False

#  Load when leia saves an ewok
pygame.mixer.init()
catchSound = pygame.mixer.Sound("sounds/gabrielaraujo.wav")

# Play once
pygame.mixer.music.load('sounds/littlerobotsoundfactory.mp3')
pygame.mixer.music.play(1)

direction = pygame.K_DOWN

missed = 0
saved = 0
win = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_DOWN or event.key == pygame.K_SPACE):
                direction = event.key
            if (event.key == pygame.K_DOWN or event.key == pygame.K_UP or
                event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
                direction = event.key

    screen.fill(black)
    screen.blit(mf, (0, 0))

    msg = "missed=" + str(missed)
    screen.blit(arial.render(msg, False, white), (400, 330))

    msg = "saved=" + str(saved)
    screen.blit(arial.render(msg, False, white), (400, 350))

    lines = [
        "Aidez la princesse Leia sauve les ewoks",
        "tombantes d'une mort certaine ... "
    ]
    lineY = 15
    for line in lines:
        bonjour = verdana.render(line, False, black)
        screen.blit(bonjour, (23, lineY))
        lineY += 20

    number = random.randint(0, 99)

    count = len(fallingEwoks)
    if (count <= 5):
        if (number >= 0 and number <= 5):
            ewok = Ewok(100, 60)
            fallingEwoks.append(ewok)
        elif (number >= 30 and number <= 31 and count > 1):
            ewok1 = Ewok(200, 60)
            fallingEwoks.append(ewok1)
        elif (number >= 60 and count > 3):
            ewok1 = Ewok(25, 60)
            ewok2 = Ewok(150, 60)
            fallingEwoks.append(ewok1)
            fallingEwoks.append(ewok2)

    # Display all falling ewoks
    if not ewokTower.win:
        for e in fallingEwoks:
            e.display(screen)
            e.move()
            if (e.missed):
                missed += 1
                e.missed = False

    # Display ewo tower
    for e in ewokTower.list:
        e.display(screen)

    if not ewokTower.win:
        darthSidius.display(screen)
        darthSidius.shift()
    else:
        darthSidius.display(screen)
        darthSidius.fall()

    princesseLeia.direction = direction
    princesseLeia.display(screen)
    princesseLeia.move()

    # Count saved
    for e in fallingEwoks:
        if abs(princesseLeia.x - e.x) <= 20 and abs(princesseLeia.y - e.y) <= 20 and e.saved == False:
            savedEwok = Ewok(250, 60, e.type)
            ewokTower.add(savedEwok)
            e.saved = True
            saved += 1
            catchSound.play()

    # Count missed
    for e in fallingEwoks:
        if (e.missed):
            missed += 1
            e.missed = False

    pygame.display.flip()
    clock.tick(60)

    pygame.time.wait(150)

pygame.quit()


