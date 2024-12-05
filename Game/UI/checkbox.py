import pygame


class Checkbox:
    def __init__(self,position,size,text,
                 fontsize=25,bgcolor="white",
                 textcolor="black",borderwidth=1
                 ,bordercolor="black",borderradius=1
                 ):
        self.position=position
        self.size=size
        self.text=text
        self.enable=True
        self.checked=False
        
        self.bgcolor=bgcolor
        self.textcolor=textcolor
        self.borderwidth=borderwidth
        self.bordercolor=bordercolor
        self.borderradius=borderradius
        
        font = pygame.font.Font(None, fontsize)
        self.text_surface = font.render(self.text, True, self.textcolor)
        self.text_rect=self.text_surface.get_rect()
        self.rect=pygame.Rect((position[0]+self.text_rect.width+5,position[1]),size)
        
        
        
        
    
    def draw(self,screen):
        if self.enable:
            if self.checked:
                pygame.draw.rect(screen,self.bgcolor,self.rect,border_radius=self.borderradius)
            
            pygame.draw.rect(screen,self.bordercolor,self.rect,self.borderwidth,self.borderradius)
            screen.blit(self.text_surface,self.position)
        
    def handle_events(self,events):
        if self.enable:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.rect.collidepoint(event.pos):
                        self.checked=not self.checked