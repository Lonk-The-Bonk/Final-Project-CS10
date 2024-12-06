import pygame

class TextInput():

    def __init__(self,position,size,font_size=28):
        
        self.rect = pygame.Rect(position[0],position[1],size[0],size[1])
        self.color = pygame.Color('gray')
        self.text = ''
        self.font = pygame.font.Font(None, font_size)
        self.active = False
        self.t_flag = True

    
    def draw(self,screen):
        pygame.draw.rect(screen, self.color, self.rect, 2)
        text_surface = self.font.render(self.text, True, self.color)
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))

        self.rect.w = max(300, text_surface.get_width() + 10)

    def handle_event(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:

                # If the user clicks on the text input box, activate it.
                if self.rect.collidepoint(event.pos):
                    self.active = True
                    self.color = pygame.Color('white')
                else:
                    self.active = False
                    self.color = pygame.Color('gray')
             

            if event.type == pygame.KEYDOWN and self.active:
                if event.key == pygame.K_BACKSPACE:
                    # If the user presses backspace, remove the last character from the text box.
                    self.text = self.text[:-1]
                else:
                    # Otherwise, add the character to the text box.
                    self.text += event.unicode

        
        
class NumberInput():

    def __init__(self,position,size,font_size=28,min=0,max=999999):
        
        self.rect = pygame.Rect(position[0],position[1],size[0],size[1])
        self.color = pygame.Color('gray')
        self.text = ''
        self.font = pygame.font.Font(None, font_size)
        self.active = False
        self.t_flag = True
        self.max=max

    
    def draw(self,screen):
        pygame.draw.rect(screen, self.color, self.rect, 2)
        text_surface = self.font.render(self.text, True, self.color)
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))

        self.rect.w = max(self.rect.w, text_surface.get_width() + 10)

    def handle_event(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:

                # If the user clicks on the text input box, activate it.
                if self.rect.collidepoint(event.pos):
                    self.active = True
                    self.color = pygame.Color('white')
                else:
                    self.active = False
                    self.color = pygame.Color('gray')
             

            if event.type == pygame.KEYDOWN and self.active:
                if event.key == pygame.K_BACKSPACE:
                    # If the user presses backspace, remove the last character from the text box.
                    self.text = self.text[:-1]
                elif event.unicode in "0123456789":
                    if int(self.text+event.unicode)<=self.max and not (self.text==''and event.unicode=="0"):
                    # Otherwise, add the character to the text box.
                        self.text += event.unicode
