import pygame
class menu:

    def __init__(self, title, buttons, font, pos, dimensions):
        #provide the menu title and the buttons
        self.title = title #the title of the menu
        self.buttons = buttons #defines what buttons need to be displayed
        self.font = font #pygame font instant
        self.x, self.y = pos
        self.width, self.height = dimensions

    def show(self, screen):
        #acceps the screen instance and draws on it
        
        #the background for the menu
        pygame.draw.rect(screen, "black", pygame.Rect(self.x, self.y, self.width, self.height), 0, 5)
        screen.blit(self.font.render(self.title, False, "white"), (self.x + 30, self.y + 10))

        menu_buttons = []
        for i in range(len(self.buttons)):
            button = self.buttons[i]
            btn = self.font.render(button, False, "white")
            btn_rect = btn.get_rect(topleft=(self.x + 30, self.y + 50*(i + 1)))
            menu_buttons.append(btn_rect)
            pygame.draw.rect(screen, "brown", btn_rect)
            screen.blit(btn, (self.x + 30, self.y + 50*(i + 1)))
            if btn_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, "white", btn_rect, 2)
        
        return menu_buttons

