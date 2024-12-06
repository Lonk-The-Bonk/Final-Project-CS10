def next_player_turn(self):
        i=self.current_player.index+1
        if i>=len(self.players):
            i=0
        
        self.current_player=self.players[i]
        self.Status="Free"

#Problem