import pygame
from settings import WIDTH,HEIGHT,FPS
from game import Game


pygame.init()

def run():
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    clock=pygame.time.Clock()
    
    Monopoly=Game()
    
    Game_Over=False
    while not Game_Over:
        clock.tick(FPS)
        delta_time=clock.get_time()/1000
        events=pygame.event.get()
        
        for event in events:
            if event.type == pygame.QUIT:
                Game_Over=True
                break
        Monopoly.update(delta_time)
        Monopoly.draw(screen)
        Monopoly.handle_events(events)
        
        
        pygame.display.flip()
        



if __name__=="__main__":
    run()