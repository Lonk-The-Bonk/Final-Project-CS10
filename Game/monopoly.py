import os
import csv
from utils import draw_text
import pygame
from functools import partial       
from UI.image import Image
from UI.button import Button
from UI.frame import Frame
from UI.input import NumberInput
from settings import Images_Path,Background_Color,BOARD
from player import Player
from random import randint,shuffle,choice
from Monopoly.block import Block
from textwrap3 import wrap
pygame.init()


FONT = pygame.font.Font(None, 30)
FONT_SMALL = pygame.font.Font(None, 25)

class Monopoly:
    players=[]
    chance_cards = [
    ("Advance to Go (Collect $200)", lambda player: player.move_to_space(0, collect=True)),
    ("Advance to Pall Mall—If you pass Go, collect $200", lambda player: player.move_to_space(24, collect=True)),
    ("Advance to The Angel Islington —If you pass Go, collect $200", lambda player: player.move_to_space(11, collect=True)),
    ("Advance token to nearest Utility. If unowned, you may buy it from the Bank. If owned, throw dice and pay owner a total of ten times the amount thrown.", lambda player: player.move_to_nearest_utility()),
    ("Advance token to the nearest RailRoad and pay owner twice the rental to which he/she is otherwise entitled. If RailRoad is unowned, you may buy it from the Bank.", lambda player: player.move_to_nearest_RailRoad()),
    ("Bank pays you dividend of $50", lambda player: player.add_cash(50)),
    ("Get Out of Jail Free—This card may be kept until needed or sold.", lambda player: player.add_chance_card("Get Out of Jail Free")),
    ("Go Back 3 Spaces", lambda player: player.move_spaces(-3)),
    ("Go Directly to Jail—Do not pass Go, do not collect $200", lambda player: player.go_to_jail()),
    ("Make general repairs on all your property—For each house pay $25, For each hotel $100.", lambda player: player.make_repairs(25,100)),
    ("Pay poor tax of $15", lambda player: player.pay_cash(15)),
    ("Take a trip to Reading RailRoad—If you pass Go, collect $200", lambda player: player.move_to_space(5, collect=True)),
    ("Take a walk on the Mayfair—Advance token to Mayfair", lambda player: player.move_to_space(39)),
    ("You have been elected Chairman of the Board—Pay each player $50", lambda player: player.pay_players(50)),
    ("Your building loan matures—Collect $150", lambda player: player.add_cash(150)),
    ("You have won a crossword competition—Collect $100.", lambda player: player.add_cash(100))
]
    community_chest_cards = [
    ("Advance to Go (Collect $200)", lambda player: player.move_to_space(0, collect=True)),
    ("Bank error in your favor – Collect $75", lambda player: player.add_cash(75)),
    ("Doctor's fees – Pay $50", lambda player: player.pay_cash(50)),
    ("Get out of jail free – This card may be kept until needed", lambda player: player.add_chance_card("Get out of jail free")),
    ("Go to jail – Go directly to jail – Do not pass Go, do not collect $200", lambda player: player.go_to_jail()),
    ("It is your birthday - Collect $10 from each player", lambda player: player.pay_players(-10)),
    ("Grand Opera Night – Collect $50 from every player for opening night seats", lambda player: player.pay_players(-50)),
    ("Income Tax refund – Collect $20", lambda player: player.add_cash(20)),
    ("Life Insurance Matures – Collect $100", lambda player: player.add_cash(100)),
    ("Pay Hospital Fees of $100", lambda player: player.pay_cash(100)),
    ("Pay School Fees of $50", lambda player: player.pay_cash(50)),
    ("Receive $25 Consultancy Fee", lambda player: player.add_cash(25)),
    ("You are assessed for street repairs – $40 per house, $115 per hotel", lambda player: player.make_repairs(40,115)),
    ("You have won second prize in a beauty contest– Collect $10", lambda player: player.add_cash(10)),
    ("You inherit $100", lambda player: player.add_cash(100))
]

    def __init__(self,players) -> None:
        self.Initialize_Board()
        
        self.Status="Free"
        self.delay=0
        self.players=[]
        for i,player in enumerate(players):
            self.players.append(Player(player[0],player[1],player[2],i,self.board))
        for player in self.players:
            player.all_players=self.players
        self.current_player=self.players[0]
        self.players[0].chance_cards=["Get Out Of Jail"]
        self.players[1].chance_cards=["Get Out Of Jail"]
        #self.players[1].cash=0
        #self.current_player.go_to_jail()
        
        self.GameOver=False
        # for block in self.board.values():
        #     if block.Type in ["Street","RailRoad","Utility"]:
        #         #block.owner=self.current_player
        #         block.houses=0
        #         pass

        self.load_resources()
        self.dice1=1
        self.dice2=1
        
        self.dice_animating=False
        
        self.double_counter=0
        
        self.players_frame=Frame((685,15),(300,300),"Players")
        self.player_properties_frame=Frame((685,320),(300,350),"Properties")
        self.roll_button=Button((290,430),(100,40),"Roll",callback=self.animate_dice,fontsize=30,textcolor="black",bgcolor="yellow",bordercolor="orange",borderwidth=5,borderradius=10)
        self.end_turn_button=Button((290,430),(100,40),"End Turn",callback=self.next_player_turn,fontsize=30,textcolor="black",bgcolor="yellow",bordercolor="orange",borderwidth=5,borderradius=10)
        self.buy_button=Button((230,430),(100,40),"Buy",callback=self.buy_property,fontsize=30,textcolor="black",bgcolor="yellow",bordercolor="orange",borderwidth=5,borderradius=10)
        self.auction_button=Button((360,430),(100,40),"Auction",callback=self.show_auction,fontsize=30,textcolor="black",bgcolor="yellow",bordercolor="orange",borderwidth=5,borderradius=10)
        self.build_button=Button((180,480),(100,40),"Build",callback=self.show_build_menu,fontsize=30,textcolor="black",bgcolor="yellow",bordercolor="orange",borderwidth=5,borderradius=10)
        self.trade_button=Button((290,480),(100,40),"Trade",callback=self.show_trade_menu,fontsize=30,textcolor="black",bgcolor="yellow",bordercolor="orange",borderwidth=5,borderradius=10)
        self.sell_button=Button((400,480),(100,40),"Sell",callback=self.show_sell_menu,fontsize=30,textcolor="black",bgcolor="yellow",bordercolor="orange",borderwidth=5,borderradius=10)
        
        self.cancel_button=Button((290,550),(100,40),"Close",callback=self.close_window,fontsize=30,textcolor="black",bgcolor="yellow",bordercolor="orange",borderwidth=5,borderradius=10)
        self.bankrupt_button=Button((360,525),(100,40),"Bankrupt",callback=self.Bankrupt,fontsize=30,textcolor="black",bgcolor="yellow",bordercolor="orange",borderwidth=5,borderradius=10)
        self.pay_button=Button((390,430),(100,40),"Pay 50",callback=self.pay_to_release,fontsize=30,textcolor="black",bgcolor="yellow",bordercolor="orange",borderwidth=5,borderradius=10)
        self.use_card_button=Button((190,430),(100,40),"Use Card",callback=self.use_card_to_release,fontsize=30,textcolor="black",bgcolor="yellow",bordercolor="orange",borderwidth=5,borderradius=10)
        



        self.previous_State="Roll"
        self.current_property=None
        
    def Bankrupt(self):
        self.current_player.bankrupt()
        self.next_player_turn()
    def Initialize_Board(self):
        self.board={}
        for block in BOARD:
            self.board[block]=Block(BOARD[block])
            
    def next_player_turn(self):
        
        i=self.current_player.index+1
        if i>=len(self.players):
            i=0
        while i!=self.current_player.index:
            if not self.players[i].is_bankrupt:
                break
            i+=1
            if i>=len(self.players):
                i=0
        playable_players=0
        for player in self.players:
            if not player.is_bankrupt:
                
                playable_players+=1
        if playable_players<2:
            self.GameOver=True
        self.current_player=self.players[i]
        self.winner=i
        self.Status="Free"
    def load_resources(self):
        self.board_image=Image(os.path.join(Images_Path,"Board","board.png"),(15,15))
        self.dice=[]
        for i in range(1,7):
            self.dice.append(pygame.image.load(os.path.join(Images_Path,"Dice",f"{i}.png")).convert_alpha())
        self.tokens=[]
        for i in range(1,9):
            self.tokens.append(pygame.image.load(os.path.join(Images_Path,"Tokens",f"{i}.png")))
        self.house_icon=pygame.transform.smoothscale(pygame.image.load(os.path.join(Images_Path,"Icons","house.png")),(20,20))
        self.hotel_icon=pygame.transform.smoothscale(pygame.image.load(os.path.join(Images_Path,"Icons","hotel.png")),(20,20))
        
    def animate_dice(self):
        self.dice_animating=True
        self.animation_duration=0.5
        self.animation_timer=0
        self.Status="Rolling"
    
    def buy_property(self):
        if self.current_player.cash>=self.current_property.Price:
            self.current_player.buy_property(self.current_property)
            self.Status="Done"
    
    def get_color_property(self,color):
        properties=[]
        for block in self.board.values():
            if block.Type=="Street":
                if block.Color==color:
                    properties.append(block)
        return properties

    def can_build(self):
        checked=[]
        can_build=False
        for block in self.board.values():
            if block.Type=="Street":
                if not block.Color in checked:
                    checked.append(block.Color)
                    build=True
                    for property in self.get_color_property(block.Color):
                        if not property.owner==self.current_player:
                            build=False
                            break
                    if build:
                        can_build=True
                        break
                
        return can_build


    def close_window(self):
        self.Status=self.previous_State
        print(self.Status)

    def get_board_coordinates(self,position,height=0):
    
        if position < 10:
            x = 10 - position
            y = 10
        elif position < 20:
            x = 0
            y = 10 - (position - 10)
        elif position < 30:
            x = position - 20
            y = 0
        else:
            x = 10
            y = position - 30
            
        # Scale the x and y values based on the board width
        scale_factor = 560 / 11  # 11 is the width of the board in positions
        x *= scale_factor
        y *= scale_factor
        if position>=0 and position<=10:
            y+=80-height
        elif position>=11 and position<=20:
            x-=70-height
        elif position>=21 and position<=30:
            y-=70-height
        elif position>=31 and position<=40:
            x+=80-height
        x+=70
        y+=70
        return (x, y)
    
    
    def draw_property_owners(self,screen):
        for i,block in enumerate(self.board.values()):
            if block.Type in ["Street","RailRoad","Utility"]:
                if block.owner!=None:
                    screen.blit(block.owner.small_token,self.get_board_coordinates(i,20))
                    if block.Type=="Street":
                        if block.houses>0:
                            if block.houses<5:
                                screen.blit(self.house_icon,self.get_board_coordinates(i,40))
                                
                                text_pos=self.get_board_coordinates(i,40)
                                
                                draw_text(screen,(text_pos[0]+20,text_pos[1]),"x"+str(block.houses),FONT_SMALL,"yellow")
                                
                            if block.houses==5:
                                screen.blit(self.hotel_icon,self.get_board_coordinates(i,40))
    
    
    def show_auction(self):
        self.Status="Auction"
        self.auction_window=Auction_Window(self.players,self.current_property)
        
    
    
    def sell_porperty(self,player,property):
        player.sell_property(property)
        self.show_sell_menu()
    
    def show_sell_menu(self):
        if self.Status!="Selling":
            self.previous_State=self.Status
        self.Status="Selling"
        self.sell_frame=Frame((60,60),(570,570),"Sell")
        player=self.current_player
        cant_sell_properties=[]
        player.sell_buttons=[]
        row=0
        col=0
        for i,property in enumerate(self.current_player.properties):
                
                if property.Type=="Street":
                    if not property.Color in cant_sell_properties:
                        
                        for p in self.get_color_property(property.Color):
                            if p.houses!=0:
                                cant_sell_properties.append(property.Color)
                                break
                    if property.Color in cant_sell_properties:
                        continue
                    
                player.sell_buttons.append([property,Button((270+row*280,110+col*26),(70,22),f"Sell",callback=partial(self.sell_porperty,self.current_player,property),fontsize=20,textcolor="black",bgcolor="yellow",bordercolor="orange",borderwidth=5,borderradius=10)])
                row+=1
                if row>1:
                    row=0
                    col+=1
    
    


    def draw_selling_menu(self,screen):
        self.sell_frame.draw(screen)
        player=self.current_player
        
        
        row=0
        col=0
        for i,button in enumerate(player.sell_buttons):
            property=button[0]
            draw_text(screen,(80+row*280,120+col*26),property.Name,FONT_SMALL,"white")
            


            button[1].draw(screen)
            row+=1
            if row>1:
                row=0
                col+=1
        self.cancel_button.draw(screen)
    
    def trade_type_select(self,type):
        self.trade_state_player=type
    
    def other_player_trade_type_select(self,type):
        self.trade_state_other_player=type

    def player_property_for_trade(self,property):
        self.player_trade_property=property
    def other_player_property_for_trade(self,property):
        self.other_player_trade_property=property
    def confirm_trade(self):
        print(1)
        selected_player=False
        if self.trade_state_player=="Cash":
            if self.player_cash_input.text!="":
                selected_player=True
        elif self.trade_state_player=="Property":
            if self.player_trade_property!=None:
                selected_player=True
        elif self.trade_state_player=="Card":
            if self.card_for_trade!=None:
                selected_player=True
        
        selected_other_player=False
        if self.trade_state_other_player=="Cash":
            if self.other_player_cash_input.text!="":
                selected_other_player=True
        elif self.trade_state_other_player=="Property":
            if self.other_player_trade_property!=None:
                selected_other_player=True
        elif self.trade_state_other_player=="Card":
            if self.card_for_trade_other_player!=None:
                selected_other_player=True
        if selected_player and selected_other_player:
            self.trade_state="Sent"

    def accept_trade(self):
        if self.trade_state_player=="Cash":
           self.current_player.pay_cash(int(self.player_cash_input.text))
           self.trade_other_player.add_cash(int(self.player_cash_input.text))

        elif self.trade_state_player=="Property":
            
            self.player_trade_property.owner=self.trade_other_player
            self.trade_other_player.properties_bought+=1
            self.current_player.properties_sold+=1

        elif self.trade_state_player=="Card":
            
            self.trade_other_player.add_chance_card("Get Out Of Jail")
            self.current_player.chance_cards.pop(0)
            

        
        if self.trade_state_other_player=="Cash":
            self.current_player.add_cash(int(self.other_player_cash_input.text))
            self.trade_other_player.pay_cash(int(self.other_player_cash_input.text))

        elif self.trade_state_other_player=="Property":
           self.other_player_trade_property.owner=self.current_player
           self.current_player.properties_bought+=1
           self.trade_other_player.properties_sold+=1
        elif self.trade_state_other_player=="Card":
            
            self.current_player.add_chance_card("Get Out Of Jail")
            self.trade_other_player.chance_cards.pop(0)
        self.Status=self.previous_State
    def decline_trade(self):
        self.Status=self.previous_State
    def on_trade_card_select(self):
        self.card_for_trade=True

    def on_trade_card_select_other_player(self):
        self.card_for_trade_other_player=True
    
    def on_other_trade_card_select(self):
        self.card_for_trade=True

    
    def show_trade_menu(self):
        self.trade_state="Idle"
        self.player_trade_property=None
        self.card_for_trade=None
        self.other_player_trade_property=None
        self.card_for_trade_other_player=None
        self.trade_state_player="Select"
        self.trade_state_other_player="Select Player"
        if self.Status!="Trading":
            self.previous_State=self.Status
        self.Status="Trading"
        self.trade_frame=Frame((60,60),(570,570),"Trade")
        player=self.current_player
        self.player_trade_buttons=[]
        self.player_cash_input=NumberInput((145,150),(100,35),34,max=player.cash)
        self.other_player_cash_input=NumberInput((470,150),(100,35),34)
        
        self.confirm_trade_button=Button((200,400),(100,50),"Trade",callback=self.confirm_trade,fontsize=25,textcolor="black",bgcolor="yellow",bordercolor="orange",borderwidth=5,borderradius=10)
        self.accept_trade_button=Button((400,400),(100,50),"Accept",callback=self.accept_trade,fontsize=25,textcolor="black",bgcolor="yellow",bordercolor="orange",borderwidth=5,borderradius=10)
        self.deny_trade_button=Button((520,400),(100,50),"Decline",callback=self.decline_trade,fontsize=25,textcolor="black",bgcolor="yellow",bordercolor="orange",borderwidth=5,borderradius=10)

        self.trade_property_selects=[]
        self.trade_card_selects=[]
        self.trade_property_selects_other_player=[]
        self.trade_card_selects_other_player=[]
        self.other_player_trade_buttons=[]
        self.trade_player_select=[]
        self.player_select_rects=[]
        i=0
        for p in self.players:
            if player!=p and not p.is_bankrupt:
                self.player_select_rects.append([p,pygame.Rect((450,160+i*75),p.token.get_size())])
                i+=1
        i=0
        for property in self.current_player.properties:
            add=True
            property=property
            if property.Type=="Street":
                if property.houses!=0:
                    add=False
            if add:    
                name=property.Name
                if len(name)>18:
                    name=name[:18]
                self.trade_property_selects.append([name,Button((260,150+i*26),(70,22),"Select",callback=partial(self.player_property_for_trade,property),fontsize=25,textcolor="black",bgcolor="yellow",bordercolor="orange",borderwidth=5,borderradius=10)])
                i+=1
        i=0
        for card in self.current_player.chance_cards:
            
            
            self.trade_card_selects.append([card,Button((260,150+i*26),(70,22),"Select",callback=partial(self.on_trade_card_select),fontsize=25,textcolor="black",bgcolor="yellow",bordercolor="orange",borderwidth=5,borderradius=10)])
            i+=1
        
        for i,category in enumerate(["Cash","Property","Card"]):
                
                self.player_trade_buttons.append(Button((160,150+i*60),(120,40),category,callback=partial(self.trade_type_select,category),fontsize=20,textcolor="black",bgcolor="yellow",bordercolor="orange",borderwidth=5,borderradius=10))
        
        for i,category in enumerate(["Cash","Property","Card"]):
                
                self.other_player_trade_buttons.append(Button((400,150+i*60),(120,40),category,callback=partial(self.other_player_trade_type_select,category),fontsize=20,textcolor="black",bgcolor="yellow",bordercolor="orange",borderwidth=5,borderradius=10))
               
    def draw_trade_menu(self,screen):
        self.trade_frame.draw(screen)
        player=self.current_player
        draw_text(screen,(220,120),"Yours",FONT,"white",True)
        
       
        
        
        if self.trade_state_player=="Select":
            for i,button in enumerate(self.player_trade_buttons):
                button.draw(screen)
        elif self.trade_state_player=="Cash":
            self.confirm_trade_button.draw(screen)
            draw_text(screen,(90,165),"Cash",FONT,"white")
            
           
            self.player_cash_input.draw(screen)
        elif self.trade_state_player=="Property":
            
            if self.player_trade_property==None:
                for i,select in enumerate(self.trade_property_selects):
                    draw_text(screen,(90,151+i*26),select[0],FONT_SMALL,"white")
                    
                    
                    select[1].draw(screen)
            else:
                self.confirm_trade_button.draw(screen)
                draw_text(screen,(90,151),self.player_trade_property.Name,FONT_SMALL,"white")

               
        elif self.trade_state_player=="Card":
            
            if self.card_for_trade==None:
                for i,select in enumerate(self.trade_card_selects):
                    draw_text(screen,(90,151+i*26),select[0],FONT_SMALL,"white")
                    
                    
                    select[1].draw(screen)
            else:
                self.confirm_trade_button.draw(screen)
                draw_text(screen,(90,151),"Get Out Of Jail",FONT_SMALL,"white")

                
        elif self.trade_state_player=="Card":
            
            if self.player_trade_property==None:
                for i,select in enumerate(self.trade_property_selects):
                    draw_text(screen,(90,151+i*26),select[0],FONT_SMALL,"white")
                    
                    select[1].draw(screen)
            else:
                self.confirm_trade_button.draw(screen)
                draw_text(screen,(90,151),self.player_trade_property.Name,FONT_SMALL,"white",True)

                
        if self.trade_state_other_player=="Select Player":
                text=FONT.render("Select Player",True,"white")
                screen.blit(text,(470-text.get_width()/2,120))
                for p,rect in self.player_select_rects:
                    screen.blit(p.token,rect)
        elif self.trade_state_other_player=="Select":
            draw_text(screen,(470,120),self.trade_other_player.name,FONT,"white",True)
            
            
            
            for i,button in enumerate(self.other_player_trade_buttons):
                button.draw(screen)
        elif self.trade_state_other_player=="Cash":
            draw_text(screen,(470,120),self.trade_other_player.name,FONT,"white",True)
            
            draw_text(screen,(410,165),"Cash",FONT,"white",True)
            

            
            self.other_player_cash_input.draw(screen)
        elif self.trade_state_other_player=="Property":
            draw_text(screen,(470,120),self.trade_other_player.name,FONT,"white",True)
            
            
            if self.other_player_trade_property==None:
                for i,select in enumerate(self.trade_property_selects_other_player):
                    draw_text(screen,(380,151+i*26),select[0],FONT_SMALL,"white")
                    

                    select[1].draw(screen)
            else:
                draw_text(screen,(380,151),self.other_player_trade_property.Name,FONT_SMALL,"white")
                
                
        elif self.trade_state_other_player=="Card":
            text=FONT.render(self.trade_other_player.name,True,"white")
            screen.blit(text,(470-text.get_width()/2,120))
            if self.card_for_trade_other_player==None:
                for i,select in enumerate(self.trade_card_selects_other_player):
                    draw_text(screen,(380,151+i*26),select[0],FONT_SMALL,"white")
                    
                    
                    select[1].draw(screen)
            else:
                draw_text(screen,(380,151),"Get Out Of Jail",FONT_SMALL,"white")
                
                
        if self.trade_state=="Sent":
                    self.accept_trade_button.draw(screen)
                    self.deny_trade_button.draw(screen)
        self.cancel_button.draw(screen)

    def build(self,player,property):
        player=self.current_player
        if player.cash>=property.House_Cost:
            property.houses+=1
            player.pay_cash(property.House_Cost)
            self.show_build_menu()
        print(property.houses)
    def show_build_menu(self):
        if self.Status!="Build":
            self.previous_State=self.Status
        self.Status="Build"
        self.sell_frame=Frame((60,60),(570,570),"Build")
        player=self.current_player
        player.build_buttons=[]
        row=0
        col=0
        checked=[]
        colors=[]
        can_build=False
        for block in self.board.values():
            if block.Type=="Street":
                if not block.Color in checked:
                    checked.append(block.Color)
                    build=True
                    min_house=5
                    for property in self.get_color_property(block.Color):
                        
                        if not property.owner==self.current_player:
                            build=False
                            break
                        min_house=min(min_house,property.houses)
                    if build:
                        colors.append((min_house,block.Color))
        for min_house,color in colors:
            for i,property in enumerate(self.get_color_property(color)):
                    if property.houses==min_house and min_house<5:
                        player.build_buttons.append([property,Button((270+row*280,110+col*26),(70,22),f"Build",callback=partial(self.build,self.current_player,property),fontsize=20,textcolor="black",bgcolor="yellow",bordercolor="orange",borderwidth=5,borderradius=10)])
                        row+=1
                        if row>1:
                            row=0
                            col+=1
    def draw_build_menu(self,screen):
        self.sell_frame.draw(screen)
        player=self.current_player
        
        
        row=0
        col=0
        for i,button in enumerate(player.build_buttons):
            
            
            property=button[0]

            name=property.Name
            if len(name)>15:
                name=name[:13]+".."
            draw_text(screen,(80+row*280,120+col*26),name,FONT_SMALL,"white")
            
            button[1].draw(screen)
            row+=1
            if row>1:
                row=0
                col+=1
        self.cancel_button.draw(screen)
                

    
    def increase_bid(self,player,price):
        if not self.auction_timer<=0 and player.cash>=self.highest_bid+price:
            self.highest_bid+=price
            self.auction_timer=5
            self.highest_bid_player=player
            
    
    
                
    
    def draw(self,screen):
        screen.fill(Background_Color)
        self.board_image.draw(screen)
        if self.Status=="Free" and self.current_player.type!="Bot":
            if self.current_player.in_jail:
                if self.current_player.jail_turns>0:
                    self.roll_button.draw(screen)
                
                self.pay_button.draw(screen)
                if self.current_player.chance_cards!=[]:
                    self.use_card_button.draw(screen)
            else:
                self.roll_button.draw(screen)
        
        self.players_frame.draw(screen)
        self.player_properties_frame.draw(screen)
        row=0
        col=0
        for property in self.current_player.properties:
            
            name=property.Name
            if len(name)>13:
                name=name[:13]
            draw_text(screen,(700+col*140,370+row*20),name,FONT_SMALL,"white")
            
            
            col+=1
            if col>1:
                col=0
                row+=1
        
        
        for i,player in enumerate(self.players):
            screen.blit(player.token,(700,60+i*40))
            color="white"
            cash=player.cash
            if player==self.current_player:
                color="yellow"
            if player.is_bankrupt:
                color="gray"
                cash="Bankrupt"
                
            draw_text(screen,(750,58+i*40),player.name,FONT,color)
            draw_text(screen,(750,78+i*40),"$"+str(cash),FONT,color)
            
            
            player.draw(screen)
            
        self.draw_property_owners(screen)
        
        
        
        
        if self.Status=="OnStreet":
            self.property_card.draw(screen)
            draw_text(screen,(135,160),"Price $"+str(self.current_property.Price)+"  Rent $"+str(self.current_property.Rent),FONT,"white")
            draw_text(screen,(135,185),"With 1 House   $"+str(self.current_property.House1),FONT,"white")
            draw_text(screen,(135,210),"With 2 House   $"+str(self.current_property.House2),FONT,"white")
            draw_text(screen,(135,235),"With 3 House   $"+str(self.current_property.House3),FONT,"white")
            draw_text(screen,(135,260),"With 4 House   $"+str(self.current_property.House4),FONT,"white")
            draw_text(screen,(135,285),"With Hotel   $"+str(self.current_property.Hotel),FONT,"white")
            draw_text(screen,(135,310),"1 House Cost  $"+str(self.current_property.House_Cost),FONT,"white")
            draw_text(screen,(135,335),"Mortgage   $"+str(self.current_property.Mortgage),FONT,"white")
            
            
         
            self.buy_button.draw(screen)
            self.auction_button.draw(screen)
        
        if self.Status=="OnRailRoad":
            self.property_card.draw(screen)
            
            draw_text(screen,(135,160),"Price $"+str(self.current_property.Price),FONT,"white")
            draw_text(screen,(135,185),"With 1 Station   $"+str(self.current_property.station1),FONT,"white")
            draw_text(screen,(135,210),"With 2 Station   $"+str(self.current_property.station2),FONT,"white")
            draw_text(screen,(135,235),"With 3 Station   $"+str(self.current_property.station3),FONT,"white")
            draw_text(screen,(135,260),"With 4 Station   $"+str(self.current_property.station4),FONT,"white")
            
          
            
            
            self.buy_button.draw(screen)
            self.auction_button.draw(screen)
        
        if self.Status=="OnUtility":
            self.property_card.draw(screen)
            draw_text(screen,(135,160),"Price $"+str(self.current_property.Price),FONT,"white")
            draw_text(screen,(135,185),"1 Company dicex"+str(self.current_property.company1),FONT,"white")
            draw_text(screen,(135,210),"2 Companies dicex"+str(self.current_property.company2),FONT,"white")
            

            self.buy_button.draw(screen)
            self.auction_button.draw(screen)
        
        if self.Status=="Chance":
            self.property_card.draw(screen)
            for i,line in enumerate(wrap(self.current_card[0], 20)):
                draw_text(screen,(135,160+i*20),line,FONT,"white")
                
                
            
            
        if self.Status=="Community Chest":
            self.property_card.draw(screen)
            for i,line in enumerate(wrap(self.current_card[0], 20)):
                draw_text(screen,(135,160+i*20),line,FONT,"white")
                
           
        
            
            
            
            
        height=360
        if self.dice_animating:
            height=randint(350,370)
        screen.blit(self.dice[self.dice1-1],(270,height))
        screen.blit(self.dice[self.dice2-1],(350,height))
        
        if self.Status in ["Done","Chance","Community Chest"]  and self.current_player.type!="Bot":
            self.end_turn_button.draw(screen)
        
        if not self.Status in ["Auction","Build","Selling","Trading"]  and self.current_player.type!="Bot":
            self.sell_button.draw(screen)
            self.trade_button.draw(screen)
            self.bankrupt_button.draw(screen)
        
            if self.can_build():
                self.build_button.draw(screen)
        if self.Status=="Auction":
            self.auction_window.draw(screen)
        if self.Status=="Selling":
            self.draw_selling_menu(screen)

        if self.Status=="Trading":
            self.draw_trade_menu(screen)

        if self.Status=="Build":
            self.draw_build_menu(screen)
    def handle_events(self,events):
        
        
        if self.Status=="Free"  and self.current_player.type!="Bot":
            if self.current_player.in_jail:
                if self.current_player.jail_turns>0:
                    self.roll_button.handle_events(events)
                
                self.pay_button.handle_events(events)
                if self.current_player.chance_cards!=[]:
                    self.use_card_button.handle_events(events)
            else:
                self.roll_button.handle_events(events)
            
        elif self.Status in ["OnStreet","OnRailRoad","OnUtility"]:
            self.buy_button.handle_events(events)
            self.auction_button.handle_events(events)
        elif self.Status in ["Done","Chance","Community Chest"]:
            self.end_turn_button.handle_events(events)
        elif self.Status=="Auction":
            self.auction_window.handle_events(events)
        elif self.Status=="Selling" :
            for button in self.current_player.sell_buttons:
                button[1].handle_events(events)
        elif self.Status=="Build"  and self.current_player.type!="Bot":
            for button in self.current_player.build_buttons:
                button[1].handle_events(events)    
        
        if not self.Status in ["Auction","Build","Selling","Trading"] and self.current_player.type!="Bot":
            self.sell_button.handle_events(events)
            self.trade_button.handle_events(events)
            self.bankrupt_button.handle_events(events)
            if self.can_build():
                self.build_button.handle_events(events)
        
        if self.Status in ["Build","Selling","Trading"]:
            self.cancel_button.handle_events(events)
        
        if self.Status=="Trading":
            if  self.trade_state_player=="Select":
                for button in self.player_trade_buttons:
                    button.handle_events(events)
            elif self.trade_state_player=="Cash":
                self.confirm_trade_button.handle_events(events)
                self.player_cash_input.handle_event(events)
            elif self.trade_state_player=="Property":
                self.confirm_trade_button.handle_events(events)
                for name,button in self.trade_property_selects:
                    button.handle_events(events)
            elif self.trade_state_player=="Card":
                self.confirm_trade_button.handle_events(events)
                for name,button in self.trade_card_selects:
                    button.handle_events(events)
            if self.trade_state_other_player=="Select Player":
                
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        for p,rect in self.player_select_rects:
                            if rect.collidepoint(event.pos):
                                self.trade_other_player=p
                                self.other_player_cash_input.max=p.cash
                                self.trade_state_other_player="Select"
                                i=0
                                for property in self.trade_other_player.properties:
                                    add=True
                                    
                                    if property.Type=="Street":
                                        if property.houses!=0:
                                            add=False
                                    if add:    
                                        name=property.Name
                                        if len(name)>18:
                                            name=name[:18]
                                        self.trade_property_selects_other_player.append([name,Button((550,150+i*26),(70,22),"Select",callback=partial(self.other_player_property_for_trade,property),fontsize=25,textcolor="black",bgcolor="yellow",bordercolor="orange",borderwidth=5,borderradius=10)])
                                        i+=1
                                i=0
                                for card in self.trade_other_player.chance_cards:
                                    
                                    
                                    self.trade_card_selects_other_player.append([card,Button((550,150+i*26),(70,22),"Select",callback=partial(self.on_trade_card_select_other_player),fontsize=25,textcolor="black",bgcolor="yellow",bordercolor="orange",borderwidth=5,borderradius=10)])
                                    i+=1
                                
            elif  self.trade_state_other_player=="Select":
                for button in self.other_player_trade_buttons:
                    button.handle_events(events)
            elif self.trade_state_other_player=="Cash":
                
                self.other_player_cash_input.handle_event(events)
            elif self.trade_state_other_player=="Property":
                for name,button in self.trade_property_selects_other_player:
                    button.handle_events(events)
            elif self.trade_state_other_player=="Card":
                for name,button in self.trade_card_selects_other_player:
                    button.handle_events(events)
            if self.Status=="Trading":
                if self.trade_state=="Sent":
                    self.accept_trade_button.handle_events(events)
                    self.deny_trade_button.handle_events(events)
    def Done_Turn(self):
        self.next_player_turn()
    
    def get_all_RailRoads(self,player):
        count=0
        for block in self.board.values():
            if block.Type=="RailRoad":
                if block.owner==player:
                    count+=1
                    
        return count

    def get_all_companies(self,player):
        count=0
        for block in self.board.values():
            if block.Type=="Utility":
                if block.owner==player:
                    count+=1
                    
        return count
    
    def pay_to_release(self):
        if self.current_player.cash>=50:
            self.current_player.jail_turns=0
            self.current_player.in_jail=False
            self.current_player.pay_cash(50)
            

    def use_card_to_release(self):
        self.current_player.use_chance_card()
            
    def check_spot(self):
        spot=self.board[self.current_player.position]
        self.current_spot=spot
        if spot.Type=="Street":
            if spot.owner==None:
                self.Status="OnStreet"
                self.current_property=spot
                self.property_card=Frame((120,110),(250,260),spot.Name)
                self.buy_button.enable=True
                if self.current_player.cash<spot.Price:
                    self.buy_button.enable=False
            
            elif spot.owner!=self.current_player:
                rent=0
                if spot.houses==0:
                    rent=spot.Rent
                    
                elif spot.houses<5:
                    rent=getattr(spot,f"House{spot.houses}")
                    
                else:
                    rent=spot.Hotel
                    
                self.current_player.pay_cash(rent)
                spot.owner.add_cash(rent)
                self.Status="Done"
            elif self.dice1 == self.dice2:
                self.double_counter+=1
                if self.double_counter==3:
                    self.current_player.go_to_jail()    
                    self.Status="Done"
                else:
                    self.Status="Free"
            else:
                self.Status="Done"
        
        elif spot.Type=="RailRoad":
            if spot.owner==None:
                self.Status="OnRailRoad"
                self.current_property=spot
                self.property_card=Frame((120,110),(250,260),spot.Name)
                self.buy_button.enable=True
                if self.current_player.cash<spot.Price:
                    self.buy_button.enable=False
            
            elif spot.owner!=self.current_player:
                rent=getattr(spot,f"station{self.get_all_RailRoads(spot.owner)}")
                self.current_player.pay_cash(rent)
                spot.owner.add_cash(rent)
                self.Status="Done"
            elif self.dice1 == self.dice2 and self.double_counter!=3:    
                    
                self.Status="Free"
            else:
                self.Status="Done"
        elif spot.Type=="Utility":
            if spot.owner==None:
                self.Status="OnUtility"
                self.current_property=spot
                self.property_card=Frame((120,110),(250,260),spot.Name)
                self.buy_button.enable=True
                if self.current_player.cash<spot.Price:
                    self.buy_button.enable=False
            
            elif spot.owner!=self.current_player:
                rent=getattr(spot,f"company{self.get_all_companies(spot.owner)}")
                self.current_player.pay_cash(rent*(self.dice1+self.dice2))
                spot.owner.add_cash(rent*(self.dice1+self.dice2))
                self.Status="Done"
            elif self.dice1 == self.dice2 and self.double_counter!=3:    
                    
                self.Status="Free"
            else:
                self.Status="Done"
        
        elif spot.Type=="Chance":
            self.property_card=Frame((120,110),(250,260),"Chance")
            self.Status="Chance"
            self.current_card=choice(self.chance_cards)
            self.current_card[1](self.current_player)
        
        elif spot.Type=="Community Chest":
            self.property_card=Frame((120,110),(250,260),"Community Chest")
            self.Status="Community Chest"
            self.current_card=choice(self.community_chest_cards)
            self.current_card[1](self.current_player)
        
        elif spot.Type=="Tax":
            self.current_player.pay_cash(spot.Fee)
            self.current_player.tax_payed+=spot.Fee
            self.Status="Done"
        
        elif spot.Type=="Go To Jail":
            self.current_player.go_to_jail()
            self.Status="Done"
        else:
            self.Status="Done"
            
    
    def check_spot_bot(self):
        player=self.current_player
        block=self.board[player.position]
        self.current_property=block
        if player.in_jail:
            if player.chance_cards!=[]:
                player.use_chance_card()
            elif player.cash>=50:
                player.pay_cash(50)
                player.in_jail=False
                player.jail_turns=0
            self.Done_Turn()
        if block.Type=="Street":
            if block.owner==None :
                if player.cash>=block.Price:
                    block.owner= self.current_player
                    player.pay_cash(block.Price)
                    self.Done_Turn()
                else:
                    self.Status="Auction"
                    self.show_auction()
            elif block.owner!=self.current_player:
                rent=0
                if block.houses==0:
                    rent=block.Rent
                    
                elif block.houses<5:
                    rent=getattr(block,f"House{block.houses}")
                    
                else:
                    rent=block.Hotel
                if player.cash<rent:
                    player.bankrupt()
                    self.Done_Turn()
                else:
                    self.current_player.pay_cash(rent)
                    block.owner.add_cash(rent)
                    self.Done_Turn()
            else:
                self.Done_Turn()
        elif block.Type =="RailRoad":
            if block.owner==None:
                if player.cash>=block.Price:
                    block.owner= self.current_player
                    player.pay_cash(block.Price)
                    self.Done_Turn()
                else:
                    self.Status="Auction"
                    self.show_auction()
            elif block.owner!=self.current_player:
                rent=getattr(block,f"station{self.get_all_RailRoads(block.owner)}")
                if player.cash<rent:
                    player.bankrupt()
                    self.Done_Turn()
                else:
                    self.current_player.pay_cash(rent)
                    block.owner.add_cash(rent)
                    self.Done_Turn()
            else:
                self.Done_Turn()
        elif block.Type =="Utility":
            if block.owner==None:
                if player.cash>=block.Price:
                    block.owner= self.current_player
                    player.pay_cash(block.Price)
                    self.Done_Turn()
                else:
                    self.Status="Auction"
                    self.show_auction()
            elif block.owner!=self.current_player:
                rent=getattr(block,f"company{self.get_all_companies(block.owner)}")
                if player.cash<rent:
                    player.bankrupt()
                    self.Done_Turn()
                else:
                    self.current_player.pay_cash(rent*(self.dice1+self.dice2))
                    block.owner.add_cash(rent*(self.dice1+self.dice2))
                    self.Done_Turn()
            else:
                self.Done_Turn()
        elif block.Type=="Chance":
            self.property_card=Frame((120,110),(250,260),"Chance")
            self.Status="Chance"
            self.delay=3
            self.current_card=choice(self.chance_cards)
            self.current_card[1](self.current_player)
        
        elif block.Type=="Community Chest":
            self.property_card=Frame((120,110),(250,260),"Community Chest")
            self.Status="Community Chest"
            self.delay=3
            self.current_card=choice(self.community_chest_cards)
            self.current_card[1](self.current_player)
        
        elif block.Type=="Tax":
            if self.current_player.cash>=block.Fee:
                self.current_player.pay_cash(block.Fee)
                self.current_player.tax_payed+=block.Fee
                self.Done_Turn()
            else:
                player.bankrupt()
                self.Done_Turn()
        elif block.Type=="Go To Jail":
            player.go_to_jail()
            self.Done_Turn()
        else:
            self.Done_Turn()
    
    def check_bot_auction(self):
        property=self.board[self.current_player.position]
        for player in self.players:
            if player.type=="Bot":
                if player.cash>=self.highest_bid+2 and self.highest_bid+2<(property.Price/100)*100:
                    if randint(0,20)==5 and self.highest_bid_player!=player:
                        self.increase_bid(player,2)

    
    def update(self,deltatime):
        if not self.GameOver:
            if self.current_player.is_bankrupt:
                self.Done_Turn()
            if self.delay>0:
                self.delay-=deltatime
                if self.delay<=0:
                    self.Done_Turn()
            else:
                current_player= self.current_player
                if current_player.type=="Bot" :
                    if self.Status=="Free":
                        self.animate_dice()
                
                

                if self.dice_animating:
                    self.dice1=randint(1,6)
                    self.dice2=randint(1,6)
                    if self.animation_duration<self.animation_timer:
                        self.dice_animating=False
                        total=self.dice1+self.dice2
                        if self.dice1==self.dice2:
                            
                            current_player.jail_turns=0
                            current_player.in_jail=False
                        elif current_player.in_jail and current_player.jail_turns!=0:
                            current_player.jail_turns-=1
                        if current_player.jail_turns==0:
                            current_player.move_spaces(total)
                            if current_player.type=="Bot":
                                self.check_spot_bot()
                            else:
                                self.check_spot()
                            
                        else:
                            if current_player.type=="Bot":
                                self.check_spot_bot()
                            else:
                                self.Status="Done"
                        
                            
                    self.animation_timer+=deltatime
                if self.Status=="Auction":
                    if self.auction_window.update(deltatime) !=None:
                        if current_player.type=="Bot":
                            self.Done_Turn()
                        else:
                            self.Status="Done"
        else:
            players={}
            if os.path.isfile("leaderboard.csv"):
                players={}

                with open('leaderboard.csv') as leaderboard_file:
                    csv_reader = csv.reader(leaderboard_file, delimiter=',')
                    i=0
                    
                    for row in csv_reader:
                        if i!=0:
                            players[row[0]]=row[1]
                        i+=1
            
            name=self.players[self.winner].name
            if name in players:
                players[name]=int(players[name])+1
            else:
                players[name]=1
            with open('leaderboard.csv', mode='w',newline='') as leaderboard_file:
                fieldnames = ['Player', 'Wins']
                writer = csv.DictWriter(leaderboard_file, fieldnames=fieldnames)

                writer.writeheader()
                for name,wins in players.items():
                    print(name)
                    writer.writerow({'Player': name, 'Wins': wins})
                
            return self.players





