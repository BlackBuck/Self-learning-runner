import pygame
from sys import exit
from ann import ann
import random
from player import player
from enemy import enemy
from menu import menu

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Self Player")
clock = pygame.time.Clock()

#misc game variables
font = pygame.font.Font(None, 50)
paused  = True
gravity = 1


#player
pl = player(300, 0, './player_walk_1.png', (200, 299))

#enemies
enemies = [enemy(5, './snail1.png', (800 + 200 + random.randint(10, 100), 300)) for _ in range(1)]

#player score and lives
score_txt = "Score : " + str(pl.get_score())
lives_txt = "Lives : " + str(pl.get_lives())

score_surf = font.render(score_txt, False, 'brown')
score_rect = score_surf.get_rect(topleft=(10, 10))
lives_surf = font.render(lives_txt, False, 'brown')
lives_rect = lives_surf.get_rect(topleft=(10, 45))

#ground and sky
ground = pygame.image.load('ground.png').convert()
ground_rect = ground.get_rect(topleft=(0,300))
sky = pygame.image.load('Sky.png').convert()


pause_menu = menu("Paused", ["Resume", "Quit", "Restart"], font, (350, 100), (220, 200))

#default initialisation of ann
nn = ann(4, 5, 2, 0.2)
outputs = [[0], [0]]
inputs = [enemies[0].rect.width, enemies[0].rect.height, enemies[0].get_vel(), enemies[0].rect.left - pl.rect.right]

while True:

    #update the score and life text
    score_txt = "Score : " + str(pl.get_score())
    lives_txt = "Lives : " + str(pl.get_lives())
    score_surf = font.render(score_txt, False, "brown")
    lives_surf = font.render(lives_txt, False, "brown")

    #player collides with the first snail
    if pl.rect.colliderect(enemies[0]):
        pl.reduce_life()
        if outputs[0][0] > 0.5:
            nn.train(inputs, [[0], [1]])
        else:
            nn.train(inputs, [[1], [0]])
        enemies.pop(0)
        enemies.append(enemy(5, './snail1.png', (800 + random.randint(10, 100), 300)))
    
    if pl.get_lives() == 0:
        paused = True
    
    if paused:
        #pause logic
        pygame.display.flip()
        screen.blit(sky, (0,0))
        screen.blit(ground, ground_rect)
        screen.blit(score_surf, (350, 10))
        screen.blit(lives_surf, (350, 50))

        buttons = pause_menu.show(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttons[0].collidepoint(pygame.mouse.get_pos()):
                    #resume button
                    paused = False
                if buttons[1].collidepoint(pygame.mouse.get_pos()):
                    #quit button
                    pygame.quit()
                    exit()
                if buttons[2].collidepoint(pygame.mouse.get_pos()):
                    #restrart
                    pl = player(300, 0, './player_walk_1.png', (200, 299))
                    nn = ann(4, 5, 2, 0.2)
                    paused = False
    else:
        #regular game logic
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and pl.rect.bottom > 280:
                    gravity = -20
                    pl.jump(gravity, 300)
                    inputs = [enemies[0].rect.width, enemies[0].rect.height, enemies[0].get_vel(), enemies[0].rect.left - pl.rect.right]
                    nn.train(inputs, [[1], [0]])
                if event.key == pygame.K_p:
                    paused = True
                    pass
            
        screen.blit(sky, (0, 0))

        #display all enemies
        for en in enemies:
            en.show(screen)
        
        #display other surfaces
        screen.blit(ground, (0, 300))
        screen.blit(score_surf, score_rect)
        screen.blit(lives_surf, lives_rect)

        gravity += 1
        pl.update(gravity, 300)
        pl.show(screen)

        #enemy updation and collision detection
        for en in enemies:
            en.update()
            if en.rect.x < -50:
                enemies.pop(enemies.index(en))
                enemies.append(enemy(5, './snail1.png', (800 + random.randint(10, 100), 300)))
                pl.add_score()
                if(outputs[0][0] > 0.50):
                    nn.train(inputs, [[1], [0]])
                else: nn.train(inputs, [[0], [1]])        
        
        inputs = [enemies[0].rect.width, enemies[0].rect.height, enemies[0].get_vel(), enemies[0].rect.left - pl.rect.right]

        outputs = nn.query(inputs)

        #train player based on the outputs
        if(outputs[0][0] > 0.5):
            gravity = -20
            pl.jump(gravity, 300)
            if pl.rect.colliderect(enemies[0]):
                pl.reduce_life()
                enemies.pop(0)
                enemies.append(enemy(5, './snail1.png', (800 + random.randint(10, 100), 300)))
                nn.train(inputs, [[0], [1]])
            else:
                nn.train(inputs, [[1], [0]])
        else:
            if pl.rect.colliderect(enemies[0]):
                pl.reduce_life()
                enemies.pop(0)
                enemies.append(enemy(5, './snail1.png', (800 + random.randint(10, 100), 300)))
                nn.train(inputs, [[1], [0]])
            else:
                nn.train(inputs, [[0], [1]])
    
        pygame.display.flip()
        clock.tick(60)

