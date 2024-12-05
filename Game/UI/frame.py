import pygame

class Frame:
    def __init__(self,position,size,text):
        self.position=position
        self.size=size
        self.rect=pygame.Rect(self.position,self.size)
        self.rect_small=self.rect.copy()
        self.rect_small.height=self.rect_small.height-50
        self.rect_small.width=self.rect_small.width-20
        self.rect_small.center=self.rect.center
        self.rect_small.top+=15
        self.text=text
        self.font = pygame.font.Font(None, 30)
        self.text_surface=self.font.render(self.text,True,"white")
        
        
        
    def draw(self,screen):
        pygame.draw.rect(screen,"#ffd700",self.rect,border_radius=15)
        pygame.draw.rect(screen,"#c45e00",self.rect_small,border_radius=15)
        
        screen.blit(self.text_surface,(self.rect.center[0]-self.text_surface.get_width()/2,self.position[1]+10))