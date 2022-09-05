import pygame
from physics import Cloth


WIN = pygame.display.set_mode((500,900))
CLOCK = pygame.time.Clock()
FPS = 0
TIME = 0
RUNNING = True




cloth = Cloth((60,60),(20,20))



while RUNNING:

    WIN.fill((0,0,15))


    DT = CLOCK.tick() / 1000
    TIME += DT

    if DT != 0:
        FPS = 1/DT

    pygame.display.set_caption(f"Cloth Simulation | {round(FPS)} fps | {round(TIME)} seconds elapsed.")

    cloth.update(DT)
    cloth.draw(WIN)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False


    pygame.display.update()
