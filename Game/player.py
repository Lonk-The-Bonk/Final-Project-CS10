import pygame

class Player:
    def __init__(self,name,token,type,index,board) -> None:
        self.name=name
        self.token=token
        self.position=0
        self.cash=1500
        self.type=type
        self.small_token=pygame.transform.smoothscale(self.token,(20,20))
        self.properties=[]
        self.all_players=[]
        self.chance_cards=[]
        self.jail_turns=0
        self.in_jail=False
        self.board=board
        self.index=index
        self.is_bankrupt=False
        self.total_cash_received=0
        self.total_cash_spent=0
        self.properties_bought=0
        self.properties_sold=0
        self.tax_payed=0
        self.jail_counter=0
    
    def move_to_space(self, space_num, collect=False):
        if collect:
            self.add_cash(200)
        self.position = space_num
    
    def buy_property(self,property):
        property.owner=self
        self.pay_cash(property.Price)
        self.properties.append(property)
        self.properties_bought+=1


    def sell_property(self,property):
        if property in self.properties:
            self.properties.remove(property)
            property.owner=None
            self.add_cash(int(property.Price/2))
            self.properties_sold+=1
    
    def transfer_property(self,player,property):
        if property in self.properties:
            self.properties.remove(property)
            self.properties_sold+=1
            property.owner=player
            player.properties.append(property)
            player.properties_bought+=1
    
    
    
    def get_board_coordinates(self):
    
        if self.position < 10:
            x = 10 - self.position
            y = 10
        elif self.position < 20:
            x = 0
            y = 10 - (self.position - 10)
        elif self.position < 30:
            x = self.position - 20
            y = 0
        else:
            x = 10
            y = self.position - 30
            
        # Scale the x and y values based on the board width
        scale_factor = 560 / 11  # 11 is the width of the board in positions
        x *= scale_factor
        y *= scale_factor
        x+=70
        y+=65
        return (x, y)
        
    def move_to_nearest_utility(self):
        if self.position == 7:
            self.move_to_space(12)
        elif self.position == 22:
            self.move_to_space(28)
        elif self.position == 36:
            self.move_to_space(12, collect=True)

    def move_to_nearest_RailRoad(self):
        if self.position == 7 or self.position == 36:
            self.move_to_space(15)
        elif self.position == 22:
            self.move_to_space(25)
        elif self.position == 33:
            self.move_to_space(5)

    def move_spaces(self, num_spaces):
        self.position += num_spaces
        if self.position >= 40:
            self.position -= 40
            self.add_cash(200)
          

    def go_to_jail(self):
        self.jail_counter+=1
        self.position = 10
        self.in_jail=True
        self.jail_turns = 3
        print(f"{self.name} has been sent to jail.")

    def add_cash(self, amount):
        self.cash += amount
        self.total_cash_received+=amount
        print(f"{self.name} received ${amount}. New balance: ${self.cash}.")

    def pay_cash(self, amount):
        if amount>self.cash:
            self.bankrupt()
        else:
            self.total_cash_spent+=amount
            self.cash -= amount
        
   

    def pay_players(self, amount):
        for other_player in self.all_players:
            if other_player != self:
                other_player.add_cash(amount)
                self.pay_cash(amount)
    
    def make_repairs(self,house,hotel):
        pass
        #self.pay_cash(total_cost)
    def add_chance_card(self, card_text):
        self.chance_cards.append(card_text)
        print(f"{self.name} received a '{card_text}' chance card.")
    
    def use_chance_card(self):
        if len(self.chance_cards) > 0:
            self.chance_cards.pop(0)
            self.jail_turns=0
            self.in_jail=False
    
    def bankrupt(self):
        self.cash=0
        for property in self.board.values():
            if property.Type in ["Street","RailRoad","Utility"]:
                if property.owner==self.index:
                    property.owner=None
                    if property.Type=="Street":
                        property.houses=0
        self.is_bankrupt=True
    
    
    def draw(self,screen):
        if not self.is_bankrupt:
            screen.blit(self.token,self.get_board_coordinates())
    
    