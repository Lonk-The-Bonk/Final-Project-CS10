from menu import MainMenu
from monopoly import Monopoly
from winscreen import WinScreen
class Game:
    STATE="MENU"
    
    def __init__(self) -> None:
        self.menu=MainMenu()
        
    
    def load_resources(self):
        pass
    
    def draw(self,screen):
        if self.STATE=="MENU":
            self.menu.draw(screen)
        elif self.STATE=="GAME":
            self.monopoly.draw(screen)
        elif self.STATE=="WinScreen":
            self.winscreen.draw(screen)
    
    def update(self,deltatime):
        if self.STATE=="MENU":
            players=self.menu.update(deltatime)
            if players:
                self.monopoly=Monopoly(players)
                self.STATE="GAME"
        elif self.STATE=="GAME":
            players=self.monopoly.update(deltatime)
            if players:
                self.winscreen=WinScreen(players)
                self.STATE="WinScreen"
        elif self.STATE=="WinScreen":
            self.winscreen.update(deltatime)
    def handle_events(self,events):
        if self.STATE=="MENU":
            self.menu.handle_events(events)
        elif self.STATE=="GAME":
            self.monopoly.handle_events(events)
        elif self.STATE=="WinScreen":
            self.winscreen.handle_events(events)


