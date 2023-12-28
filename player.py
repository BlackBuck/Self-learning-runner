import pygame


class player:

    def __init__(self, lives, score, sprite_file, pos) -> None:
        self.lives = lives
        self.score = score
        self.sprite_file = sprite_file
        self.surf = pygame.image.load(self.sprite_file)
        self.rect = self.surf.get_rect(midbottom=pos)
        self.is_jumping = False
    
    def jump(self, gravity, boundary):
        if self.rect.bottom > boundary - 5 and not self.is_jumping:
            self.rect.y += gravity
            self.is_jumping = True
    
    def get_lives(self):
        return self.lives
    
    def reduce_life(self, lives=1):
        self.lives -= lives
    
    def get_score(self):
        return self.score

    def add_score(self, score=1):
        self.score += score
    
    def show(self, screen):
        screen.blit(self.surf, self.rect)
    
    def update(self, gravity, boundary):
        self.rect.y += gravity
        if self.rect.bottom > boundary + 2:
            self.rect.bottom = boundary
            self.is_jumping = False
        if self.rect.top < 0:
            self.rect.top = 2