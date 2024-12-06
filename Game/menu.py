import os
import csv
import pygame
from settings import Images_Path,WIDTH,HEIGHT,Background_Color
from UI.image import Image
from UI.input import TextInput
from UI.button import Button
from UI.checkbox import Checkbox
from UI.frame import Frame
class MainMenu:
    def __init__(self) -> None:
        
        self.selected_token=-1
        self.players=[]
        self.selected_tokens=[]
        
        self.font = pygame.font.Font(None, 30)
        
        self.load_resources()
        self.name_input=TextInput((-150+WIDTH/2,-50+HEIGHT/2),(120,30))
        self.add_button=Button((-120+WIDTH/2,50+HEIGHT/2),(100,40),"Add",callback=self.add_player,fontsize=30,textcolor="black",bgcolor="yellow",bordercolor="orange",borderwidth=5,borderradius=10)
        self.done_button=Button((20+WIDTH/2,50+HEIGHT/2),(100,40),"Done",callback=self.done_pressed,fontsize=30,textcolor="black",bgcolor="yellow",bordercolor="orange",borderwidth=5,borderradius=10)
        self.bot_checkbox=Checkbox((50+120+WIDTH/2,-40+HEIGHT/2),(20,20),"Bot",fontsize=30,textcolor="black",bgcolor="yellow",bordercolor="orange",borderwidth=5,borderradius=10)
        self.leaderboard_button=Button((830,630),(150,40),"Leaderboard",callback=self.show_leaderboard,fontsize=30,textcolor="black",bgcolor="yellow",bordercolor="orange",borderwidth=5,borderradius=10)
        
        self.Status="Choosing"
        
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
        
    
    def show_leaderboard(self):
        self.leaderboard_frame=Frame((250,40),(500,580),"Leaderboard")
        self.Status="Leaderboard"
        self.close_button=Button((450,550),(100,40),"Close",callback=self.close_leaderboard,fontsize=30,textcolor="black",bgcolor="yellow",bordercolor="orange",borderwidth=5,borderradius=10)

        
        
    def close_leaderboard(self):
        self.Status="Choosing"
    
    def draw(self,screen:pygame.Surface):
        screen.fill(Background_Color)
        self.logo.draw(screen)
        self.name_input.draw(screen)
        self.add_button.draw(screen)
        self.bot_checkbox.draw(screen)
        self.leaderboard_button.draw(screen)
        if len(self.players)>1:
            self.done_button.draw(screen)
        for i,token in enumerate(self.tokens):
            if i not in self.selected_tokens:
                height=-5
                if i==self.selected_token:
                    height=5
                screen.blit(token,(250+i*60,height+HEIGHT/2))
        
        for i,player in enumerate(self.players):
            screen.blit(player[1],(350,i*40+100+HEIGHT/2))
            
            self.text_surface = self.font.render(player[0], True, "white")
            screen.blit(self.text_surface,(400,i*40+110+HEIGHT/2))
        if self.Status=="Leaderboard":
            self.leaderboard_frame.draw(screen)
            self.close_button.draw(screen)
            if os.path.isfile("leaderboard.csv"):
                players=[]

                with open('leaderboard.csv') as leaderboard_file:
                    csv_reader = csv.reader(leaderboard_file, delimiter=',')
                    i=0
                    for row in csv_reader:
                        if i!=0:
                            players.append([row[0],int(row[1])])
                        i+=1
                players.sort(key=lambda x: x[1],reverse=True)
                if len(players)>10:
                    players=players[:10]
                i=0
                for player in players:
                    self.text_surface = self.font.render(str(player[0]), True, "white")
                    screen.blit(self.text_surface,(300,i*40+100))
                    self.text_surface = self.font.render(str(player[1]), True, "white")
                    screen.blit(self.text_surface,(550,i*40+100))
                    i += 1    
                        
                    
        
    def update(self,deltatime):
        if self.Status=="Done":
            return self.players
        return None
    
    def add_player(self):
        for player in self.players:
            if player[0]==self.name_input.text:
                return
        if self.name_input.text!="" and self.selected_token!=-1 and len(self.players)<6:
            player_type="Player"
            if self.bot_checkbox.checked:
                player_type="Bot"
            self.players.append((self.name_input.text,self.tokens[self.selected_token],player_type))
            self.selected_tokens.append(self.selected_token)
            self.name_input.text=""
            self.selected_token=-1
    
    def done_pressed(self):
        if len(self.players)>1:
            self.Status="Done"
    
    def handle_events(self,events):
        if self.Status=="Choosing":
            self.name_input.handle_event(events)
            self.add_button.handle_events(events)
            self.bot_checkbox.handle_events(events)
            self.leaderboard_button.handle_events(events)
            if len(self.players)>1:
                self.done_button.handle_events(events)
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i,token_rect in enumerate(self.tokens_rect):
                        if token_rect.collidepoint(event.pos) and i not in self.selected_tokens and len(self.players)<6:
                            self.selected_token=i
        elif self.Status=="Leaderboard":
            self.close_button.handle_events(events)