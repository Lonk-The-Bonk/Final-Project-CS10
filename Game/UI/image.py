import pygame


class Image:
    def __init__(self,image_path,position,alignV="top",alignH="left") -> None:
        self.image=pygame.image.load(image_path).convert_alpha()
        self.position=list(position)
        
        if alignV=="center":
            self.position[1]-=self.image.get_height()/2
        elif alignV=="bottom":
            self.position[1]-=self.image.get_height()
        
        if alignH=="center":
            self.position[0]-=self.image.get_width()/2
        elif alignH=="right":
            self.position[0]-=self.image.get_width()
        
    def draw(self,screen):
        screen.blit(self.image,self.position)