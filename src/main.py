import pygame

from dot import Dot

SCREEN_SIZE = (1920, 1080)
DT = 60
N_DOTS = 200
DISTANCE_LIMIT = 100
MAX_FRIENDS = 5
MAX_SPEED = 200

pygame.init()

screen = pygame.display.set_mode(SCREEN_SIZE)
surface = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
clock = pygame.time.Clock()
running = True

dots: list[Dot] = [Dot(SCREEN_SIZE, MAX_SPEED) for _ in range(N_DOTS)]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                dots: list[Dot] = [Dot(SCREEN_SIZE, MAX_SPEED) for _ in range(N_DOTS)]

    surface.fill("black")
    screen.fill("black")

    for d1 in dots:
        d1.prune_friends(DISTANCE_LIMIT)

        for d2 in dots:
            if d1 is d2:
                continue

            if d1.is_friendable(d2, DISTANCE_LIMIT):
                d1.add_friend(d2)
                d2.add_friend(d1)

    for d_i in range(len(dots)):
        dot = dots[d_i]
        if not dot.is_on_screen():
            dots[d_i] = Dot(SCREEN_SIZE, MAX_SPEED)

        if dot.expired():
            dots[d_i] = Dot(SCREEN_SIZE, MAX_SPEED)

        dot.update(DT)
        dot.draw(surface)

    screen.blit(surface, (0, 0))
    pygame.display.flip()

    clock.tick(60)
