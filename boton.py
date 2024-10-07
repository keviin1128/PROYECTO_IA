import pygame as pg

class Button: 
    def __init__(self, x=0, y=0, text="", width=200, height=50, elev=6): #elev es la elevacion del boton 
        self.font = pg.font.Font('font/minecraft_font.ttf', 20)
        self.text = self.font.render(text, True, (255, 255, 255))
        self.text_rect = self.text.get_rect()
        
        self.bottom_rect = pg.Rect((x+elev, y+elev) , (width, height)) #Rectangulo de abajo
        self.top_rect = pg.Rect((x, y) , (width, height)) #Rectangulo de arriba
        self.text_rect.center = self.top_rect.center #Centramos el texto
        
        self.hovered = False
        self.clicked = False
        self.pressed = False
        
    def update(self): #Actualiza el estado del boton
        self.clicked = False
        mouse_pos = pg.mouse.get_pos() #Obtenemos la posicion del mouse
        
        if self.top_rect.collidepoint(mouse_pos):
            self.hovered = True
            if pg.mouse.get_pressed()[0]: #Si presionamos el boton mientras el mouse esta sobre el
                self.pressed = True
                self.clicked = True
            else:
                self.pressed = False
        else:
            self.hovered = False
            
        
    def draw(self, display): #Dibuja el boton
        top_rect_color = "#317bcf" if self.hovered else "#3194cf"
        if not self.pressed: 
            #Si no esta presionado el boton, se dibuja el rectangulo de arriba
            pg.draw.rect(display, "#1a232e", self.bottom_rect)
            pg.draw.rect(display, top_rect_color, self.top_rect)
            self.text_rect.center = self.top_rect.center
        else:
            #Si esta presionado el boton, se dibuja el rectangulo de abajo
            pg.draw.rect(display, top_rect_color, self.bottom_rect)
            self.text_rect.center = self.bottom_rect.center
        display.blit(self.text, self.text_rect)
        
    def reset(self):
        self.hovered = False
        self.clicked = False
        self.pressed = False
        
        