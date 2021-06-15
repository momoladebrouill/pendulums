import pygame as pg

import math
import random
from pygame import gfxdraw
from colorsys import hsv_to_rgb
# Constantes :
FPS = 60  # les fps tabernak
WIND = 750 # dimentions de la fentere
pg.init()
f = pg.display.set_mode(size=(WIND, WIND))
pg.display.set_caption("Pendulum")
fpsClock = pg.time.Clock()
font = pg.font.Font('../consolas.ttf', 30) #police//roxane
b = 1
positions=[]
dreams=list()
nbs=3
longu=WIND/2/nbs
nbs-=1

class Pos:
    def __init__(self,x=0,y=0):
        self.x=x
        self.y=y
        self.taille=WIND/2
    def get_pos(self):
        return (self.x,self.y)
    
class Pendule:
    def __init__(self,x,y):
        self.pos=Pos(x,y)
        self.angle=-random.random()*math.pi
        self.coef=50
        self.mouv=0
        self.boul=Pos(self.pos.x+math.cos(self.angle)*self.coef,self.pos.y+math.sin(self.angle)*self.coef)
    def update(self):
        if self.pos.x>self.boul.x:
            self.mouv-=0.001
        else:
            self.mouv+=0.001
        self.angle+=self.mouv
        self.angle=self.angle%math.tau
    
    def draw(self):
        self.boul.x=self.pos.x+math.cos(self.angle)*longu
        self.boul.y=self.pos.y+math.sin(self.angle)*longu
        pg.draw.line(f,(255,255,255),self.pos.get_pos(),self.boul.get_pos())
        pg.draw.circle(f,(255,0,0),self.boul.get_pos(),5)        
def dist(a:Pos,b:Pos):
    return math.sqrt((a.x-b.x)**2+(a.y-b.y)**2)

mouv_speed=10
dreams.append(Pendule(WIND/2,WIND/2))
for i in range(nbs):
    dreams.append(Pendule(dreams[i].boul.x,dreams[i].boul.y))
try:
    while b:
        b+=1
        # Actualiser:
        pg.display.flip()
        # Appliquer les images de fond sur la fenetre
        s = pg.Surface((WIND, WIND))  
        s.set_alpha(150)
        s.fill((0, 0, 0))
        f.blit(s, (0, 0))
        
        
        dreams[0].update()
        for i in range(nbs):
            dreams[i+1].pos=dreams[i].boul
            dreams[i+1].update()
        positions.append((Pos(dreams[-1].boul.x,dreams[-1].boul.y),dreams[0].angle))
        ind=0
        for ind,posz in enumerate(positions):
            coul=hsv_to_rgb(posz[1]/math.tau,1,255)
            if ind>0:
                pg.draw.line(f,coul,(posz[0].x,posz[0].y),(positions[ind-1][0].x,positions[ind-1][0].y))
            pg.draw.rect(f,coul,(posz[0].x,posz[0].y,1,1))
            ind+=1
        if ind>1000:
            positions.pop(0)
        for rev in dreams:
            rev.draw()
        
        
       
        pointer = pg.mouse
        pos = pointer.get_pos()

        for event in pg.event.get():  # QUAND la touche est appuyée
            if event.type == pg.QUIT:
                b = False
                print(" Fin du jeu  babe")
            elif event.type == pg.KEYUP:
                if event.dict['key']==pg.K_a:
                    for i in dreams:
                        i.angle=0
                if event.dict['key']==pg.K_SPACE:
                    dreams[0].__init__(WIND/2,WIND/2)
                    for i in range(nbs):
                        dreams[i+1].__init__(dreams[i].boul.x,dreams[i].boul.y)
                    positions=[]
                    
                """if event.dict['key']==pg.K_a:"""
                    
            elif event.type == pg.MOUSEBUTTONUP:
                """if event.button==1: #click gauche
                    pos=event.pos


                if event.button==3: #click droit
                   
                elif event.button==4: #vers le haut
                    zoom+=0.01
                elif event.button==5: #vers le bas
                    zoom-=0.01"""

        #text = font.render(str(reve.angle), True, (255,255,255))
        #textRect = text.get_rect()        
        #f.blit(text, (0,0))


        fpsClock.tick(FPS)
except :
    pg.quit()
    raise
finally:
    pg.quit()
