import pygame


class enemy:

    def __init__(self, vel, sprite_file, pos) -> None:
        self.vel = vel
        self.sprite_file = sprite_file
        self.surf = pygame.image.load(sprite_file)
        self.rect = self.surf.get_rect(midbottom = pos)

    def get_vel(self):
        return self.vel

    def update(self):
        self.rect.left -= self.get_vel()
    
    def set_pos(self, pos):
        self.rect.midbottom = pos
    
    def get_pos(self):
        return self.rect.midbottom
    
    def show(self, screen):
        screen.blit(self.surf, self.rect)
    