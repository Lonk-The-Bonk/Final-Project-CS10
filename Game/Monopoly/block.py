class Block:
    def __init__(self,data) -> None:
        if data is not None:
            for key, value in data.items():
                setattr(self, key, value)
        if self.Type=="Street":
            self.houses=0
        
        self.owner=None
        
        
        
  