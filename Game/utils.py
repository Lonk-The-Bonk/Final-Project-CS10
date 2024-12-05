

def draw_text(screen,position,text,font,color,center=False):
    text_surface=font.render(text,True,color)
    x,y=position
    if center:
        x-=text_surface.get_width()/2
    screen.blit(text_surface,(x,y))