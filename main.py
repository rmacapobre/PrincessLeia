import pygame

# Entry point

pygame.init()
screen = pygame.display.set_mode((500, 400))
pygame.display.set_caption("Princesse Leia")

black = (0, 0, 0)
white = (255, 255, 255)
clock = pygame.time.Clock()

mf = pygame.image.load("images/mf.jpg")
mf = pygame.transform.scale(mf, (500, 400))

leiaFront1 = pygame.image.load("images/leiaFront1.png")
leiaFront2 = pygame.image.load("images/leiaFront2.png")
leiaFront3 = pygame.image.load("images/leiaFront3.png")
leiaFront4 = pygame.image.load("images/leiaFront4.png")

leiaLeft1 = pygame.image.load("images/leiaLeft1.png")
leiaLeft2 = pygame.image.load("images/leiaLeft2.png")
leiaLeft3 = pygame.image.load("images/leiaLeft3.png")
leiaLeft4 = pygame.image.load("images/leiaLeft4.png")

leiaRight1 = pygame.image.load("images/leiaRight1.png")
leiaRight2 = pygame.image.load("images/leiaRight2.png")
leiaRight3 = pygame.image.load("images/leiaRight3.png")
leiaRight4 = pygame.image.load("images/leiaRight4.png")

leiaBack1 = pygame.image.load("images/leiaBack1.png")
leiaBack2 = pygame.image.load("images/leiaBack2.png")
leiaBack3 = pygame.image.load("images/leiaBack3.png")
leiaBack4 = pygame.image.load("images/leiaBack4.png")

current = 1


x = 10
y = 10
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

    if (direction == pygame.K_DOWN):
        if (current == 1): screen.blit(leiaFront1, (x, y))
        elif (current == 2):
            screen.blit(leiaFront2, (x, y))
        elif (current == 3): screen.blit(leiaFront3, (x, y))
        elif (current == 4):
            screen.blit(leiaFront4, (x, y))
        y += 5
        if (y >= 300): direction = pygame.K_RIGHT
    elif (direction == pygame.K_UP):
        if (current == 1): screen.blit(leiaBack1, (x, y))
        elif (current == 2): screen.blit(leiaBack2, (x, y))
        elif (current == 3): screen.blit(leiaBack3, (x, y))
        elif (current == 4): screen.blit(leiaBack4, (x, y))
        y -= 5
        if (y <= 10): direction = pygame.K_LEFT
    elif (direction == pygame.K_LEFT):
        if (current == 1): screen.blit(leiaLeft1, (x, y))
        elif (current == 2): screen.blit(leiaLeft2, (x, y))
        elif (current == 3): screen.blit(leiaLeft3, (x, y))
        elif (current == 4): screen.blit(leiaLeft4, (x, y))
        x -= 5
        if (x <= 10): direction = pygame.K_DOWN
    elif (direction == pygame.K_RIGHT):
        if (current == 1): screen.blit(leiaRight1, (x, y))
        elif (current == 2): screen.blit(leiaRight2, (x, y))
        elif (current == 3): screen.blit(leiaRight3, (x, y))
        elif (current == 4): screen.blit(leiaRight4, (x, y))
        x += 5
        if (x >= 300): direction = pygame.K_UP
    else:
        # Stop walking
        continue

    current += 1
    if (current == 5): current = 1

    pygame.display.flip()
    clock.tick(60)

    pygame.time.wait(150)

pygame.quit()


