import os
import pygame
from settings import Images_Path,WIDTH,HEIGHT,Background_Color
from UI.image import Image
from UI.frame import Frame
from UI.button import Button
from UI.checkbox import Checkbox

class WinScreen:
    def __init__(self,players) -> None:
        self.players=players
        
        
        self.font_big = pygame.font.Font(None, 45)
        self.font_normal = pygame.font.Font(None, 30)
        self.font_small = pygame.font.Font(None, 22)
        
        self.load_resources()
        self.gameover_frame=Frame((20,20),(960,640),"GameOver")
        
        
    def load_resources(self):
        self.logo=Image(os.path.join(Images_Path,"Menu","Logo.png"),(WIDTH/2,-50+HEIGHT/3),alignV="center",alignH="center")
        self.tokens=[]
        self.tokens_rect=[]
        for i in range(1,9):
            token=pygame.image.load(os.path.join(Images_Path,"Tokens",f"{i}.png"))
            token_rect=token.get_rect()
            token_rect.topleft=(250+(i-1)*60,-5+HEIGHT/2)
            self.tokens.append(token)
            self.tokens_rect.append(token_rect)
            
    
    def draw(self,screen:pygame.Surface):
        screen.fill(Background_Color)
        self.gameover_frame.draw(screen)
        for i,title in enumerate(["Total Cash Earn","Total Cash Spent","Properties Bought","Properties Sold","Tax Payed","Jail"]):
            self.text_surface = self.font_small.render(title, True, "white")
            screen.blit(self.text_surface,(40,220+i*50))
        for i,player in enumerate(self.players):
            if not player.is_bankrupt:
                self.text_surface = self.font_big.render(player.name+" Wins", True, "white")
                screen.blit(self.text_surface,(-self.text_surface.get_width()/2+500,100))
            self.text_surface = self.font_normal.render(player.name, True, "white")
            screen.blit(self.text_surface,(-self.text_surface.get_width()/2+240+i*125,170))
            self.text_surface = self.font_normal.render(str(player.total_cash_received), True, "white")
            screen.blit(self.text_surface,(-self.text_surface.get_width()/2+240+i*125,220))
            self.text_surface = self.font_normal.render(str(player.total_cash_spent), True, "white")
            screen.blit(self.text_surface,(-self.text_surface.get_width()/2+240+i*125,270))
            self.text_surface = self.font_normal.render(str(player.properties_bought), True, "white")
            screen.blit(self.text_surface,(-self.text_surface.get_width()/2+240+i*125,320))
            self.text_surface = self.font_normal.render(str(player.properties_sold), True, "white")
            screen.blit(self.text_surface,(-self.text_surface.get_width()/2+240+i*125,370))
            self.text_surface = self.font_normal.render(str(player.tax_payed), True, "white")
            screen.blit(self.text_surface,(-self.text_surface.get_width()/2+240+i*125,420))
            self.text_surface = self.font_normal.render(str(player.jail_counter), True, "white")
            screen.blit(self.text_surface,(-self.text_surface.get_width()/2+240+i*125,470))
        
    
    def update(self,deltatime):
        pass
       
    
    
    def done_pressed(self):
        if len(self.players)>1:
            self.Status="Done"
    
    def handle_events(self,events):
        pass
        