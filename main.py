import pygame
from game import Game

game = Game()

run = True 
clock = pygame.time.Clock()

while run:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game.paused = True 
            if event.key == pygame.K_ESCAPE:
                run = False
        if event.type == pygame.QUIT:
            run = False
            break 

    game.loop()
    game.draw()

    if game.run == False:
        run = False
    
    pygame.display.update()

pygame.quit()

