import pygame
import glob
import math
import random

class Ewok:
    def __init__(self, startx, starty):
        self.x = startx
        self.y = starty
        self.angle = 0
        self.direction = pygame.K_DOWN
        self.saved = False
        self.missed = False
        number = random.randint(0, 3)
        if (number == 0): self.img =  pygame.image.load("images/ewok1.png")
        elif (number == 1): self.img = pygame.image.load("images/ewok2.png")
        elif (number == 2): self.img = pygame.image.load("images/ewok3.png")
        else: self.img =  pygame.image.load("images/ewok4.png")

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
        # Define limits
        if self.x <= 10: self.x = 10
        if self.x >= 450: self.x = 450
        if self.y <= 330: self.y = 340
        if self.y >= 340: self.y = 340


# Entry point

pygame.init()
screen = pygame.display.set_mode((500, 400))
pygame.display.set_caption("Princesse Leia")

black = (0, 0, 0)
white = (255, 255, 255)
yellow = (255, 255, 0)
clock = pygame.time.Clock()

pygame.font.init()
comicSansMS = pygame.font.SysFont('Verdana', 15)
comicSansMS.set_bold(True)

mf = pygame.image.load("images/mf.jpg")
mf = pygame.transform.scale(mf, (500, 400))

darthSidius = Person(350, 60, "ds")
princesseLeia = Person(10, 350, "leia")

fallingEwoks = []
ewokTower = EwokTower()

done = False
pygame.mixer.music.load("sounds/femalefootstep.wav")
direction = pygame.K_DOWN

missed = 0
saved = 0

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
    bonjour = comicSansMS.render(msg, False, black)
    screen.blit(bonjour, (23, 10))

    msg = "saved=" + str(saved)
    bonjour = comicSansMS.render(msg, False, black)
    screen.blit(bonjour, (23, 20))

    number = random.randint(0, 99)

    count = len(fallingEwoks)
    if (count <= 3):
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
    for e in fallingEwoks:
        e.display(screen)
        e.move()
        if (e.missed):
            missed += 1
            e.missed = False

    # Display ewo tower
    for e in ewokTower.list:
        e.display(screen)

    darthSidius.display(screen)

    princesseLeia.direction = direction
    princesseLeia.display(screen)
    princesseLeia.move()

    # Count saved
    for e in fallingEwoks:
        if abs(princesseLeia.x - e.x) <= 20 and abs(princesseLeia.y - e.y) <= 20 and e.saved == False:
            savedEwok = Ewok(250, 60)
            ewokTower.add(savedEwok)
            e.saved = True
            saved += 1

    # Count missed
    for e in fallingEwoks:
        if (e.missed):
            missed += 1
            e.missed = False

    pygame.display.flip()
    clock.tick(60)

    pygame.time.wait(150)

pygame.quit()


