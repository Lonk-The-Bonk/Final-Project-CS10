import pygame


class Button:
    def __init__(self,position,size,text,callback=None,
                 fontsize=25,bgcolor="white",
                 textcolor="black",borderwidth=1
                 ,bordercolor="black",borderradius=1
                 ):
        self.position=position
        self.size=size
        self.text=text
        self.enable=True
        self.callback=callback
        self.rect=pygame.Rect(position,size)
        self.bgcolor=bgcolor
        self.textcolor=textcolor
        self.borderwidth=borderwidth
        self.bordercolor=bordercolor
        self.borderradius=borderradius
        
        font = pygame.font.Font(None, fontsize)
        self.text_surface = font.render(self.text, True, self.textcolor)
        self.text_rect=self.text_surface.get_rect()
        self.text_rect.center=self.rect.center
        
        
        
    
    def draw(self,screen):
        if self.enable:
            pygame.draw.rect(screen,self.bgcolor,self.rect,border_radius=self.borderradius)
            pygame.draw.rect(screen,self.bordercolor,self.rect,self.borderwidth,self.borderradius)
            screen.blit(self.text_surface,self.text_rect)
        
    def handle_events(self,events):
        if self.enable:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.rect.collidepoint(event.pos) and self.callback!=None:
                        self.callback()