class Auction_Window:
    def __init__(self,players,property) -> None:
        self.frame=Frame((120,110),(440,440),"Auction")
        self.players=players
        self.property=property
        self.auction_timer=5
        self.auction_duration=5
        self.highest_bid=2
        self.highest_bid_player=None
        self.bid_buttons=[]
        y=0
        for player in self.players:
                if not player.is_bankrupt:
                    if player.type!="Bot":
                        for x,bid in enumerate([2,10,100]):
                            
                            self.bid_buttons.append(Button((200+x*110,260+y*38),(100,40),f"${bid}",callback=partial(self.place_bid,player,bid),fontsize=30,textcolor="black",bgcolor="yellow",bordercolor="orange",borderwidth=5,borderradius=10))
                    y+=1
    
    def place_bid(self,player,bid):
        if not self.auction_timer<=0 and player.cash>=self.highest_bid+bid:
            self.highest_bid+=bid
            self.auction_timer=5
            self.highest_bid_player=player
    
    def bot_bid(self):
        for player in self.players:
            if player.type=="Bot":
                if player.cash>=self.highest_bid+2 and self.highest_bid+2<(self.property.Price/100)*100:
                    if randint(0,30)==5 and self.highest_bid_player!=player:
                        self.place_bid(player,2)
    
    def draw(self,screen):
        self.frame.draw(screen)

        
        draw_text(screen,(340,160),self.property.Name,FONT,"white",True)
        
        draw_text(screen,(190,200),"$"+str(self.highest_bid),FONT,"white")
        
        draw_text(screen,(280,200),"Time Left:"+str(int(self.auction_timer)),FONT,"white")
        
        if self.highest_bid_player!=None:
            screen.blit(self.highest_bid_player.token,(150,190))
        
        y=0
        for i,player in enumerate(self.players):
            if not player.is_bankrupt:
                screen.blit(player.token,(140,260+y*38))
                
                y+=1
        for buttons in self.bid_buttons:
                buttons.draw(screen)
    
    def update(self,deltatime):
        self.bot_bid()
        self.auction_timer-=deltatime
        if self.auction_timer<=0:
            if self.highest_bid_player!=None:
                self.highest_bid_player.pay_cash(self.highest_bid)
                self.property.owner=self.highest_bid_player
                self.highest_bid_player.properties_bought+=1
            return True
    
    def handle_events(self,events):
        
        for button in self.bid_buttons:
            button.handle_events(events)








