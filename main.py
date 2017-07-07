import pygame
import glob

class Person:
    def __init__(self, startx, starty, name, screen):
        self.x = startx
        self.y = starty
        self.current = 1
        self.direction = pygame.K_DOWN

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
        if (self.direction == pygame.K_LEFT): self.x -= 5
        if (self.direction == pygame.K_RIGHT): self.x += 5


# Entry point

pygame.init()
screen = pygame.display.set_mode((500, 400))
pygame.display.set_caption("Princesse Leia")

black = (0, 0, 0)
white = (255, 255, 255)
yellow = (255, 255, 0)
clock = pygame.time.Clock()

pygame.font.init()
comicSansMS = pygame.font.SysFont('FreeMono, Bold', 35)
comicSansMS.set_bold(True)


mf = pygame.image.load("images/mf.jpg")
mf = pygame.transform.scale(mf, (500, 400))

darthSidius = Person(350, 60, "ds", screen)
princesseLeia = Person(10, 350, "leia", screen)

done = False
pygame.mixer.music.load("sounds/femalefootstep.wav")
direction = pygame.K_DOWN

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

    msg = "x=" + str(princesseLeia.x) + " y=" + str(princesseLeia.y)
    bonjour = comicSansMS.render(msg, False, black)
    screen.blit(bonjour, (23, 10))

    darthSidius.display(screen)

    princesseLeia.direction = direction
    princesseLeia.display(screen)
    princesseLeia.move()

    pygame.display.flip()
    clock.tick(60)

    pygame.time.wait(150)

pygame.quit()


